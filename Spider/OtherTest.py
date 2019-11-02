import re
import random
import pandas as pd
import numpy as np
import collections

def ysf(a,b):
   d = collections.deque(range(1,a+1))
   while d:
      d.rotate(-b)
      print(d.pop())

def dequeTst():
   d = collections.deque([])
   d.append('a')
   d.appendleft('b')
   d.extendleft(['e','f','g'])
   print(d)
   d.rotate(-2)
   print(str(d))

if __name__ == '__main__':
   # ysf(41,3)
   # dequeTst()
   # d = collections.deque(maxlen=3)
   # d.append('a')
   # d.append('b')
   # d.append('c')
   # print(d)
   # d.append('d')
   # print(d)
   n = np.array(random.sample(range(50),10))
   print(n)
   n = np.append(n, random.sample(range(1000, 1000 + 50), 10), axis=0)
   print(n)

