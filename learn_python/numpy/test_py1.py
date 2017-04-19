import os
import sys
#from skimage import data, io, filters

def test_py() :
	a = numpy.loadtxt('pattern.txt');
#	image = data.coins() # or any NumPy array!
	image = a;
	edges = filters.sobel(image);
	io.imshow(edges);
	io.show();

test_py()

