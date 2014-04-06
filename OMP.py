# -*- coding: utf-8 -*-
'''
Created on 2013年12月18日

@author: ZhuJiahui506
'''

import numpy as np
import time
from scipy import linalg
import scipy as sp

def omp(D, X, spn=5):
    '''
    Sparse coding of a group of signals based on a given 
    dictionary and specified number of atoms to use.
    
    :param D: 字典
    the dictionary (its columns MUST be normalized).
    :param X: 数据
    the signals to represent
    :param spn: 稀疏度
    the max. number of coefficients for each signal.
    
    output omp_gamma: 稀疏系数矩阵
    sparse coefficient matrix.
    '''
    # data_dimension = X.shape[0]
    data_size = X.shape[1]
    dict_size = D.shape[1]
    
    omp_gamma = np.zeros((data_size, dict_size))
    
    for k in range(data_size):
        if k % 10 == 0:
            print k + 1

        x = X[:, k]  # 此处是行向量
        residual = x  # 此处是行向量
        
        nonzero_index = np.zeros(spn, np.int)
        
        for j in range(spn):
            proj = sp.dot(residual, D)
            
            nonzero_index[j] = np.argmax(np.abs(proj))

            a = linalg.lstsq(D[:, nonzero_index[:(j + 1)]], x)[0]
            
            #计算残差
            #residual = np.subtract(x, sp.dot(D[:, nonzero_index[:(j + 1)]], a.T).T)
            residual = np.subtract(x, sp.dot(a, np.transpose(D[:, nonzero_index[:(j + 1)]])))
            #此处residual是行向量


            if np.sum(np.multiply(residual, residual)) < 1e-6:
                break
        
    
        omp_gamma[k][nonzero_index[: (j + 1)]] = a
    
    return np.transpose(omp_gamma)

'''
batch_omp remains to be completed.
'''
def batch_omp(DtX, DtD, spn=5):
    '''
    Batch sparse coding of a group of signals based on a given 
    dictionary and specified number of atoms to use.
    '''

    # data_dimension = X.shape[0]
    data_size = DtX.shape[1]
    dict_size = DtX.shape[0]
     
    batch_omp_gamma = np.zeros((dict_size, data_size))
     
    for k in range(data_size):
        if k % 10 == 0:
            print k + 1
        # a = []
        #x = X[:, k]  # 此处是行向量
        #residual = x  # 此处是行向量
         
        Alpha = DtX[:, k]
        #L = 
        nonzero_index = np.zeros(spn, np.int)
        #L = np.ones((spn-1, spn-1))
        L = np.zeros((spn, spn))
        
        for j in range(spn):
            max_index = np.argmax(np.abs(Alpha))
            
            if j > 0:         
                w = linalg.solve(L[0 : j, 0 : j], DtD[nonzero_index[0 : j], max_index])
                #L1[0 : j, 0 : j] = L[0 : j, 0 : j]
                L[j, 0 : j] = w.T
                L[0 : j, j] = np.zeros(j).T
                L[j, j] = np.sqrt(np.subtract(1, np.dot(w.T, w)))
                
            
            nonzero_index[j] = max_index
            
            LL = np.dot(L[0 : j + 1, 0 : j + 1], L[0 : j + 1, 0 : j + 1].T)
            
            c = linalg.solve(LL, Alpha[nonzero_index[0 : j + 1]])
            
            batch_omp_gamma[nonzero_index[0 : (j + 1)], k] = c
            #proj = sp.dot(residual, D)
             
            #nonzero_index[j] = np.argmax(np.abs(proj))
 
            #a = linalg.lstsq(D[:, nonzero_index[:(j + 1)]], x)[0]
             
            #计算残差
            #residual = np.subtract(x, sp.dot(D[:, nonzero_index[:(j + 1)]], a.T).T)
            Beta = np.dot(DtD[:, nonzero_index[0 : j + 1]], c)
            Alpha = np.subtract(Alpha, Beta)
            #此处residual是行向量

    return batch_omp_gamma

if __name__ == '__main__':
    
    read_filename1 = u'D:/Local/DataStreamMining/dataset/non_orthogonal/Music5/字典.txt'
    read_filename2 = u'D:/Local/DataStreamMining/dataset/non_orthogonal/Music5/采样信号/1.txt'
    read_filename3 = u'D:/Local/DataStreamMining/dataset/non_orthogonal/Music5/Q.txt'
    #read_filename1 = u'dataset/D.txt'
    #read_filename2 = u'dataset/X.txt'
    #D = np.array([[1,2], [4,5], [7,9], [3, 4], [5, 8], [4, 6], [0, 8]])
    #X = np.array([[2, 4, 5, 6], [4, 6, 7, 8], [2, 4, 7, 9], [3, 8, 6, 4], [5, 7, 4, 3], [3, 8, 6, 4], [5, 7, 4, 3]])
    
    f1 = open(read_filename1)
    d = f1.readlines()
    f1.close()
    
    dict_size = len(d[0].split())
    D = np.zeros((len(d), dict_size))
    
    for i in range(len(d)):
        #D[i] = np.array([float(y) for y in d[i].split()])
        D[i] = np.array(map(float, d[i].split()))
    
    f2 = open(read_filename2)
    x = f2.readlines()
    f2.close()
    
    data_size = len(x[0].split())
    X = np.zeros((len(x), data_size))
    
    for i in range(len(x)):
        #X[i] = np.array([float(y) for y in x[i].split()])
        X[i] = np.array(map(float, x[i].split()))
        
    f3 = open(read_filename3)
    q = f3.readlines()
    f3.close()
    
    data_size = len(q[0].split())
    Q = np.zeros((len(q), data_size))
    
    for i in range(len(q)):
        #X[i] = np.array([float(y) for y in x[i].split()])
        Q[i] = np.array(map(float, q[i].split()))
    
    
    D1 = np.dot(Q, D)
    #X1 = linalg.lstsq(Q, X)[0]
    #DtX = np.dot(D.T, X1)
    #DtD = np.dot(D.T, D)
    #D = np.loadtxt(read_filename1)
    #X = np.loadtxt(read_filename2)
    start = time.clock()
    #aa = D[0][:, None][:, 0]
    #a = np.linalg.lstsq(D, X)[0]
    #Da = D[:, 0:10]
    #Xa = X[:, 0:10]
    #b = sp.dot(linalg.pinv(D1[:, 0:10]), X[:, 0:10])
    #a = linalg.lstsq(D1[:, 0:10], X[:, 0:10])[0]
    #a = np.transpose(D)
    spn = 3
    #G = batch_omp(DtX, DtD, spn)
    G0 = omp(D1, X, spn)
    #print G
    print 'Total time %f seconds' % (time.clock() - start)
