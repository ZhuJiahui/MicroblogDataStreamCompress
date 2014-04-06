# -*- coding: utf-8 -*-
'''
Created on 2014年1月6日

@author: ZhuJiahui506
'''

import os
import time
from TextToolkit import quick_write_list_to_text
import numpy as np
from Reflect import reflect_vsm_to_wordlist

def merge_all_center(read_directory1, read_directory2, read_filename, write_directory, write_filename):
    #文件总数
    file_number = np.sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    new_word_list = []
    
    batch_index = []
    f = open(read_filename)
    line = f.readline()
    while line:
        batch_index.append(line.split()[0])
        line = f.readline()
        
    f.close()
    
    
    for i in range(file_number):
        word_list = []
        f1 = open(read_directory2 + '/' + batch_index[i] + '.txt', 'rb')
        line = f1.readline()
        while line:
            word_list.append(line.split()[0])
            line = f1.readline()
        
        f1.close()
        
        
        center = np.loadtxt(read_directory1 + '/' + str(i + 1) + '.txt')
        center = center.T
        
        for each in center:
            word_result = reflect_vsm_to_wordlist(each, word_list)
            for word in set(word_result).difference(new_word_list):
                new_word_list.append(word)
    
    
    for i in range(file_number):
        word_list = []
        f1 = open(read_directory2 + '/' + batch_index[i] + '.txt', 'rb')
        line = f1.readline()
        while line:
            word_list.append(line.split()[0])
            line = f1.readline()
        
        f1.close()
        
        center = np.loadtxt(read_directory1 + '/' + str(i + 1) + '.txt')
        center = center.T
        
        #tf_dict = {}
        result = []
        for each in center:
            tf_dict = {}
            for k in range(len(each)):
                if each[k] > 0.0001:
                    tf_dict[word_list[k]] = each[k]
                
            tf_dict2 = {}
            for each1 in new_word_list:
                if each1 in tf_dict.keys():
                    tf_dict2[each1] = tf_dict[each1]
                else:
                    tf_dict2[each1] = 0
            
            this_line = []
            for key in new_word_list:
                this_line.append(str(tf_dict2[key]))
            
            #每一行合并为字符串，方便写入
            result.append(" ".join(this_line))
        
        quick_write_list_to_text(result, write_directory + '/' + str(i + 1) + '.txt')
    
    quick_write_list_to_text(new_word_list, write_filename)
        

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = 'D:/Local/DataStreamMining/dataset/cluster/topics_data22/cluster_center'
    read_directory2 = root_directory + u'dataset/batch_data_segment/topics_data2/top_n_word'
    read_filename = 'D:/Local/DataStreamMining/dataset/cluster/topics_data22/batch_index.txt'
    write_directory = 'D:/Local/DataStreamMining/dataset/cluster/topics_data22/merge_cluster_center'
    write_filename = 'D:/Local/DataStreamMining/dataset/cluster/topics_data22/new_word_list.txt'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    merge_all_center(read_directory1, read_directory2, read_filename, write_directory, write_filename)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'