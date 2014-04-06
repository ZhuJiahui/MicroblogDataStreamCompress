# -*- coding: utf-8 -*-
'''
Created on 2014年1月10日

@author: ZhuJiahui506
'''

import os
import time
from TextToolkit import quick_write_list_to_text
import numpy as np

def get_new_wordlist(read_directory1, read_directory2, write_directory, write_filename):
    #文件总数
    file_number = np.sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    file_count = 1
    this_start_time = 41538
    new_word_list = []
    all_batch_id = []
    this_batch_id = []
    
    for i in range(file_number):
        time_series = []
        f = open(read_directory1 + "/" + str(i + 1) + '.txt')
        line = f.readline()
        while line:
            time_series.append(float(line.split()[1]))
            line = f.readline()
        
        f.close()
        
        if time_series[0] >= 41548:
            break;
        elif (time_series[-1] < 41538):
            pass;
        else:
            word_list = []
            f1 = open(read_directory2 + '/' + str(i + 1) + '.txt', 'rb')
            line = f1.readline()
            while line:
                word_list.append(line.split()[0])
                line = f1.readline()
            f1.close()
            
            if (time_series[-1] - this_start_time < 2):
                for word in set(word_list).difference(new_word_list):
                    new_word_list.append(word)
                
                this_batch_id.append(str(i + 1))
                
            else:
                quick_write_list_to_text(new_word_list, write_directory + '/' + str(file_count) + '.txt')
                all_batch_id.append(" ".join(this_batch_id))
                
                new_word_list = []
                this_start_time = this_start_time + 2
                this_batch_id = []
                file_count = file_count + 1
    
    quick_write_list_to_text(all_batch_id, write_filename)
        

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset/batch_data_segment/topics_data2/update_id_time'
    read_directory2 = root_directory + u'dataset/batch_data_segment/topics_data2/top_n_word'
    write_directory = 'D:/Local/DataStreamMining/dataset/cluster/topics_data22/original_merge_wordlist'
    write_filename = 'D:/Local/DataStreamMining/dataset/cluster/topics_data22/original_merge_batch_id.txt'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    get_new_wordlist(read_directory1, read_directory2, write_directory, write_filename)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'