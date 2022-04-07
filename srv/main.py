#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@date: 2022-04-07
@author: Shell.Xu
@copyright: 2022, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
import sys
import time
import logging
from os import path
sys.path.append(path.abspath(path.join(path.dirname(__file__), '../proto/')))

import grpc
from concurrent import futures
import iface_pb2 as pb2
import iface_pb2_grpc as pb2_grpc


class Service(object):

    def Add(self, req, ctx):
        logging.info(f'rpc add in, A: {req.a}, B: {req.b}')
        resp = pb2.AddResponse(n=req.a+req.b)
        logging.info(f'rpc add out, N: {resp.n}')
        return resp

    def Sum(self, reqiter, ctx):
        logging.info('rpc sum in')
        s = 0
        for req in reqiter:
            s += req.n
            logging.info(f'rpc sum stream recv, N: {req.n}')
        resp = pb2.SumResponse(n=s)
        logging.info(f'rpc sum out, N: {resp.n}')
        return resp

    def Range(self, req, ctx):
        logging.info(f'rpc range in, N: {req.n}, len: {req.len}')
        for i in range(req.n, req.n+req.len):
            logging.info(f'rpc range stream send, N: {i}')
            yield pb2.RangeResponse(n=i)
        logging.info('rpc range end')
        return

    def Echo(self, reqiter, ctx):
        logging.info('rpc echo in')
        for req in reqiter:
            logging.info(f'rpc echo stream recved, N: {req.n}, S: {req.s}')
            resp = pb2.EchoResponse(n=req.n+1, s=req.s+'python')
            logging.info(f'rpc echo stream sent, N: {resp.n}, S: {resp.s}')
            yield resp
        logging.info('rpc echo end')
        return


def main():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    svc = Service()
    pb2_grpc.add_AddServicer_to_server(svc, server)
    pb2_grpc.add_RangeServicer_to_server(svc, server)
    pb2_grpc.add_EchoServicer_to_server(svc, server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
