# -*- coding: utf-8 -*-
'''
Created on 2013年12月28日

@author: ZhuJiahui506
'''

import os
import time
import numpy as np
import random
from TextToolkit import quick_write_list_to_text, get_text_to_nparray


def data_sample(read_directory, write_directory1, write_directory2):
    '''
    
    :param read_directory:
    :param write_directory1:
    :param write_directory2:
    '''
    file_number = np.sum([len(files) for root, dirs, files in os.walk(read_directory)])
    sample_size = 250
    sample_time = []
    ratio = []
    
    for i in range(file_number):
        vsm_matrix = get_text_to_nparray(read_directory + '/' + str(i + 1) + '.txt', 'int')
        vsm_matrix = vsm_matrix.T
        
        print 'Batch: %d' % (i + 1)
        start = time.clock()
        
        data_dimension = vsm_matrix.shape[0]
        
        Q = np.zeros((sample_size, data_dimension))
        for k in range(Q.shape[0]):
            for j in range(Q.shape[1]):
                Q[k, j] = random.gauss(1, np.sqrt(np.true_divide(1, np.sqrt(sample_size))))
                
        sample_result = np.dot(Q, vsm_matrix)
        
        this_ratio = np.true_divide(sample_size, data_dimension) * 8.0 / 4.0
        ratio.append(str(this_ratio))
        
        interval = time.clock() - start
        print 'Time: %f' % interval
        sample_time.append(str(interval))
        
        write_result = []
        for each in sample_result:
            write_result.append(" ".join([str(x) for x in each]))
        quick_write_list_to_text(write_result, write_directory1 + '/' + str(i + 1) + '.txt')
        
    quick_write_list_to_text(sample_time, write_directory2 + '/sample_time.txt')
    quick_write_list_to_text(ratio, write_directory2 + '/ratio.txt')
    
    
if __name__ == '__main__':

    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset/batch_data_segment/Music/Music5/update_vsm'
    
    write_directory1 = root_directory + u'dataset/sample/Music5/sample_data'
    write_directory2 = root_directory + u'dataset/sample/Music5'
    
    if (not(os.path.exists(root_directory + u'dataset/sample'))):
        os.mkdir(root_directory + u'dataset/sample')
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)
    if (not(os.path.exists(write_directory1))):
        os.mkdir(write_directory1)
    
    data_sample(read_directory, write_directory1, write_directory2)
    
    print "Sample Complete!!!"
