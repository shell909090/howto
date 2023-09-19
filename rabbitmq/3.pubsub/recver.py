#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2023-09-18
@author: Shell.Xu
@copyright: 2023, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
from gevent import monkey
monkey.patch_all()

import time
import random

import pika
import gevent
from gevent import pool


def callback(ch, method, properties, body):
    print(f"[x] {gevent.getcurrent().minimal_ident} Received {body}")
    msg = int(body)
    time.sleep((msg+random.randint(0, 1000))/1000)
    print(f"[x] {body} done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='logs', queue=queue_name)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback)
    print(f'[*] {gevent.getcurrent().minimal_ident} Waiting for messages in queue {queue_name}. To exit press CTRL+C')
    channel.start_consuming()

    connection.close()


def main():
    p = pool.Pool(10)
    for _ in range(10):
        p.spawn(consumer)
    p.join()


if __name__ == '__main__':
    main()
