"""
װ����Ҳ����һ�ְ�װ���ϣ����ǿ���������ִ�б�װ�εĺ���֮ǰ��֮��ִ���������룬
���Ҳ���Ҫ�޸ĺ���������ԭ��Ƚϳ���You see, decorators are wrappers which 
means that they let you execute code before and after the function 
they decorate without the need to modify the function itself.��
"""

# һ��װ������һ����Ҫ��һ��������Ϊ�����ĺ���
def my_shiny_new_decorator(a_function_to_decorate):
    # ��װ�����ڲ���̬����һ��������wrapper(ԭ�⣺��װֽ).
    # �������������װ��ԭʼ����������
    # ��˾Ϳ�����ԭʼ����֮ǰ��֮��ִ��һЩ����.
    def the_wrapper_around_the_original_function():
        # ����Ҫ�ڵ���ԭʼ����ǰ���еĴ��������
        print("Before the function runs")

        # ����ԭʼ��������Ҫ�����ţ�
        a_function_to_decorate()

        # ����Ҫ�ڵ���ԭʼ���������еĴ��������
        print("After the function runs")

    # ֱ�����ڣ�"a_function_to_decorate"��û��ִ�й� (HAS NEVER BEEN EXECUTED).
    # ���ǰѸոմ����� wrapper ��������.
    # wrapper �����������������������һЩ��Ҫ��ǰ��֮��ִ�еĴ��룬
    # ����ֱ��ʹ���ˣ�It's ready to use!��
    return the_wrapper_around_the_original_function


# Now imagine you create a function you don't want to ever touch again.
def a_stand_alone_function():
    print("I am a stand alone function, don't you dare modify me")


a_stand_alone_function()
# outputs: I am a stand alone function, don't you dare modify me

# ���ڣ������װ��һ�����޸�������Ϊ.
# ֻҪ�򵥵İ������ݸ�װ���������������κ�����Ҫ�Ĵ��붯̬�İ�װ
# ���ҷ���һ������ֱ��ʹ�õ��º���:

a_stand_alone_function_decorated = my_shiny_new_decorator(a_stand_alone_function)
a_stand_alone_function_decorated()
# outputs:
# Before the function runs
# I am a stand alone function, don't you dare modify me
# After the function runs
# ��������ϣ����ÿ�ε���a_stand_alone_function
# ʱ��ʵ�ʵ��õ���a_stand_alone_function_decorated ��������ף�ֻҪ��
# my_shiny_new_decorator
# ���صĺ�������
# a_stand_alone_function
# �Ϳ����ˣ�
a_stand_alone_function = my_shiny_new_decorator(a_stand_alone_function)
a_stand_alone_function()
# outputs:
# Before the function runs
# I am a stand alone function, don't you dare modify me
# After the function runs
