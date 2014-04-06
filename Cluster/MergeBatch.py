# -*- coding: utf-8 -*-
'''
Created on 2014年1月10日

@author: ZhuJiahui506
'''

import os
import time
from TextToolkit import quick_write_list_to_text, get_text_to_nparray, get_text_to_single_list

def merge_batch(read_directory1, read_directory2, read_directory3, read_directory4, read_filename, write_directory1, write_directory2):
    
    all_batch_index = []
    f = open(read_filename)
    line = f.readline()
    while line:
        all_batch_index.append(line.split())
        line = f.readline()
        
    f.close()
    
    for i in range(len(all_batch_index)):
        this_word_list = []
        f1 = open(read_directory2 + '/' + str(i + 1) + '.txt', 'rb')
        line = f1.readline()
        while line:
            this_word_list.append(line.strip())
            line = f1.readline()
        
        f1.close()
        
        result = []
        result_id_time = []
        
        for j in range(len(all_batch_index[i])):
            
            word_list = []
            f2 = open(read_directory3 + '/' + all_batch_index[i][j] + '.txt', 'rb')
            line = f2.readline()
            while line:
                word_list.append(line.split()[0])
                line = f2.readline()
        
            f2.close()
            
            
            vsm_nparray = get_text_to_nparray(read_directory1 + '/' + all_batch_index[i][j] + '.txt', 'int')
            
            id_time = []
            get_text_to_single_list(id_time, read_directory4 + '/' + all_batch_index[i][j] + '.txt')
            
            for each2 in id_time:
                result_id_time.append(each2)
            
            for each in vsm_nparray:
                tf_dict = {}
                for k in range(len(each)):
                    if each[k] > 0.0001:
                        tf_dict[word_list[k]] = each[k]
                
                tf_dict2 = {}
                for each1 in this_word_list:
                    if each1 in tf_dict.keys():
                        tf_dict2[each1] = tf_dict[each1]
                    else:
                        tf_dict2[each1] = 0
            
                this_line = []
                for key in this_word_list:
                    this_line.append(str(tf_dict2[key]))
            
                #每一行合并为字符串，方便写入
                result.append(" ".join(this_line))
        
        quick_write_list_to_text(result, write_directory1 + '/' + str(i + 1) + '.txt')
        quick_write_list_to_text(result_id_time, write_directory2 + '/' + str(i + 1) + '.txt')
            

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset/batch_data_segment/topics_data2/update_vsm'
    read_directory2 = 'D:/Local/DataStreamMining/dataset/cluster/topics_data22/original_merge_wordlist'
    read_directory3 = root_directory + u'dataset/batch_data_segment/topics_data2/top_n_word'
    read_directory4 = root_directory + u'dataset/batch_data_segment/topics_data2/update_id_time'
    read_filename = 'D:/Local/DataStreamMining/dataset/cluster/topics_data22/original_merge_batch_id.txt'
    write_directory1 = 'D:/Local/DataStreamMining/dataset/cluster/topics_data22/original_merge_vsm'
    write_directory2 = 'D:/Local/DataStreamMining/dataset/cluster/topics_data22/original_merge_id_time'
    
    if (not(os.path.exists(write_directory1))):
        os.mkdir(write_directory1)
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)
    
    merge_batch(read_directory1, read_directory2, read_directory3, read_directory4, read_filename, write_directory1, write_directory2)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'