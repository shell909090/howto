#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2012-10-26
@author: shell.xu
'''
import sys
import time

# from memory_profiler import profile


# @profile
def main():
    time.sleep(1)

    # import tracemalloc
    # tracemalloc.start()
    # ss1 = tracemalloc.take_snapshot()

    with open(sys.argv[1]) as fi:
        l = []
        for line in fi:
            t = line.strip().split()
            t = tuple(map(int, t))
            l.append(t)
        l = sorted(l, key=lambda x: x[1])

    # ss2 = tracemalloc.take_snapshot()
    # top_stats = ss2.compare_to(ss1, 'lineno')
    # print("[ Top 10 differences ]")
    # for stat in top_stats[:10]:
    #     print(stat)

    time.sleep(10)


if __name__ == '__main__':
    main()
