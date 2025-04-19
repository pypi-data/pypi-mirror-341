
from .system_header import *
import traceback
import signal
import time
import os

class BP_STOP(Exception):
    pass

class BetterProcess(mp.Process):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._external_stop_ = mp.Event()
        self._external_stop_.clear()
        self._ack_stop_ = mp.Event()
        self._ack_stop_.clear()
        self._ack_start_ = mp.Event()
        self._ack_start_.clear()
        self._parent_pipe_,self._child_pipe_ = mp.Pipe()
        self._better_stop_reason_ = None
        self._child_exception_ = None
        self._child_pid_ = None
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
        out = f"<BetterProcess: {state}, name: {self._name}, target: {self._tgt_name}>"
        return out
    
    def __repr__(self):
        return str(self)


    def stop(self,reason:str=None):
        if not self._external_stop_.is_set():
            self._external_stop_.set()
            if hasattr(signal,"pidfd_send_signal"):
                signal.pidfd_send_signal(os.pidfd_open(self._child_pid_),signal.SIGUSR1)
            else:
                import subprocess,shlex
                command = f'/usr/bin/bash -c "kill -n 10 {str(self._child_pid_)}"'
                proc = subprocess.Popen(shlex.split(command))
                while proc.poll() is None:
                    time.sleep(0.01)
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

    def wait(self,timeout=None):
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

    def start(self):
        if self._ack_start_.is_set():
            return
        self._ack_start_.set()
        super().start()
        self._child_pid_ = self._parent_pipe_.recv()
        if not isinstance(self._child_pid_,int):
            self._child_exception_ = self._child_pid_
            self._child_pid_ = None

    def run(self):
        def handler(sig,frame):
            raise BP_STOP
        signal.signal(signal.SIGUSR1,handler)
        try:
            self._child_pipe_.send(os.getpid())
            mp.Process.run(self)
            self._child_pipe_.send(None)
        except BP_STOP:
            self._child_pipe_.send("stop caught")
        except Exception as e:
            tb = traceback.format_exc()
            self._child_pipe_.send((e,tb))
            raise
        finally:
            self._stopped()

    @property
    def exception(self):
        if self._parent_pipe_.poll():
            self._child_exception_ = self._parent_pipe_.recv()
        return self._child_exception_

    def close(self):
        self.stop()
        self.wait()
        self.join()

    @property
    def reason(self):
        if self.is_alive():
            return None
        return self._better_stop_reason_
