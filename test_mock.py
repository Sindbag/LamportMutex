import unittest

from lamportmutex import LamportMutex
from rpc import LocalRPC


class MockNode(object):
    def __init__(self, pid):
        self.pid = pid


class LamportTestCase(unittest.TestCase):
    def test_single(self):
        n = MockNode(0)
        table = {0: n}
        rpc = LocalRPC(n, table)
        mutex = LamportMutex(rpc)

        self.assertTrue(mutex.request_crit_section())
        mutex.release_request()

    def test_multi(self):
        n1, n2  = MockNode(0), MockNode(0)
        table = {}
        rpc1, rpc2 = LocalRPC(n1, table), LocalRPC(n2, table)
        mutex1, mutex2 = LamportMutex(rpc1), LamportMutex(rpc2)

        self.assertTrue(mutex1.request_crit_section())
        mutex1.release_request()

        self.assertTrue(mutex2.request_crit_section())
        mutex2.release_request()
