from rpc.message import Message
from asyncio import Lock


class LogicalTime(object):
    def __init__(self):
        self.time = 0

    def local_event(self):
        self.time += 1

    def remote_event(self, time):
        self.time = max(self.time, time) + 1


class LamportMutex(object):
    def __init__(self, rpc):
        self.rpc = rpc
        self.requests = []
        self.request_made = False
        self.pending_replies = []
        self.localtime = LogicalTime()
        self.lock = Lock()

    def receive(self, msg):
        self.localtime.remote_event(msg.time)

        if msg.type == Message.REQUEST:
            self._send_message(msg.from_, Message.REPLY)

        elif msg.type == Message.RELEASE:
            self._release(msg)

        elif msg.type == Message.REPLY:
            self._reply(msg)

    def acquire(self):
        if not self.request_made:
            self.request_made = True
            self.pending_replies = self.rpc.other_pids[:]
            self._multicast(Message.REQUEST)

        if self.requests and self.requests[0].from_ == self.rpc.pid:
            if len(self.pending_replies) == 0:
                return True

        return False

    def release(self):
        self._release()
        self._multicast(Message.RELEASE)

    def _release(self, msg=None):
        if msg is None:
            self.request_made = False
            self.requests.pop(0)
            return

        if self.requests and self.requests[0].from_ == msg.from_:
            self.requests.pop(0)

    def _reply(self, msg=None):
        if self.request_made:
            self.pending_replies.pop(0)

    def _queue_extend(self, msg):
        self.requests.append(msg)
        self.requests.sort()

    def _send_message(self, receiver, _type):
        if _type == Message.REPLY:
            self.localtime.local_event()

        msg = Message(to=receiver,
                      from_=self.rpc.pid,
                      time=self.localtime.time,
                      type=_type)

        if receiver == self.rpc.pid and _type == Message.REQUEST:
            self._queue_extend(msg)
        else:
            self.rpc.send_message(msg)

    def _multicast(self, _type):
        self.localtime.local_event()

        if _type == Message.REQUEST:
            self._send_message(self.rpc.pid,  _type)

        for pid in self.rpc.other_pids:
            self._send_message(pid, _type)
