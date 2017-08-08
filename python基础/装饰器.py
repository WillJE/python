"""
装饰器也就是一种包装材料，它们可以让你在执行被装饰的函数之前或之后执行其他代码，
而且不需要修改函数本身。（原句比较长：You see, decorators are wrappers which 
means that they let you execute code before and after the function 
they decorate without the need to modify the function itself.）
"""

# 一个装饰器是一个需要另一个函数作为参数的函数
def my_shiny_new_decorator(a_function_to_decorate):
    # 在装饰器内部动态定义一个函数：wrapper(原意：包装纸).
    # 这个函数将被包装在原始函数的四周
    # 因此就可以在原始函数之前和之后执行一些代码.
    def the_wrapper_around_the_original_function():
        # 把想要在调用原始函数前运行的代码放这里
        print("Before the function runs")

        # 调用原始函数（需要带括号）
        a_function_to_decorate()

        # 把想要在调用原始函数后运行的代码放这里
        print("After the function runs")

    # 直到现在，"a_function_to_decorate"还没有执行过 (HAS NEVER BEEN EXECUTED).
    # 我们把刚刚创建的 wrapper 函数返回.
    # wrapper 函数包含了这个函数，还有一些需要提前后之后执行的代码，
    # 可以直接使用了（It's ready to use!）
    return the_wrapper_around_the_original_function


# Now imagine you create a function you don't want to ever touch again.
def a_stand_alone_function():
    print("I am a stand alone function, don't you dare modify me")


a_stand_alone_function()
# outputs: I am a stand alone function, don't you dare modify me

# 现在，你可以装饰一下来修改它的行为.
# 只要简单的把它传递给装饰器，后者能用任何你想要的代码动态的包装
# 而且返回一个可以直接使用的新函数:

a_stand_alone_function_decorated = my_shiny_new_decorator(a_stand_alone_function)
a_stand_alone_function_decorated()
# outputs:
# Before the function runs
# I am a stand alone function, don't you dare modify me
# After the function runs
# 现在你大概希望，每次调用a_stand_alone_function
# 时，实际调用的是a_stand_alone_function_decorated 。这很容易，只要把
# my_shiny_new_decorator
# 返回的函数覆盖
# a_stand_alone_function
# 就可以了：
a_stand_alone_function = my_shiny_new_decorator(a_stand_alone_function)
a_stand_alone_function()
# outputs:
# Before the function runs
# I am a stand alone function, don't you dare modify me
# After the function runs
