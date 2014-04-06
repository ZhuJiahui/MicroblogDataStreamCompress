# -*- coding: utf-8 -*-
'''
Created on 2013年11月22日

@author: ZhuJiahui506
'''

import os
import time
from EnglishWordSegment import word_segment, get_stopwords
from TextToolkit import quick_write_list_to_text

def data_segment(read_directory, write_directory):
    '''
    数据片内的处理：分词和合并
    :param read_directory: 读取文件目录
    :param write_directory: 写入目录
    '''
    
    # 获取停用词无关词
    mark_stop, english_stop = get_stopwords()
    
    # 文件开始的编号
    first_number = 880
    
    # 文件个数
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    
    print "Begin word segmentation!!!" 
    print "May take a long time, Please Wait..."
    
    for i in range(file_number):
        print "Batch %d..." % (i + 1)
        
        # 每条标题的分词
        each_summary_segment = []
        # 每条文本的分词
        each_text_segment = []
        # 文本中的所有词汇
        all_text_word = []
        # 每条数据中的id,helpfulness,score,time
        phst_line = []
        
        line_count = 1
    
        fr = open(read_directory + '/' + str(first_number + i) + '.txt', 'rb')
        line = fr.readline()
    
        # 对于该文件采取产生结果即写入的方式
        f1 = open(write_directory + u'/phst/' + str(i + 1) + '.txt', 'w')
        while line: 
            if line_count % 9 == 1:
                phst_line.append(line.strip()[19:])
            elif line_count % 9 == 4:
                phst_line.append(line.strip()[20:])
            elif line_count % 9 == 5:
                phst_line.append(line.strip()[14:])
            elif line_count % 9 == 6:
                phst_line.append(line.strip()[13:])
                f1.write(" ".join(phst_line) + "\n")
                phst_line = []
            # 以下2种情况涉及分词        
            elif line_count % 9 == 7:
                this_segment = word_segment(line[16:], mark_stop, english_stop)
                each_summary_segment.append(" ".join(this_segment))
            elif line_count % 9 == 8:
                this_segment = word_segment(line[13:], mark_stop, english_stop)
                each_text_segment.append(" ".join(this_segment))
                for word in set(this_segment).difference(all_text_word):
                    all_text_word.append(word)
            else:
                pass
            
            line_count += 1
            line = fr.readline()
        
        
        fr.close()
        f1.close()
        
        # 写入文件
        quick_write_list_to_text(each_summary_segment, write_directory + u'/each_summary_segment/' + str(i + 1) + '.txt')
        quick_write_list_to_text(each_text_segment, write_directory + u'/each_text_segment/' + str(i + 1) + '.txt')
        quick_write_list_to_text(all_text_word, write_directory + u'/all_text_word/' + str(i + 1) + '.txt')    
        print "Batch %d complete." % (i + 1)
        
    print "Data Segmentation Complete!!!"
    print "Total Segments: %d" % (file_number)    

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset/batch_data_segment/Music/sort_original_data/2'
    write_directory = root_directory + u'dataset/batch_data_segment/Music/Music2'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
        os.mkdir(write_directory + u'/each_summary_segment')
        os.mkdir(write_directory + u'/phst')
        os.mkdir(write_directory + u'/each_text_segment')
        os.mkdir(write_directory + u'/all_text_word')
        
    if (not(os.path.exists(write_directory + u'/each_summary_segment'))):
        os.mkdir(write_directory + u'/each_summary_segment')
        
    if (not(os.path.exists(write_directory + u'/phst'))):
        os.mkdir(write_directory + u'/phst')
    
    if (not(os.path.exists(write_directory + u'/each_text_segment'))):
        os.mkdir(write_directory + u'/each_text_segment')
    
    if (not(os.path.exists(write_directory + u'/all_text_word'))):
        os.mkdir(write_directory + u'/all_text_word')
    
    data_segment(read_directory, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
    
