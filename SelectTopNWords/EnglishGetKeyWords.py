#coding:utf-8
'''
Created on 2013年11月28日

@author: ZhuJiahui506
'''

import os
from TextToolkit import quick_write_list_to_text
import time

def count_word_tf(read_directory, write_directory):
       
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    
    for i in range(file_number):
        review_keywords = []
        
        f = open(read_directory + '/' + str(i + 1) + '.txt', 'rb')
        line = f.readline()
        while line:
            for word in set(line.split()).difference(review_keywords):
                review_keywords.append(word)
                             
            line = f.readline()
        f.close()
        
        quick_write_list_to_text(review_keywords, write_directory + '/' + str(i + 1) + '.txt')

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset/batch_data_segment/Music/Music2/each_summary_segment'
    write_directory = root_directory + u'dataset/batch_data_segment/Music/Music2/all_key_words'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    count_word_tf(read_directory, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    