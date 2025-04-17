import random as r
import turtle as t
from setuptools import setup, find_packages

setup(
    name='Math_A',  
    version='1.5',  
    packages=find_packages(),
    description='A module for Allame hellie`s students',  
    author='M.P.Abdi',  
    author_email='m.p.abdi90@gmail.com',  
    python_requires='>=3.6',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)

"""
فاکتوریل یک عدد را حساب می کند.
"""
def fact(n):

    x = 1
    for i in range(1 , n+1):
        x = x * i
    
    return x

"""
مجموع  عدد اول تا عدد دوم را حساب می کند   
"""

def _sum(a,b):

    m = 0
    for i in range(a, b+1):
        m = m + i

    return m

"""
نشان می دهد که کدام بزرگتر است 
"""

def compair(a,b):

    x = a
    if b > a:
        x = b
    
    return x

"""
تعداد ارقام را حساب می کند
"""

def digits(n):

    t = 0
    while n != 0:
        t = t + 1
        n = n //10
    
    return t

"""
جمع ارقام را حساب می کند
"""

def sum_digits(n):

    sum = 0
    while n != 0:
        sum = sum + n % 10
        n = n //10

    return sum

"""
مقلوب عدد را چاپ می کند
"""

def inverse(n):

    m = 0
    while n != 0:
        m = m * 10 + n % 10
        n = n // 10

    return m

"""
حساب می کند عدد اول است یا خیر
"""

def check_prime(n):

    flag = True
    for i in range(2,n):
        if n % i == 0:
            flag = False

    return flag

"""
ک.م.م را حساب می کند
"""

def k_m_m(a,b):

    i = compair(a,b)
    while i % b != 0 and i % b != 0:
        i = i + 1
    
    return i

"""
ب.م.م را حساب می کند
"""

def b_m_m(a,b):
    
    for i in range(a,0,-1):
        if a % i == 0 and b % i == 0:
            return i
        
