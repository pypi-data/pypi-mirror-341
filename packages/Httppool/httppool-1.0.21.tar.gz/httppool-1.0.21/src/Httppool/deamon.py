#!/usr/bin/python
# -*- coding: utf-8 -*-
# alex_dev
# frothy2000@gmail.com

from multiprocessing import Process
import Httppool

PROCESS_NAME = 'Httppool-deamon.py'

class HttppoolDeamon(object):

    def __init__(self, name=PROCESS_NAME):
        self.process = Process(name=name, daemon=True, target=Httppool.run_producer_thread())

    def start(self):
        self.process.start()

    def stop(self):
        self.process.terminate()


if __name__ == '__main__':
    p = HttppoolDeamon()
    p.start()

