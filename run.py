import argparse
import glob
import os

from multiprocessing import Process as T
from threading import Thread

import time

from node import Node

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="path to configuration file")
    parser.add_argument("-m", help="Manual mode", action='store_true')
    parser.add_argument("-p", type=int, default=0, help="Manual mode node id, starting from 0")
    parser.add_argument("-n", type=int, default=10, help="Number of nodes")

    args = parser.parse_args()

    for file in glob.glob('logs/*.log'):
        os.remove(file)

    if args.m:
        n = Node(args.p, args.config)
        t = T(target=n.run, args=(True, ))
        time.sleep(1)
        t.start()
        t.join()
    else:
        procs = []

        def callsome(i):
            n = Node(i, args.config, None)
            n.run()

        for i in range(args.n):
            t = T(target=callsome, args=(i,))
            procs.append(t)

        time.sleep(1)
        print('To stop press Ctrl+C.')
        for i, t in enumerate(procs):
            print('Starting %i proc' % i)
            t.start()

        for t in procs:
            t.join()
