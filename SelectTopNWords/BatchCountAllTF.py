# -*- coding: utf-8 -*-
'''
Created on 2013年11月14日
Last on 2014年1月2日
@author: ZhuJiahui506
'''

import os
from operator import itemgetter
from TextToolkit import get_text_to_single_list, get_text_to_complex_list, quick_write_list_to_text
import time

def count_word_tf(read_directory1, read_directory2, write_directory):
    '''
    计算每片数据的所有词汇的词频
    :param read_directory1: 文本文件目录
    :param read_directory2: 所有词汇文件目录
    :param write_directory: 写入目录
    '''
       
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    for i in range(file_number):
        each_weibo_fenci = [] 
        all_weibo_fenci = []
        
        get_text_to_complex_list(each_weibo_fenci, read_directory1 + '/' + str(i + 1) + '.txt', 2)
        get_text_to_single_list(all_weibo_fenci, read_directory2 + '/'+ str(i + 1) + '.txt')
        
        tf_dict = {}  #词频TF字典
        for key in all_weibo_fenci:
            tf_dict[key] = 0
            
        for row in range(len(each_weibo_fenci)):
            for j in range(len(each_weibo_fenci[row])):
                try:
                    tf_dict[each_weibo_fenci[row][j]] += 1
                except KeyError:
                    tf_dict[each_weibo_fenci[row][j]] = 0
        
        #词频列表
        value_list = []
        for key in all_weibo_fenci:
            value_list.append(tf_dict[key])
        
        # 按词频降序排序
        va = zip(all_weibo_fenci, value_list)
        va = sorted(va, key = itemgetter(1), reverse = True)    
        
        result_all = ['-Word- -TF-']
        for each in va:
            result_all.append(each[0] + " " + str(each[1]))

        
        quick_write_list_to_text(result_all, write_directory + '/' + str(i + 1) + '.txt')

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset/batch_data_segment/topics_data2/each_weibo_fenci'
    read_directory2 = root_directory + u'dataset/batch_data_segment/topics_data2/all_weibo_word'
    write_directory = root_directory + u'dataset/batch_data_segment/topics_data2/tf_all'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    count_word_tf(read_directory1, read_directory2, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    