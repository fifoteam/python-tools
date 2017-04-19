#coding=utf-8

import os
import sys
#import ctypes
#import sub_func
#from sub_func import *

def test_py() :

	a = numpy.loadtxt('pattern.txt');
	b = a.shape;

	print("b is ",b);

	image = a;
	edges = filters.sobel(image);

test_py()