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


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    print("[x] Create an exchange 'logs'")

    for _ in range(100):
        msg = random.randint(0, 1000)
        channel.basic_publish(exchange='logs',
                              routing_key='',
                              body=str(msg))
        print(f"[x] Sent '{msg}'")

    connection.close()


if __name__ == '__main__':
    main()
