"""
编译是函数从里到外，执行是从外到里执行
"""
def bread(func):
    def wrapper():
        print("</''''''\>")
        func()
        print("<\______/>")
    return wrapper
def ingredients(func):
    def wrapper():
        print("#tomatoes#")
        func()
        print("~salad~")
    return wrapper
def sandwich(food="--ham--"):
    print(food)

# sandwich()
# outputs: --ham--
sandwich = bread(ingredients(sandwich))
sandwich()
# outputs:
# </''''''\>
# #tomatoes#
# --ham--
# ~salad~
# <\______/>
