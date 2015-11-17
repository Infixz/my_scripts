# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:54:08 2015

@author: user
"""

import threading
import time

class MyThread(threading.Thread):
    def run(self):
        global num
        for i in range(3):
            time.sleep(1)
            num += 1
            msg = self.name + " set num to " + str(num)
            print msg
num = 0                
def test():
    for i in range(5):
        t = MyThread()
        t.start()
        
if __name__ == "__main__":
    test()
