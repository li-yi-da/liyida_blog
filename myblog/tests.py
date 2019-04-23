from django.test import TestCase

# Create your tests here.

# a = None
#
# print(len(a))

# import os
#
# def serverretart():
#     # os.popen('supervisorctl reload')
#     # os.popen('service nginx restart')
#     data = os.popen('netstat -n')
#     print(data.read())
#
# if __name__ == '__main__':
#     serverretart()

# print(os.popen('netstat').read())

# data = os.popen('netstat -n')
# lines = data.read()
# print(lines)

# a = {
#     'a':1,
#     'w':2
# }
#
# print(a['a'])

# class Aaaa():
#
#     def __init__(self, a=None, b='eee'):
#         self.a = a
#         self.b = b
#
#     # def a(self):
#     #     self.a1 = 1
#     #     a2 = 2
#     #     self.a2 = a2
#
#     def b1(self):
#         # self.a()
#         print(self.a)
#         print(self.b)
#
# obj = Aaaa('a','bbb')
# obj.b1()

#
# class Aaaa():
#
#     def __init__(self, a):
#         self.a = a
#
#     def b1(self):
#         b2 = self.a[0:8]
#         return b2
#
#     def bb(self):
#         if self.a == 1:
#             return '1'
# obj = Aaaa([])
# print(obj.b1())


# obj = Aaaa(2)
# print(obj.bb())

a = [1,2,3]
b = [4,5,6]
# print([(i,j) for i in a for j in b])
# print([i for i in a for j in b])
# a.append(for i in b])
# print(a)
# for i in b:
#     a.append(i)
# print(a)

def Test(ta, tb, *args):
    print(a)
    print(b)
    at = tuple(a)
    print(at)
    bt = tuple(b)
    # for i in a:
    #     args.__add__(i)
    # for i in b:
    #     args.__add__(i)
    args.__add__(at)
    args.__add__(bt)
    print(at)
    print(args)

Test(a,b,)

# at = tuple(a)
# print(at)