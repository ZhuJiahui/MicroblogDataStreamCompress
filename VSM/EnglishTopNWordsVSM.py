# -*- coding: utf-8 -*-
'''
Created on 2013年11月28日
Last on 2013年11月29日

@author: ZhuJiahui506
'''
import os
from TextToolkit import get_text_to_complex_list, quick_write_list_to_text
import time

def top_N_words_tfidf_vsm_process(read_directory1, read_directory2, write_directory):
    '''
    微博文本的向量空间构造，值为TF
    :param read_filename1:
    :param read_filename2:
    :param write_filename:
    '''
    
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    for i in range(file_number):
        each_text_segment = [] 
        top_n_word = []
        
        get_text_to_complex_list(each_text_segment, read_directory1 + '/' + str(i + 1) + '.txt', 0)
        f = open(read_directory2 + '/' + str(i + 1) + '.txt', 'rb')
        line = f.readline()
        while line:
            top_n_word.append(line.split()[0])
            line = f.readline()  
        f.close()
        
        result = []
        
        for row in range(len(each_text_segment)):
            
            tf_dict = {}  # 词频TF字典
            for key in top_n_word:
                tf_dict[key] = 0
            
            for j in range(len(each_text_segment[row])):
                try:
                    tf_dict[each_text_segment[row][j]] += 1
                except KeyError:
                    tf_dict[each_text_segment[row][j]] = 0
            
            this_line = []
            for key in top_n_word:
                this_line.append(str(tf_dict[key]))
            
            #每一行合并为字符串，方便写入
            result.append(" ".join(this_line))
        
        quick_write_list_to_text(result, write_directory + '/' + str(i + 1) + '.txt')
    
    print "VSM Complete!!!"

if __name__ == "__main__":

    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset/batch_data_segment/Music/Music2/each_text_segment'
    read_directory2 = root_directory + u'dataset/batch_data_segment/Music/Music2/top_n_word'
    write_directory = root_directory + u'dataset/batch_data_segment/Music/Music2/vsm'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    top_N_words_tfidf_vsm_process(read_directory1, read_directory2, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
