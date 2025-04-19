
from .system_header import *
import time
from typing import List,Tuple,Dict,Union,Any



class BetterThread(threading.Thread):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._external_stop_ = threading.Event()
        self._external_stop_.clear()
        self._ack_stop_ = threading.Event()
        self._ack_stop_.clear()
        self._ack_start_ = threading.Event()
        self._ack_start_.clear()
        self._better_stop_reason_ = None
        target = kwargs['target']
        if callable(target) and hasattr(target,'__qualname__'):
            self._tgt_name = target.__qualname__
        elif callable(target) and hasattr(target,'__name__'):
            self._tgt_name = target.__name__
        else:
            self._tgt_name = "?"

    def __str__(self):
        state = ((int(self._ack_start_.is_set()) << 0)
                +(int(self._ack_stop_.is_set()) << 1)
                +(int(self._external_stop_.is_set() << 2)))
        if state == 0:
            state = "Pending"
        elif state == 1:
            state = "Running"
        elif state in [2,3]:
            state = "Finished"
        elif state in [4,5]:
            state = 'Stopping'
        elif state in [6,7]:
            state = 'Stopped'
        out = f"<BetterThread: {state}, name: {self._name}, target: {self._tgt_name}>"
        return out
    
    def __repr__(self):
        return str(self)

    def stop(self,reason:str=None):
        if not self._external_stop_.is_set():
            self._external_stop_.set()
        if reason is not None:
            if self._better_stop_reason_:
                self._better_stop_reason_ = "\n".join([self._better_stop_reason_,reason])
            else:
                self._better_stop_reason_ = reason

    def check_for_stop(self):
        return self._external_stop_.is_set()

    def _stopped(self):
        self._ack_stop_.set()
    
    def is_stopped(self):
        return self._ack_stop_.is_set()

    def wait(self,timeout:Union[int,float]=None):
        wait_at = time.time()
        if timeout is None:
            continue_loop = lambda : True
        else:
            continue_loop = lambda : time.time() - wait_at < timeout
        while (continue_loop()):
            if not self.is_alive():
                self._stopped()
                return True
        return False

    def join(self):
        super().join()
        if not self._ack_stop_.is_set():
            self._stopped()

    def start(self):
        self._ack_start_.set()
        super().start()

    def run(self):
        self._ack_start_.set()
        super().run()
        self._stopped()

    @property
    def reason(self):
        if self.is_alive():
            return None
        return self._better_stop_reason_
