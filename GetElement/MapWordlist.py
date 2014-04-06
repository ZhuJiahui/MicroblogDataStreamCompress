# -*- coding: utf-8 -*-
'''
Created on 2014年1月5日

@author: ZhuJiahui506
'''

import os
import numpy as np
from Reflect import reflect_vsm_to_wordlist
from TextToolkit import quick_write_list_to_text
import time

def map_word_list(read_filename1, read_filename2, write_filename):
    
    word_list = []
    f = open(read_filename2, 'rb')
    line = f.readline()
    while line:
        word_list.append(line.strip().split(',')[0])
        line = f.readline()
    
    f.close()
    
    word_result = []
    vsm = np.loadtxt(read_filename1)
    vsm = vsm.T
    for each in vsm:
        word_result.append(" ".join(reflect_vsm_to_wordlist(each, word_list)))
    
    quick_write_list_to_text(word_result, write_filename)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = 'D:/Local/DataStreamMining/dataset/cluster/Music5/cluster_center/13.txt'
    read_filename2 = root_directory + u'dataset/batch_data_segment/Music/Music5/top_n_word/100.txt'
    write_filename = 'D:/Local/DataStreamMining/dataset/cluster/Music5/c13.txt'
    
    map_word_list(read_filename1, read_filename2, write_filename)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    