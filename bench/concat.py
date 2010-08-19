# Benchmark that compares the times for concatenating arrays with
# compressed arrays vs plain numpy arrays.  The 'numpy' and 'concat'
# styles are for regular numpy arrays, while 'carray' is for carrays.

import sys, math
import numpy
from numpy.testing import assert_array_equal, assert_array_almost_equal
import carray
import time

def concat(data):
    tlen = sum(x.shape[0] for x in data)
    alldata = numpy.empty((tlen,))
    pos = 0
    for x in data:
        step = x.shape[0]
        alldata[pos:pos+step] = x
        pos += step

    return alldata

def append(data, clevel):
    alldata = carray.carray(data[0], clevel=clevel)
    for carr in data[1:]:
        alldata.append(carr)

    return alldata

style = sys.argv[1]
N,K,T = [int(arg) for arg in sys.argv[2:5]]
if len(sys.argv) > 5:
    clevel = int(sys.argv[5])
else:
    clevel = 0

# The next datasets allow for very high compression ratios
a = [numpy.arange(N, dtype='f8') for _ in range(K)]
print("problem size: (%d) x %d = 10^%g" % (N, K, math.log10(N*K)))

t = time.time()
if style == 'numpy':
    for _ in xrange(T):
        r = numpy.concatenate(a, 0)
elif style == 'concat':
    for _ in xrange(T):
        r = concat(a)
elif style == 'carray':
    for _ in xrange(T):
        r = append(a, clevel)
else:
    A = numpy.concatenate(a, 0)
    B = concat(a)
    assert_array_almost_equal(A, B)
    C = append(a).toarray()
    assert_array_almost_equal(A, C)

t = time.time() - t
print('time for concat: %.3fs' % (t / T))

if style == 'carray':
    size = r.cbytes
else: 
    size = r.size*r.dtype.itemsize
print("size of the final container: %.3f MB" % (size / float(1024*1024)) )