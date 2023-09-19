#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2023-09-18
@author: Shell.Xu
@copyright: 2023, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
import random

import pika


TREE = [
    'a',
    'a.b',
    'a.b.c',
    'a.d',
    'a.d.e',
    'f',
    'f.g',
    'f.g.h'
]


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    for _ in range(10):
        msg = random.randint(0, 1000)
        queue_name = random.choice(TREE)
        channel.basic_publish(exchange='amq.topic',
                              routing_key=queue_name,
                              body=str(msg))
        print(f"[x] Sent '{msg}' to '{queue_name}'")

    connection.close()


if __name__ == '__main__':
    main()
