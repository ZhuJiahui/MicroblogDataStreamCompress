# -*- coding: utf-8 -*-
'''
Created on 2013年11月21日

@author: ZhuJiahui506
'''

import os
import nltk
import time
from TextToolkit import quick_write_list_to_text

def get_stopwords():
    '''
    获取停用词
    '''

    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    mark_stop = [x.strip() for x in file (root_directory + "stopwords/English_mark_stop.txt")]
    english_stop = [x.strip() for x in file (root_directory + "stopwords/English_stopwords.txt")]
    return mark_stop, english_stop
    
def word_segment(data, mark_stop, english_stop):
    '''
    分词并去除停用词
    :param data:
    :param stopwords_list:
    '''
    
    '''
    segment_text = nltk.word_tokenize(data.replace('.', ' '))
    segment_text = [word.lower() for word in segment_text if word.lower() not in (english_stop + mark_stop)]
    segment = nltk.pos_tag(segment_text)  #词性标注
    '''
    
    
    pattern = r'''(?x)([A-Z]\.)+|\w+(-\w+)*|\$?\d+(\.\d+)?%?|\.\.\.|[][.,;'"?():-_`]'''
    segment_text = nltk.regexp_tokenize(data, pattern)
    #可选择取词干
    #porter = nltk.PorterStemmer()
    segment_text = [t.lower() for t in segment_text if t.lower() not in (english_stop + mark_stop)]
    segment = nltk.pos_tag(segment_text)  #词性标注
    
    
    segment_list = []
    for item in segment:
        segment_list.append(item[0] + "," + item[1])

    return segment_list;

def fenci_process(read_filename):
    '''
    分词操作
    '''
    mark_stop, english_stop = get_stopwords()

    each_review_fenci = []
    all_review_word = []
    
    f = open(read_filename, 'rb')
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        if (i + 1) % 9 == 8:
            fenci_result = word_segment(lines[i][13:], mark_stop, english_stop)
            each_review_fenci.append(" ".join(fenci_result))
            aa = set(fenci_result).difference(all_review_word)
            for word in aa:
                all_review_word.append(word)

    
    print "\nComplete Word Segmentation!!!"
    return each_review_fenci, all_review_word

if __name__ == '__main__':
    
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = root_directory + u'dataset/batch_data_segment/Music/sort_original_data/880.txt'
    write_filename1 = root_directory + u"dataset/test1.txt"
    write_filename2 = root_directory + u"dataset/test2.txt"

    r1, r2 = fenci_process(read_filename1)
    
    quick_write_list_to_text(r1, write_filename1)
    quick_write_list_to_text(r2, write_filename2)
    
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'complete'
