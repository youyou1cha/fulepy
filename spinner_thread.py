#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import itertools
import time
import sys

class Singal:
    go = True

def spin(msg,signal):
    write, flush = sys.stdout.write,sys.stdout.flush
    # 重复迭代元素迭代器
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:
            break
    write(' ' * len(status) + '\x08' * len(status))

def slow_function():
    time.sleep(10)
    return 42

def supervisor():
    signal = Singal()
    spinner = threading.Thread(target=spin,args=('thinking!',signal))
    print('spinner object:',spinner)
    spinner.start()
    result = slow_function()
    signal.go = False
    spinner.join()
    return result

def main():
    result = supervisor()
    print('Answer:',result)

if __name__ == '__main__':
    main()
