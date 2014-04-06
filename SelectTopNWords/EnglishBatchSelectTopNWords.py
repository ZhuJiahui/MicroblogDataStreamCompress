# -*- coding: utf-8 -*-
'''
Created on 2013年11月28日

@author: ZhuJiahui506
'''

import os
from operator import itemgetter
from TextToolkit import get_text_to_complex_list, get_text_to_single_list, quick_write_list_to_text
import time

def select_top_N_words(read_directory1, read_directory2, write_directory):
    '''
    选取前N个词汇
    :param read_directory1: 所有单词tf文件目录
    :param read_directory2: 关键词文件目录
    :param write_directory: 写入目录
    '''
    #选取的词汇数目
    N = 2000
    
    #目录下的文件个数
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    #权值字典，按词性分配
    score_dict = {"CC":0.0, "CD":0.0, "DT":0.2, "EX":0.0, "FW":0.3, "IN":0.0, "JJ":0.7, \
                  "JJR":0.75, "JJS":0.75, "LS":0.0, "MD":0.5, "NN":0.9, "NNS":0.9, "NNP":1.0, \
                  "NNPS":1.0, "PDT":0.0, "POS":0.0, "PRP":0.1, "PRP$":0.1, \
                  "RB":0.3, "RBR":0.35, "RBS":0.4, "RP":0.5, "SYM":0.0, "TO":0.0, "UH":0.0, \
                  "VB":0.7, "VBD":0.7, "VBG":0.7, "VBN":0.75, "VBP":0.7, "VBZ":0.7, \
                  "WDT":0.0, "WP":0.3, "WP$":0.3, "WRB":0.0, ":":0.0}
    
    for i in range(file_number):
        each_word_tf = [] 
        key_words = []
        
        select_word = []
        word_score = []
        
        get_text_to_complex_list(each_word_tf, read_directory1 + '/' + str(i + 1) + '.txt', 0)
        each_word_tf = each_word_tf[1:]  # 列表，内层2个
        
        get_text_to_single_list(key_words, read_directory2 + '/' + str(i + 1) + '.txt')
        
        for j in range(len(each_word_tf)):
            #word_entity = each_word_tf[j][0].split('/')[0]
            word_tag = each_word_tf[j][0].split(',')[1]
            if each_word_tf[j][0] in key_words:
                select_word.append(each_word_tf[j][0])
                try:
                    word_score.append(float(each_word_tf[j][1]) * score_dict[word_tag] * 1.0)
                except KeyError:
                    word_score.append(float(0.0))  
            else:
                select_word.append(each_word_tf[j][0])
                try:
                    word_score.append(float(each_word_tf[j][1]) * score_dict[word_tag] * 0.80)
                except KeyError:
                    word_score.append(float(0.0))
        
        # 按权值降序排序
        sw = zip(select_word, word_score)
        sw = sorted(sw, key = itemgetter(1), reverse = True)    
        
        result_all = []
        count_number = 1
        for each in sw:
            result_all.append(each[0] + " " + str(each[1]))
            count_number += 1
            if count_number > N:
                break

        quick_write_list_to_text(result_all, write_directory + '/' + str(i + 1) + '.txt')


if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset/batch_data_segment/Music/Music2/tf_all'
    read_directory2 = root_directory + u'dataset/batch_data_segment/Music//Music2/all_key_words'
    write_directory = root_directory + u'dataset/batch_data_segment/Music/Music2/top_n_word'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    select_top_N_words(read_directory1, read_directory2, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
