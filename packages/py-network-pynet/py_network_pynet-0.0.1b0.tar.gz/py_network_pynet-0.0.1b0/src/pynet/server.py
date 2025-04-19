
from .system_header import *
from . import (
    ConnectionRole as CR,
    BetterConnection as BC,
    BetterProcess as BP,
    BetterThread as BT
)
from .better_connection import zmq_poll
import os,time
from queue import deque

PING = b'__ping__'
PONG = b'__pong__'

class ServerRole(IntFlag):
    MAIN=0 # Main process/thread
    CHDT=1 # Main process : thread
    CHDP=2 # Child process


class ServerConnection(BC):
    def __init__(self,
            endpoint:str='127.115.97.105:0',
            _ctx:zmq.Context=None):
        if '://' in endpoint:
            _,endpoint = endpoint.split("://")
        addr,port = endpoint.split(':')
        super(ServerConnection,self).__init__(
            CR.TCP_ | CR.SEND | CR.RECV | CR.BIND,
            addr,
            port,
            _ctx
        )

class ServerNetworking(object):
    def __init__(self,
            endpoint:str,
            using="proc",
            _ctx:zmq.Context=None):
        self.endpoints = endpoint
        self.mode = int(using=="thread")
        self._ctx = _ctx
        self._task_callback = None
        self.listener = None
        self._pid = os.getpid()
        self.reset()

    def set_callback(self,fcn):
        if not callable(fcn):
            raise ValueError("callback must be callable")
        self._task_callback = fcn

    def reset(self):
        if self.listener is not None:
            self.stop()
            self.wait()
        self._ping = False
        self.state_map = dict()
        self.task_map = dict()
        self.reply_map = dict()
        self._mpipe, self._cpipe, self._mcond, self._ccond, self._lthread = [None,]*5
        self._fcn = ServerRole.MAIN

    def stop(self,reason:str=None):
        if self.listener is not None:
            self.listener.stop(reason)
        if self._lthread is not None:
            self._lthread.stop()
    def disconnect(self):
        self.stop()
    def close(self):
        self.stop()

    def start(self):
        if self.listener is not None:
            return
        if self.mode == 0:
            # multi-process
            self._mpipe,self._cpipe = mp.Pipe()
            self._mcond,self._ccond = mp.Condition(),mp.Condition()
        self.listener = [BP,BT][self.mode](target=self._interface)
        self.listener.start()
        if self.mode == 0:
            response = self._mpipe.recv()
            self.endpoint = response['endpoint']
            self._lthread = BT(target=self._monitor_pipe)
            self._lthread.start()
    def connect(self):
        self.start()


    def _interface(self):
        self._fcn = ServerRole.CHDT if self.mode else ServerRole.CHDP
        connection = ServerConnection(self.endpoints,None if not self.mode else self._ctx)
        connection.connect()
        self.endpoint = connection.endpoint
        if not self.mode:
            self._cpipe.send({'endpoint':self.endpoint})

        ####################
        ## DEBUG
        ####################
        debug_timeout = 30.0
        ticks = 0
        last = time.time()

        while not self.listener.check_for_stop():
            if not self.mode:
                if self._cpipe.poll(0.001):
                    incoming = self._cpipe.recv()
                    # print("incoming",incoming)
                    if not isinstance(incoming,dict):
                        continue
                    if 'ping' in incoming:
                        self._ping = incoming['ping']
                    elif 'sid' in incoming:
                        sid = incoming['sid']
                        if 'reply' in incoming:
                            priority = incoming['priority']
                            msg = incoming['reply']
                        if 'send' in incoming:
                            msg = incoming['send']
                            priority = 0
                        self._reply(sid,msg,priority)
                    if 'debug' in incoming:
                        print("state:",self.state_map)
                        print("task:",self.task_map)
                        print("reply:",self.reply_map)

            if self._ping:
                for k,d_q in self.reply_map.items():
                    if d_q and d_q[0] == PING:
                        continue
                    while PING in d_q:
                        d_q.remove(PING)
                    d_q.insert(0,PING)
                    self.state_map[k] = 16
                    if not self.mode:
                        self._cpipe.send({"state_change":16,"sid":k})
                        with self._mcond:
                            self._mcond.notify()
                self._ping = False
            
            socks = dict(zmq_poll([(connection,zmq.POLLIN | zmq.POLLOUT)], 10))
            ticks += (1 if len(self.state_map) else 0)
            if time.time() - last > debug_timeout:
                # print(socks,ticks)
                if ticks > 200000:
                    print("CONNECTION LOST")
                    if not self.mode:
                        for k in self.state_map.keys():
                            self._cpipe.send({"state_change":0,"sid":k})
                            with self._mcond:
                                self._mcond.notify()

                self._ping = True
                last = time.time()

            ##### send anything ready
            if connection in socks and socks[connection] & zmq.POLLOUT:
                for sid,d_q in self.reply_map.items():
                    if d_q:
                        msg = d_q.popleft()
                        payload = [sid,b'']
                        if isinstance(msg,list):
                            payload.extend(msg)
                        else:
                            payload.append(msg)
                        connection.send(payload)
            ##### recv anything ready
            payload_set = list()
            if connection in socks and socks[connection] & zmq.POLLIN:
                last = time.time()
                ticks = 0
                payload_set = connection.recv_all()
                # print("RECV:",payload_set)
            for payload in payload_set:
                if len(payload) > 2:
                    if payload[1] == b'':
                        sid,msg = payload[0],payload[2:]
                        if sid not in self.state_map:
                            if not self.mode:
                                self._cpipe.send({'new_sid':sid})
                                with self._mcond:
                                    self._mcond.notify()
                            self._add_new_sid(sid)
                        if len(msg) == 1 and msg[0]==PING:
                            self.reply(sid,PONG,1)
                            # print("____pinged____")
                        elif len(msg) == 1 and msg[0]==PONG:
                            self.state_map[sid] = 1
                            if not self.mode:
                                self._cpipe.send({"state_change":1,"sid":sid})
                                with self._mcond:
                                    self._mcond.notify()
                            # print("____ponged____")
                        else:
                            if not self.mode:
                                self._cpipe.send({'task':msg,'sid':sid})
                                with self._mcond:
                                    self._mcond.notify()
                            elif callable(self._task_callback):
                                self._task_callback((sid,msg))
                            else:
                                self.task_map[sid].append(msg)
                    else:
                        print("hmm,separator not found",payload[:2])
                else:
                    print("hmm, message structure is too short:",payload)
        else:
            connection.close()
            self.endpoint = None
            if self._cpipe is not None and not self._cpipe.closed:
                try:
                    self._cpipe.close()
                except:
                    pass

    def _add_new_sid(self,sid):
        if sid in self.state_map:
            return
        self.state_map[sid] = 0
        self.task_map[sid] = deque()
        self.reply_map[sid] = deque()

    def _monitor_pipe(self):
        if os.getpid() != self._pid:
            print("only works in object process")
            return
        if self.mode:
            print("only works in process mode")
            return
        while self._lthread is not None and not self._lthread.check_for_stop():
            with self._mcond:
                if self._mcond.wait(0.1) or (self._mpipe is not None and self._mpipe.poll(0)):
                    payload = self._mpipe.recv()
                    # print(payload)
                    try:
                        if 'clear' in payload:
                            if 'error' in payload:
                                print(payload['error'])
                            if payload['clear'] in self.reply_map:
                                if payload['clear'] is True:
                                    for d_q in self.reply_map.values():
                                        d_q.clear()
                                else:
                                    d_q = self.reply_map[payload['clear']]
                                    if "msg" in payload:
                                        if payload["msg"] in d_q:
                                            clear_idx = d_q.index(msg)
                                            del d_q[clear_idx]
                                        else:
                                            print("msg not found in clear request")
                                    else:
                                        d_q.clear()
                            continue
                        if 'state_change' in payload:
                            self.state_map[payload['sid']] = payload['state_change']
                            continue
                        if 'new_sid' in payload:
                            self._add_new_sid(payload['new_sid'])
                            continue
                        if 'task' in payload:
                            sid = payload['sid']
                            msg = payload['task']
                            if callable(self._task_callback):
                                self._task_callback((sid,msg))
                            else:
                                self.task_map[sid].append(msg)
                    except:
                        import traceback
                        traceback.print_exc()
                        print("failed:",payload)



    def wait(self):
        if self.listener is not None:
            self.listener.wait()
            self.listener = None

    def ping(self):
        if self._mpipe is not None:
            self._mpipe.send({'ping':True})
        else:
            self._ping = True
        time.sleep(0.1)

    def send(self,msg:Union[str,bytes]):
        for ep in list(self.state_map):
            self.reply_map[ep].append(msg)
            if not self.mode:
                self._mpipe.send({"send":msg,"sid":ep})

    def reply(self,sid,msg,priority=0):
        if self.mode:
            self._reply(sid,msg,priority)
        if sid not in self.reply_map:
            return
        else:
            self._mpipe.send({"reply":msg,"sid":sid,"priority":priority})

    def _reply(self,sid,msg,priority=0):
        if sid not in self.reply_map:
            return
        if priority == 1:
            self.reply_map[sid].insert(0,msg)
        else:
            self.reply_map[sid].append(msg)