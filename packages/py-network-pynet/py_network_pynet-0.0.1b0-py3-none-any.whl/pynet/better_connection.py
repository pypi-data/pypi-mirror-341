
from .system_header import *
import struct

import socket

class ConnectionRole(IntFlag):
    OFF_=0
    SEND=1
    RECV=2
    UDP_=4
    TCP_=8
    UNIX=16
    MCST=32
    BIND=64
    REUSE=128

    @staticmethod
    def make(keys):
        if isinstance(keys,ConnectionRole):
            return keys
        value = ConnectionRole.OFF_
        for k in keys:
            try:
                if k[0].lower() == 's':
                    value |= ConnectionRole.SEND
                elif k[0].lower() == 'r':
                    if k[2].lower() == 'c':
                        value |= ConnectionRole.RECV
                    elif k[2].lower() == 'u':
                        value |= ConnectionRole.REUSE
                elif k[0].lower() == 'u':
                    if k[1].lower() == 'd':
                        value |= ConnectionRole.UDP_
                    elif k[1].lower() == 'n':
                        value |= ConnectionRole.UNIX
                elif k[0].lower() == 't':
                    value |= ConnectionRole.TCP_
                elif k[0].lower() == 'b':
                    value |= ConnectionRole.BIND
                elif k[0].lower() == 'm':
                    value |= ConnectionRole.MCST
            except:
                pass
        return value


class MessageWrapper(object):
    def __init__(self):
        self.buff = None
        self.ready = False
        self.active = None
        self.rem_segs = None
        self.rem_lens = None
        self._excess = bytes()

    @staticmethod
    def wrap(raw_msg:List[bytes]) -> List[bytes]:
        segments = len(raw_msg)
        seglens = [len(x) for x in raw_msg]
        wrapped = [None]*segments
        index = 0
        while segments:
            pad = struct.pack('>HH',index,seglens[index]) if index else struct.pack('>HHH',segments,index,seglens[index])
            wrapped[index] = pad + raw_msg[index]
            index += 1
            segments -= 1
        return wrapped

    def parse(self,buffer:bytes):
        if self.ready:
            return
        buffer = self._excess+buffer
        self._excess = bytes()
        if self.buff is None:
            self.rem_segs = struct.unpack('>H',buffer[:2])[0]
            buffer = buffer[2:]
            self.buff = [None]*self.rem_segs
            self.active = 0
        while len(buffer) and self.rem_segs:
            if self.rem_lens is None:
                header = struct.unpack('>HH',buffer[:4])
                if header[0] not in [self.active,self.active+1]:
                    print("------------desync---------------")
                self.active = header[0]
                self.rem_lens = header[1]
                buffer = buffer[4:]
                if self.active < len(self.buff):
                    self.buff[self.active] = bytes()
            chunk = buffer[:self.rem_lens]
            self.rem_lens -= len(chunk)
            buffer = buffer[len(chunk):]
            if self.active < len(self.buff):
                self.buff[self.active] += chunk
            if self.rem_lens == 0:
                self.rem_lens = None
                self.rem_segs -= 1
        if self.rem_segs == 0:
            if len(buffer):
                self._excess = buffer
            self.ready = True
            self.rem_segs = None
            self.rem_lens = None

    def get(self):
        if not self.ready:
            return []
        buff = [x for x in self.buff]
        self.buff = None
        self.active = None
        return buff if len(buff) > 1 else buff[0]

def zmq_poll(sockets:List[Tuple[Any,int]],timeout:int=None):
    socks = {}
    for sock,flag in sockets:
        socks[sock.fileno()] = sock
    try:
        result = dict(zmq.zmq_poll(sockets,timeout))
    except Exception as e:
        import traceback
        thread = threading.current_thread()
        try:
            print(thread.getName(),'..stopping')
            thread.stop(traceback.format_exc())
        except:
            pass
        return dict()
    better_result = dict()
    for k,v in result.items():
        if isinstance(k,int):
            try:
                better_result[socks[k]] = v
            except:
                print(k,v,socks,better_result)
                raise
        else:
            better_result[k] = v
    return better_result
zmq_poll.__doc__ = "\n".join(["USE_IN BetterThread",zmq.zmq_poll.__doc__])

class BetterConnection(object):
    def __init__(self,role:ConnectionRole,
                      addr:Union[str,List[str]],
                      port:Union[int,str,List[Union[int,str]]],
                      _ctx:zmq.Context=None):
        self.role = role
        self._ctx = _ctx
        self._ctx_owner = _ctx is None
        self._sock = None
        self._conn = None
        if isinstance(addr,list) or isinstance(port,list):
            if role & ConnectionRole.BIND:
                raise ValueError("Cannot bind to multiple connections.")
            if not (isinstance(addr,list) and isinstance(port,list)):
                raise ValueError("Both addr and port must be lists")
            if len(addr)!=len(port):
                raise ValueError("Both addr and port must be lists of the same length")
            self.net = (addr,port)
        else:
            self.net = ([addr],[port])
        self.sendpoint = None
        self.endpoint = None
        self._n0 = 0

    def __str__(self):
        state = ((int(self._conn is not None) << 0)
                +(int(self._sock is None) << 1))
        if state == 0:
            state = "Pending"
        elif state == 1:
            state = "Running"
        elif state in [2,3]:
            state = "Closed"
        out = f"<BetterConnection: {state}, role: {str(self.role)}, fileno: {self.fileno()}>"
        return out

    def __repr__(self):
        return str(self)

    def connect(self):
        if self.role & ConnectionRole.REUSE:
            return self._connect_socket()
        self._ctx = self._ctx if self._ctx else zmq.Context()
        self.protocol = None
        if self.role & (ConnectionRole.RECV | ConnectionRole.SEND):
            if (self.role & (ConnectionRole.RECV | ConnectionRole.SEND) == (ConnectionRole.RECV | ConnectionRole.SEND)):
                self._sock_type = zmq.ROUTER
            else:
                self._sock_type = zmq.SUB if not self.role & ConnectionRole.SEND else zmq.PUB
        if self.role & ConnectionRole.MCST:
            if self.role & ConnectionRole.UDP_:
                self._sock_type = zmq.DGRAM
                self.protocol = 'udp'
                self.role |= ConnectionRole.BIND # must bind
            else:
                self._sock_type = zmq.STREAM
                self.protocol = 'tcp'
        elif self.role & ConnectionRole.UDP_:
            raise NotImplementedError("If you're here, this isn't functional")
            self.protocol = 'udp'
        elif self.role & ConnectionRole.TCP_:
            self.protocol = 'tcp'
        elif self.role & ConnectionRole.UNIX:
            self.protocol = 'ipc'
        if self.protocol is None:
            self.role |= ConnectionRole.TCP_
            self.protocol = 'tcp'
        # print("socket type:",self._sock_type)
        self._sock = self._ctx.socket(self._sock_type)
        endpoint = f"{self.protocol}://{self.net[0][0]}:{self.net[1][0]}"
        if self.role & ConnectionRole.BIND:
            if self._sock_type == zmq.ROUTER:
                self._sock.identity = endpoint.encode()
            if self.role & ConnectionRole.MCST:
                pass
            self._conn = self._sock.bind(endpoint)
            self.endpoint = self._sock.LAST_ENDPOINT
            # print("Socket bind ",end='')
            if self._sock_type in [zmq.DGRAM, zmq.STREAM]:
                self.sendpoint = self.endpoint
        else:
            if self._sock_type == zmq.ROUTER:
                self.sendpoint = [f"{self.protocol}://{a}:{p}" for a,p in zip(self.net[0],self.net[1])]
            endpoints = [f"{self.protocol}://{a}:{p}" for a,p in zip(self.net[0],self.net[1])]
            self._conn = [None]*len(endpoints)
            for idx,ep in enumerate(endpoints):
                self._conn[idx] = self._sock.connect(ep)
                endpoints[idx] = self._sock.LAST_ENDPOINT
            self.endpoint = endpoints
            # print("Socket connect ",end='')
        # print(self.endpoint)
        if self._sock_type == zmq.SUB:
            self._sock.setsockopt_string(zmq.SUBSCRIBE,'')
        return self

    def _connect_socket(self):
        group = self.net[0][0]
        port = self.net[1][0]
        ttl = 4
        self._sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP
        )
        self._sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_MULTICAST_TTL,
            ttl
        )
        self._sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )
        self._sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEPORT,
            1
        )
        self._sock.setblocking(0)

        self._sock.bind((group,port))

        grp_req = struct.pack("4sl",socket.inet_aton(group),socket.INADDR_ANY)
        self._sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            grp_req
        )
        self.sendpoint = (group,port)
        self._sock_type = zmq.DGRAM

    def get_socket(self):
        return self._sock

    def send(self,msg:Union[ClientRequest,str,List[str]],tag:bytes=None,_raw=True):
        try:
            self.sendto(msg,tag=tag,_raw=_raw)
        except RuntimeError as e:
            if "destination" in str(e).lower():
                raise RuntimeError(str(e) + ", use sendto and specify dest:Tuple")
            raise

    def sendto(self,msg:Union[ClientRequest,str,List[str]],dest:Tuple=None,tag:bytes=None,_raw=True):
        # confirm message is useable
        if not isinstance(msg,(ClientRequest,str,bytes)):
            if not isinstance(msg,(list,tuple)):
                raise ValueError(f"Cannot interpret msg of type: {type(msg)}")
            if not all([isinstance(x,(str,bytes)) for x in msg]):
                raise ValueError(f"Cannot interpret iterable message whose values aren't in (str,bytes)")

        dests = None
        if isinstance(msg,(list,tuple)):
            msg = [x.encode() if isinstance(x,str) else x for x in msg]
            if b'' in msg:
                split_on = msg.index(b'')
                dests = msg[:split_on]
                msg = msg[split_on+1:]
        elif isinstance(msg,ClientRequest):
            payload = msg.get_payload()
            split_on = payload.index(b"")
            dests = payload[:split_on]
            msg = payload[split_on+1:]
        else:
            if isinstance(msg,str):
                msg = msg.encode()
            if isinstance(msg,bytes):
                msg = [msg]


        # print(dest,tag,msg) # not it
        if self._sock_type in [zmq.PUB]:
            dests = [self.endpoint]

        # print(msg,dest,dests)
        if dests is None:
            def parse_str(d):
                if "://" in d:
                    _,d = d.split("://")
                if ":" not in d:
                    raise ValueError("dest must contain at minimum and 'addr:port' format")
                addr,port = d.split(":")
                return addr,port
            def parse_byt(d):
                if b"://" in d:
                    _,d = d.split(b"://")
                if ":" not in d:
                    raise ValueError("dest must contain at minimum and 'addr:port' format")
                addr,port = d.split(b":")
                return addr,port

            if isinstance(dest,(str,bytes,list,tuple)):
                if isinstance(dest,(str,bytes)):
                    if isinstance(dest,str):
                        addr,port = parse_str(dest)
                    else:
                        addr,port = parse_byt(dest)
                    addr = [addr]
                    port = [port]
                elif isinstance(dest,tuple) and len(dest) == 2 and not (
                    (isinstance(dest[0],str) and ":" in dest) or
                    (isinstance(dest[0],bytes) and b":" in dest) or
                    isinstance(dest[0],list)):
                    addr = [dest[0]]
                    port = [dest[1]]
                elif isinstance(dest,tuple) and len(dest) == 2 and isinstance(dest[0],list):
                    addr = dest[0]
                    port = dest[1]
                elif isinstance(dest,(list,tuple)):
                    addr = []
                    port = []
                    for d in dest:
                        if isinstance(d,str):
                            a,p = parse_str(d)
                        else:
                            a,p = parse_byt(d)
                        addr.append(a)
                        port.append(p)
                else:
                    raise ValueError("Couldn't understand 'dest'")
                dests = [f"{self.protocol}://{a if isinstance(a,str) else a.decode()}:{p if isinstance(p,str) else p.decode()}".encode() for a,p in zip(addr,port)]
            elif self.sendpoint is not None:
                dests = ([x.encode() if isinstance(x,str) else x for x in self.sendpoint]
                         if isinstance(self.sendpoint,list) else 
                         [self.sendpoint.encode() if isinstance(self.sendpoint,str) else self.sendpoint])
            # else:
            #     raise RuntimeError("Destination address could not be inferred")
            # maybe still further down in the payload?
        # print(msg,dest,dests)
        
        # print(dest,tag,msg) # not it
        if isinstance(msg,str):
            payload = [msg.encode()]
        elif isinstance(msg,bytes):
            payload = [msg]
        else:
            def bytify(obj):
                if hasattr(obj,'encode'):
                    return obj.encode()
                elif hasattr(obj,'dumps'):
                    tmp = (b'',f'd:{obj.__class__.__name__}'.encode(),obj.dumps())
                    if not isinstance(tmp[-1],bytes):
                        tmp = tmp[:-1] + (tmp[-1].encode(),)
                    return tmp
                elif hasattr(obj,'to_bytes'):
                    return (b'',f'b:{obj.__class__.__name__}'.encode(),obj.to_bytes())
                else:
                    raise ValueError(f"Don't know how to get bytes from {type(obj)}")
            multimsg = False
            if isinstance(msg,(tuple,list)):
                payload = [x.encode() if hasattr(x,'encode') else x for x in msg]
                for idx in range(len(payload)):
                    if isinstance(payload[idx],ClientRequest):
                        p = msg.get_payload()
                        split_on = p.index(b"")
                        d = p[:split_on]
                        p = p[split_on+1:]
                        payload[idx] = (d,p)
                        if d:
                            multimsg = True
                    elif not isinstance(payload[idx],bytes):
                        payload[idx] = bytify(payload[idx])
            else:
                payload = bytify(payload)
            if multimsg:
                dests = True
        # print(msg,dest,dests)
        # print(dest,tag,msg) # not it
        if not dests:
            print(self._sock_type)
            raise RuntimeError("Destinations cannot be derived. ")
        # print(msg,dest,dests)
        if dests == True:
            send_msgs = []
            for dest,msg in payload:
                for x in dest:
                    send_msgs.append([x] + ([b''] if self._sock_type in [zmq.ROUTER] else []) + msg)
        elif dests:
            delim = [b''] if self._sock_type == zmq.ROUTER else (
                [] if self._sock_type != zmq.PUB else (
                    [(tag.encode() if isinstance(tag,str) else tag)] if tag else [b'']
                )
            )
            send_msgs = [[x] + delim + msg for x in dests]

        if self._n0:
            print(self.role,dest,dests,tag,send_msgs)
            self._n0 -= 1

        # print(dest,tag,send_msgs)
        if len(send_msgs) > 1:
            return self.__send_multi_msg(send_msgs)

        elif send_msgs:
            send_msg = send_msgs[0]
        else:
            return
        # print("send_msg:",send_msg)
        # print(msg,dest,dests)

        if isinstance(self._sock,zmq.Socket):
            if self._sock_type in [zmq.DGRAM,zmq.STREAM]:
                if send_msg and send_msg[0] == self.sendpoint:
                    # print("Send point A",send_msg)
                    self._sock.send_multipart(send_msg)
                else:
                    # print("Send point A",[f'{self.sendpoint.decode()}'.encode()]+send_msg)
                    self._sock.send_multipart([f'{self.sendpoint.decode()}'.encode()]+send_msg)
            else:
                # print(send_msg)
                if len(send_msg) > 1:
                    # # print("Send point B",len(send_msg),[len(x) for x in send_msg]) #### pub should always be here, same with router
                    # for x in send_msg:
                    #     if len(x) < 100:
                    #         print(x, end=' | ')
                    # print()
                    self._sock.send_multipart(send_msg)
                else:
                    # print("Send point C",send_msg[0])
                    self._sock.send(send_msg[0])
        else:
            # print("Send point D++",len(send_msg),len(send_msg[1]))
            self._sock.sendto(send_msg[1],self.sendpoint)

    def __send_multi_msg(self,msg_list):
        if not isinstance(self._sock,zmq.Socket):
            print("Send point G",len(msg_list))
            raise ValueError("Got here without being zmq")
        ### assumed zmq for this
        # print(msg_list)
        for msg in msg_list:
            if len(msg) > 1:
                print("Send point D--",len(msg))
                print(msg)
                self._sock.send_multipart(msg)
            else:
                print("Send point F",len(msg))
                self._sock.send(msg[0])

    def recv(self,timeout:int=10,tag:str=None,_raw=True):
        # print('timeout =',timeout)
        socks = zmq_poll([(self._sock,zmq.POLLIN)],timeout=timeout)
        handler = MessageWrapper()
        sender = None
        if self._sock in socks or self._sock.fileno() in socks:
            if isinstance(self._sock,zmq.Socket):
                payload = self._sock.recv_multipart()
                # print("raw recv:",payload)
                if self.role & ConnectionRole.MCST:
                    payload = payload[1:]
                if self._sock.socket_type == zmq.ROUTER:
                    sender = payload[0]
                    payload = payload[1:]
                if not _raw:
                    for chunk in payload:
                        handler.parse(chunk)
                    if not handler.ready:
                        print("....")
                    payload = handler.get()
                    payload = [payload] if not isinstance(payload,list) else payload
                payload = ([sender] if sender is not None else []) + payload
                payload = payload if len(payload) > 1 else payload[0]
            elif isinstance(self._sock,socket.socket):
                payload = self._sock.recv(9000)
            return payload
        return None

    def recv_all(self,timeout:int=10,tag:str=None,count:int=0,_raw=True):
        payloads = []
        if isinstance(self._sock, zmq.Socket):
            payload = self.recv(timeout=timeout,tag=tag,_raw=_raw)
            while payload is not None:
                payloads.append(payload)
                payload = self.recv(timeout=timeout,tag=tag,_raw=_raw)
        elif isinstance(self._sock, socket.socket):
            payload = self.recv(timeout=timeout,tag=tag,_raw=_raw)
            while payload is not None:
                payloads.append(payload)
                payload = self.recv(timeout=0,tag=tag,_raw=_raw)
        return payloads

    def close(self):
        if self._sock is not None:
            self._sock.close()
            self._sock = None
        if self._ctx is not None and self._ctx_owner:
            self._ctx.term()

    def fileno(self):
        return -1 if self._sock is None else self._sock.fileno()

