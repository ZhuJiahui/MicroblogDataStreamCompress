# -*- coding: utf-8 -*-
'''
Created on 2014年1月5日

@author: ZhuJiahui506
'''

import os
import numpy as np
from Reflect import reflect_vsm_to_wordlist2
from TextToolkit import quick_write_list_to_text
import time

def map_word_list(read_directory1, read_filename2, write_filename):
    
    #文件总数
    file_number = np.sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    word_list = []
    f = open(read_filename2, 'rb')
    line = f.readline()
    while line:
        word_list.append(line.strip())
        line = f.readline()
    
    f.close()
    
    result = []
    for i in range(file_number):
        vsm = np.loadtxt(read_directory1 + '/' + str(i + 1) + '.txt')
        vsm = vsm.T
        for each in vsm:
            result.append(" ".join(reflect_vsm_to_wordlist2(each, word_list)))
    
    quick_write_list_to_text(result, write_filename)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = 'D:/Local/DataStreamMining/dataset/cluster/topics_data23/final_cluster_center'
    read_filename2 = 'D:/Local/DataStreamMining/dataset/cluster/topics_data23/new_word_list.txt'
    write_filename = 'D:/Local/DataStreamMining/dataset/cluster/topics_data23/text_result_tf.txt'
    
    map_word_list(read_directory1, read_filename2, write_filename)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    