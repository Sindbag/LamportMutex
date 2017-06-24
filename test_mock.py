import unittest

from lamportmutex import LamportMutex
from rpc import LocalRPC


class MockNode(object):
    def __init__(self, pid):
        self.pid = pid


class LamportTestCase(unittest.TestCase):
    def test_single_acquire(self):
        node = MockNode(0)
        table = {0: node}
        rpc = LocalRPC(node, table)
        mutex = LamportMutex(rpc)

        self.assertTrue(mutex.acquire())
        self.assertEqual(mutex.request_made, True)
        self.assertEqual(mutex.localtime.time, 1)

    def test_single_release(self):
        node = MockNode(0)
        table = {0: node}
        rpc = LocalRPC(node, table)
        mutex = LamportMutex(rpc)
        mutex.requests.append('mock')

        mutex.release()

        self.assertEqual(mutex.request_made, False)
        self.assertEqual(mutex.requests, [])
        self.assertEqual(mutex.localtime.time, 1)

    def test_single_acquire_release(self):
        node = MockNode(0)
        table = {0: node}
        rpc = LocalRPC(node, table)
        mutex = LamportMutex(rpc)

        mutex.acquire()
        mutex.release()

        self.assertEqual(mutex.request_made, False)
        self.assertEqual(mutex.requests, [])
        self.assertEqual(mutex.localtime.time, 2)

    def test_multi(self):
        n0, n1 = MockNode(0), MockNode(1)
        table = {0: n0, 1: n1}
        rpc1, rpc2 = LocalRPC(n0, table), LocalRPC(n1, table)
        mutex1, mutex2 = LamportMutex(rpc1), LamportMutex(rpc2)
        n0.mutex, n1.mutex = mutex1, mutex2

        self.assertTrue(mutex1.acquire())
        self.assertEqual(mutex1.requests[0].from_, 0) # request from 0
        self.assertEqual(mutex2.requests[0].from_, 0)
        self.assertFalse(mutex2.acquire())
        mutex1.release()

        self.assertEqual(mutex1.requests[0].from_, 1) # request from 1 is in queue
        self.assertEqual(mutex2.requests[0].from_, 1)

        self.assertTrue(mutex2.acquire())
        mutex2.release()
        self.assertEqual(mutex1.requests, [])
