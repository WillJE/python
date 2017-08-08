"""

生成器是一种非常有用的类型，最大的好处在于其数据的产生是在需要使用的时候才产生，
可供一次性遍历，此外还可以做到数据的返回值是无穷多，例如每次返回一个递增值，
从0开始一直递增下去。传统的方式是无法做到的，生成器在很多场景下有着非常重要的作用。

"""
"""
迭代器代表一个数据流对象，不断重复调用迭代器的next()方法可以逐次地返回数据流中的每一项，
当没有更多数据可用时，next()方法会抛出异常StopIteration。此时迭代器对象已经枯竭了，
之后调用next()方法都会抛出异常StopIteration。
"""
"""
生成器也是一个迭代器，但是你只可以迭代他们一次，不能重复迭代，
因为它并没有把所有值存储在内存中，而是实时地生成值
重点是生成器只能使用一次
"""

def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        # print b
        a, b = b, a + b
        n = n + 1

for i in fab(5):
    print(i)
"""
简单地讲，yield 的作用就是把一个函数变成一个 generator，
带有 yield 的函数不再是一个普通函数，Python 解释器会将其视为一个 generator，
调用 fab(5) 不会执行 fab 函数，而是返回一个 iterable 对象！
在 for 循环执行时，每次循环都会执行 fab 函数内部的代码，执行到 yield b 时，
fab 函数就返回一个迭代值，下次迭代时，代码从 yield b 的下一条语句继续执行，
而函数的本地变量看起来和上次中断执行前是完全一样的，于是函数继续执行，
直到再次遇到 yield。
"""
# 读取文件的例子
def read_file(fpath):
   BLOCK_SIZE = 1024
   with open(fpath, 'rb') as f:
       while True:
           block = f.read(BLOCK_SIZE)
           if block:
               yield block
           else:
               return


