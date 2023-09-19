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


class Consumer(object):

    def __init__(self, param, queue_name, routing_key):
        self.param = param
        self.queue_name = queue_name
        self.routing_key = routing_key

    def loop(self):
        self.conn = pika.BlockingConnection(self.param)
        self.chan = self.conn.channel()

        result = self.chan.queue_declare(queue=self.queue_name, exclusive=True)
        self.chan.queue_bind(exchange='amq.topic', queue=self.queue_name, routing_key=self.routing_key)
        self.chan.basic_qos(prefetch_count=1)

        self.chan.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        print(f'[*] {gevent.getcurrent().minimal_ident} Waiting for messages in queue {self.queue_name}. To exit press CTRL+C')
        self.chan.start_consuming()

        self.conn.close()

    def callback(self, ch, method, properties, body):
        print(f"[x] {gevent.getcurrent().minimal_ident} Received {body} in queue {self.queue_name}")
        msg = int(body)
        time.sleep((msg+random.randint(0, 1000))/1000)
        print(f"[x] {body} done")
        ch.basic_ack(delivery_tag=method.delivery_tag)


# # recver tree
# def main():
#     p = pool.Pool(10)
#     p.spawn(Consumer(pika.ConnectionParameters('localhost'), 'a', 'a.#').loop)
#     p.spawn(Consumer(pika.ConnectionParameters('localhost'), 'a.b', 'a.b.#').loop)
#     p.spawn(Consumer(pika.ConnectionParameters('localhost'), 'f', 'f.#').loop)
#     p.join()


# recver tag
def main():
    p = pool.Pool(10)
    for x in 'abcdefgh':
        p.spawn(Consumer(pika.ConnectionParameters('localhost'), x, f'#.{x}.#').loop)
    p.join()


if __name__ == '__main__':
    main()
