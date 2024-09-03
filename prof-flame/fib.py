#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2024-08-26
@author: Shell.Xu
@copyright: 2024, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''


def memorized(f):
    cached = {}
    def _(n):
        if n not in cached:
            cached[n] = f(n)
        return cached[n]
    return _


# @memorized
def fib(n):
    if n <= 0:
        return 0
    elif n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def main():
    print(fib(35))


# def main():
#     import cProfile
#     pr = cProfile.Profile()
#     pr.enable()
#     print(fib(35))
#     pr.disable()
#     pr.dump_stats('fib.prof')


if __name__ == '__main__':
    main()
