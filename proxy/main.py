#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2022-04-05
@author: Shell.Xu
@copyright: 2022, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
import sys
import socket


def main():
    host, port
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as li:
        li.bind((host, port))
        li.listen(5)

        while True:
            conn, addr = li.accept()
            


if __name__ == '__main__':
    main()
