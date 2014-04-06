# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: ZhuJiahui506
'''

import numpy as np

def KL_distance(a, b):
    '''
    Compute the Kullback-Leibler Divergence of two vectors.
    :param a: vector1
    :param b: vector2
    '''
    if len(a) == len(b):
        for i in range(len(a)):
            if a[i] < 0.00001:
                a[i] = 0.0001
            if b[i] < 0.00001:
                b[i] = 0.0001
        
        a = np.true_divide(a, np.sum(a))
        b = np.true_divide(b, np.sum(b))
        distance = np.dot(a, np.log2(np.true_divide(a, b)))
    else:
        distance = 0
    
    return distance

if __name__ == '__main__':
    a = np.array([1,2,39])
    b = np.array([1,2,9])
    print KL_distance(a, b)