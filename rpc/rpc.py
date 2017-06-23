import socket
from threading import Thread

from rpc.message import Message


class LamportListenerThread(Thread):
    def __init__(self, lamport_mutex, port):
        def task():
            sock = socket.socket()
            sock.bind(("", port))
            sock.listen(20)
            while True:
                conn, addr = sock.accept()
                length = int.from_bytes(conn.recv(4), 'big')
                msg = Message(conn.recv(length))
                lamport_mutex.deliver_message(msg)
        super().__init__(target=task)


class LocalRPC(object):
    def __init__(self, node_reference, table):
        self.node_reference = node_reference
        self.table = table
        self.other_pids = []
        for pid in self.table.keys():
            if pid != self.pid:
                self.other_pids.append(pid)

    def run_listener(self):
        pass

    def send_message(self, msg):
        self.table[msg.to].mutex.deliver_message(msg)

    @property
    def pid(self):
        return self.node_reference.pid


class NetworkRPC(LocalRPC):
    def __init__(self, node_reference, table):
        super().__init__(node_reference, table)
        self.port = table[self.pid][1]

    def run_listener(self):
        listener = LamportListenerThread(self.node_reference.mutex,  self.port)
        listener.start()

    def send_message(self, msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(self.table[msg.to])
            data = msg.dump()
            data = len(data).to_bytes(4, 'big') + data
            sock.send(data)
        except ConnectionRefusedError as e:
            print(e)
        finally:
            sock.close()
