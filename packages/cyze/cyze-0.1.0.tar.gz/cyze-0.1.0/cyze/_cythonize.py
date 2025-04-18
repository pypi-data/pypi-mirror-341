#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setup.py
@Time    :   2025/04/14
@Author  :   Winter.Yu 
@Version :   1.0
@Contact :   winter741258@126.com
@Desc    :   None
'''

# here put the import lib
import sys
from distutils.core import setup
 
try:
    from Cython.Build import cythonize
except:
    print("你没有安装Cython，请安装 pip install Cython")
    print("本项目需要C++开发支持，请确认安装了相应组件")
 
arg_list = sys.argv
f_name = arg_list[1]
sys.argv.pop(1)
 
setup(ext_modules=cythonize(f_name))