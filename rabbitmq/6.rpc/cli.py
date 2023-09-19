#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2023-09-19
@author: Shell.Xu
@copyright: 2023, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
import uuid

import pika


def rpc_call(connection, channel, exchange, routing_key, body):
    corr_id = str(uuid.uuid4())
    response = None
    def on_response(ch, method, props, body):
        nonlocal response
        if corr_id == props.correlation_id:
            response = body

    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue
    channel.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True)

    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=corr_id),
        body=body)
    connection.process_data_events(time_limit=None)

    return response



def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    response = rpc_call(connection, channel, '', 'rpc_queue', str(4))
    result = int(response)
    print(f'fib(4) = {result}')


if __name__ == '__main__':
    main()
