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

    for _ in range(100):
        msg = random.randint(0, 1000)
        queue_name = random.choice(['orange', 'bule', 'black', 'red'])
        channel.basic_publish(exchange='amq.direct',
                              routing_key=queue_name,
                              body=str(msg))
        print(f"[x] Sent '{msg}' to '{queue_name}'")

    connection.close()


if __name__ == '__main__':
    main()
