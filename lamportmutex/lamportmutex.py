from rpc.message import Message


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
        self.requestList = []
        self.request_made = False
        self.pending_replies = []
        self.localtime = LogicalTime()

    def deliver_message(self, msg):
        self.localtime.remote_event(msg.time)

        if msg.type == Message.REQUEST:
            self._send_message(msg.from_, Message.REPLY)

        elif msg.type == Message.RELEASE:
            self._release_request(msg)

        elif msg.type == Message.REPLY:
            self._reply_request(msg)

    def release_request(self):
        self._release_request()
        self._multicast(Message.RELEASE)

    def request_crit_section(self):
        if not self.request_made:
            self.request_made = True
            self.pending_replies = self.rpc.other_pids[:]
            self._multicast(Message.REQUEST)

        if self.requestList and self.requestList[0].from_ == self.rpc.pid:
            if len(self.pending_replies) == 0:
                return True

        return False

    def _release_request(self, msg=None):
        if msg is None:
            self.request_made = False
            self.requestList = self.requestList[1:]
            return

        if self.requestList and self.requestList[0].from_ == msg.from_:
            self.requestList = self.requestList[1:]

    def _reply_request(self, msg=None):
        if self.request_made:
            self.pending_replies.pop()

    def _queue_request(self, msg):
        self.requestList.append(msg)
        self.requestList.sort()

    def _send_message(self, receiver, type):
        if type == Message.REPLY:
            self.localtime.local_event()

        msg = Message(to=receiver,
                      from_=self.rpc.pid,
                      time=self.localtime.time,
                      type=type)

        if receiver == self.rpc.pid and type == Message.REQUEST:
            self._queue_request(msg)
        else:
            self.rpc.send_message(msg)

    def _multicast(self, type):
        self.localtime.local_event()

        if type == Message.REQUEST:
            self._send_message(self.rpc.pid,  type)

        for pid in self.rpc.other_pids:
            self._send_message(pid, type)
