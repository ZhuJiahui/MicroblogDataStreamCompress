# -*- coding: utf-8 -*-
'''
Created on 2013年11月14日
Last on 2014年1月2日

@author: ZhuJiahui506
'''
import os
import time
from TextToolkit import get_text_to_complex_list, quick_write_list_to_text

def top_N_words_tfidf_vsm_process(read_directory1, read_directory2, write_directory):
    '''
    微博文本的向量空间构造，值为TF
    :param read_filename1:
    :param read_filename2:
    :param write_filename:
    '''
    
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    for i in range(file_number):
        each_weibo_fenci = [] 
        all_weibo_fenci = []
        
        get_text_to_complex_list(each_weibo_fenci, read_directory1 + '/' + str(i + 1) + '.txt', 2)
        f = open(read_directory2 + '/' + str(i + 1) + '.txt')
        line = f.readline()
        while line:
            all_weibo_fenci.append(line.strip().split()[0])
            line = f.readline()  
        f.close()
        
        result = []
        
        for row in range(len(each_weibo_fenci)):
            
            tf_dict = {}  # 词频TF字典
            for key in all_weibo_fenci:
                tf_dict[key] = 0
            
            for j in range(len(each_weibo_fenci[row])):
                try:
                    tf_dict[each_weibo_fenci[row][j].split('/')[0]] += 1
                except KeyError:
                    tf_dict[each_weibo_fenci[row][j].split('/')[0]] = 0
            
            this_line = []
            for key in all_weibo_fenci:
                this_line.append(str(tf_dict[key]))
            
            #每一行合并为字符串，方便写入
            result.append(" ".join(this_line))
        
        quick_write_list_to_text(result, write_directory + '/' + str(i + 1) + '.txt')
    
    print "VSM Complete!!!"

if __name__ == "__main__":

    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset/batch_data_segment/topics_data2/each_weibo_fenci'
    read_directory2 = root_directory + u'dataset/batch_data_segment/topics_data2/top_n_word'
    write_directory = root_directory + u'dataset/batch_data_segment/topics_data2/vsm'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    top_N_words_tfidf_vsm_process(read_directory1, read_directory2, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
