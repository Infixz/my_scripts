#coding:utf-8
import time

def print_a():
    print 'a'

def main():
    while True:
        print_a()
        time.sleep(2)

if __name__ == '__main__':
    main()