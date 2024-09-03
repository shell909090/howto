#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2012-04-11
@author: shell.xu
'''
import sys
import random


def main():
    with open(sys.argv[1], 'w') as fo:
        for i in range(1000000):
            fo.write('%d %d\n' % (i, random.randint(0, 10000)))


if __name__ == '__main__':
    main()
