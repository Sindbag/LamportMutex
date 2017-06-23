import argparse
import glob
import os
import threading

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
        t = threading.Thread(target=n.run, args=(True, ))
        time.sleep(1)
        t.start()
        t.join()
    else:
        threads = []
        for i in range(args.n):
            n = Node(i, args.config)
            t = threading.Thread(target=n.run)
            threads.append(t)

        time.sleep(1)
        for t in threads:
            t.start()

        for t in threads:
            t.join()
