"""
协程就是用户态下的线程，是人们在有了进程、线程之后仍觉得效率不够，而追求的又一种高并发解决方案。
为什么说是用户态，是因为操作系统并不知道它的存在，
它是由程序员自己控制、互相协作的让出控制权而不是像进程、线程那样由操作系统调度决定是否让出控制权。
"""
import random
from time import sleep
import greenlet
import queue

def a():
    print("a start")
    b()
    print("a end")


def b():
    print("b start")
    c()
    print("b end")


def c():
    print("c start")
    print("c end")

queue = queue.Queue(1)

@greenlet
def producer():
    chars = ['a', 'b', 'c', 'd', 'e']
    global queue
    while True:
        char = random.choice(chars)
        queue.put(char)
        print ("Produced: ", char)
        sleep(1)
        consumer.switch()

@greenlet
def consumer():
    global queue
    while True:
        char = queue.get()
        print("Consumed: ", char)
        sleep(1)
        producer.switch()

if __name__ == "__main__":
    producer.run()
    consumer.run()
    # a()