import random
import time
import fcntl

from lamportmutex import LamportMutex
from rpc import NetworkRPC


def router_table(file):
    table = {}
    with open(file) as f:
        for i, line in enumerate(f):
            ip, port = line.split()
            table[i] = (ip, int(port))
    return table


class Node(object):
    def __init__(self, pid, configpath, times=None):
        self.pid = pid
        self.times = times
        self.rpc = NetworkRPC(self, router_table(configpath))
        self.mutex = LamportMutex(self.rpc)
        self.rpc.run_listener()
        self.log_filepath = "logs/%d.log" % self.pid

    def execute_critical(self, logictime):
        with open('logs/common.txt', 'a') as f:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                f.write("{} {} {}\n".format(self.pid, logictime, self.mutex.localtime.time))
            except IOError as e:
                print(e)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def log_local(self, action):
        with open(self.log_filepath, 'a') as f:
            f.write("%s %.5f %5d %d\n" % (action, time.time(), self.mutex.localtime.time, self.pid))

    def run(self, manual=False):
        time.sleep(5)
        while True:
            if manual:
                input("Acquire")

            self.log_local('request')
            while not self.mutex.acquire():
                self.log_local('request')
                time.sleep(random.uniform(1, 5))

            print("acquire", self.pid)
            logtime = self.mutex.localtime.time
            self.log_local('acquire')

            self.execute_critical(logtime)

            if manual:
                input('Release')

            self.mutex.release()
            self.log_local('release')

            if self.times is not None:
                self.times -= 1
                if self.times <= 0:
                    break
