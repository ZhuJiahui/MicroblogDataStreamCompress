# -*- coding: utf-8 -*-
'''
Created on 2013年11月20日

@author: ZhuJiahui506
'''

import os
import time
from TextToolkit import quick_write_list_to_text
import numpy as np

def get_weibo_entropy(read_directory1, read_directory2, write_directory):
    '''
    计算文本信息熵
    :param read_directory1: 词频向量文件目录
    :param read_directory2: top n word文件目录
    :param write_directory: 写入目录
    '''

    #文件总数
    file_number = np.sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    for i in range(file_number):
        word_weight = []
        
        #获取词频向量
        f0 = open(read_directory1 + '/' + str(i + 1) + '.txt')
        each_vsm = f0.readlines()
        f0.close()
        
        #获取词汇权值为一个列表
        f = open(read_directory2 + '/' + str(i + 1) + '.txt')
        line = f.readline()
        while line:
            word_weight.append(float(line.split()[1]))
            line = f.readline()  
        f.close()
        
        #得到的word_weight是一个array
        word_weight = np.log2(word_weight)
        
        entropy_all = []
        
        for each in each_vsm:
            #计算熵值
            each_line_vsm = np.array([float(x) for x in each.split()])
            entropy_all.append(str(np.dot(word_weight, each_line_vsm)))
        
        #写入文件
        quick_write_list_to_text(entropy_all, write_directory + '/' + str(i + 1) + '.txt')
    
    print "Compute Entropy Complete!!!"

if __name__ == "__main__":

    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset/batch_data_segment/Music/Music2/update_vsm'
    read_directory2 = root_directory + u'dataset/batch_data_segment/Music/Music2/top_n_word'
    write_directory = root_directory + u'dataset/batch_data_segment/Music/Music2/entropy'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    get_weibo_entropy(read_directory1, read_directory2, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
