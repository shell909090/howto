#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@date: 2022-04-07
@author: Shell.Xu
@copyright: 2022, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
import sys
import logging
from os import path
sys.path.append(path.abspath(path.join(path.dirname(__file__), '../proto/')))

import grpc
import iface_pb2 as pb2
import iface_pb2_grpc as pb2_grpc


def proc_add(ch):
    c = pb2_grpc.AddStub(ch)
    req = pb2.AddRequest(a=10, b=20)
    logging.info(f'rpc add call, A: {req.a}, B: {req.b}')
    resp = c.Add(req)
    logging.info(f'rpc add return, N: {resp.n}')


def proc_sum(ch):
    c = pb2_grpc.AddStub(ch)
    def data():
        for i in range(20, 30):
            logging.info(f'rpc sum stream send, N: {i}')
            yield pb2.SumRequest(n=i)
    logging.info('rpc sum call')
    resp = c.Sum(data())
    logging.info(f'rpc sum return, N: {resp.n}')


def proc_range(ch):
    c = pb2_grpc.RangeStub(ch)
    req = pb2.RangeRequest(n=10, len=10)
    logging.info(f'rpc range call, N: {req.n}')
    for resp in c.Range(req):
        logging.info(f'rpc range stream recv, N: {resp.n}')
    logging.info('rpc range end')


def proc_echo(ch):
    c = pb2_grpc.EchoStub(ch)
    def data():
        for i in range(10, 100, 10):
            logging.info(f'rpc echo stream send, N: {i}, S: {i}')
            yield pb2.EchoRequest(n=i, s=str(i))
    logging.info('rpc echo call')
    for resp in c.Echo(data()):
        logging.info(f'rpc echo stream recv, N: {resp.n}, S: {resp.s}')
    logging.info('rpc echo end')


def main():
    logging.basicConfig(level=logging.INFO)
    ch = grpc.insecure_channel(sys.argv[1])
    if sys.argv[2] == 'add':
        proc_add(ch)
    elif sys.argv[2] == 'sum':
        proc_sum(ch)
    elif sys.argv[2] == 'range':
        proc_range(ch)
    elif sys.argv[2] == 'echo':
        proc_echo(ch)


if __name__ == '__main__':
    main()
