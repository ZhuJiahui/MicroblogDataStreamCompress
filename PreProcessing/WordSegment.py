# -*- coding: utf-8 -*-
'''
Created on 2013年7月10日
Last on 2013年11月13日

@author: ZhuJiahui506
'''
import os
import jieba as jb
import jieba.posseg as jbp
from datetime import datetime
from ExcelToolkit import open_sheet, sheet_to_list

def get_stopwords():
    '''
    获取停用词
    '''

    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    mark_stop = [x.strip().decode('gbk') for x in file (root_directory + "stopwords/mark_stop.txt")]
    english_stop = [x.strip().decode('gbk') for x in file (root_directory + "stopwords/Englishword.txt")]
    pre_CN_stop = [x.strip().decode('gbk') for x in file (root_directory + "stopwords/stop_word_pre.txt")]
    post_CN_stop = [x.strip().decode('gbk') for x in file(root_directory + "stopwords/stop_word.txt")]
    mul_stop = [x.strip().decode('gbk') for x in file(root_directory + "stopwords/stop_word_mul.txt") ]
    waste_content = [x.strip().decode('gbk') for x in file(root_directory + "stopwords/waste_content.txt") ]
    all_stop = [x.strip().decode('gbk') for x in file(root_directory + "stopwords/cn_stopwords.txt") ]
    return set(mark_stop + english_stop + pre_CN_stop + mul_stop + post_CN_stop + waste_content + all_stop)
    
def word_segment(data, stopwords_list):
    '''
    分词并去除停用词
    :param data:
    :param stopwords_list:
    '''
    try:
        data = [word.strip() for word in data if word not in stopwords_list]
    except Exception, e:
        print data
        print e

    data = "".join(data)

    segment = jb.cut_for_search(data)
    segment = jbp.cut(','.join(segment))  #词性标注
    
    segment_list = []
    for item in segment:
        if (item.word not in stopwords_list):
            segment_list.append(item.word.strip() + "/" + item.flag.strip())

    return segment_list;

def fenci_process(filename):
    '''
    分词操作
    '''
    stopwords_list = get_stopwords()
    weibo_sheet = open_sheet(filename)
    dataList = sheet_to_list(weibo_sheet)  #不含表头部分
    
    weibo_column = weibo_sheet.ncols
    weibo_row = weibo_sheet.nrows
    print 'Number of the Weibo row: %d' % weibo_row
    
    each_weibo_fenci = []
    all_weibo_word = []
    
    for i in range(0, weibo_row - 1):
        fenci_result = word_segment(dataList[weibo_column - 1][i], stopwords_list)
        each_weibo_fenci.append(fenci_result)
        
        for word in set(fenci_result).difference(all_weibo_word):
            all_weibo_word.append(word)
    
    print "\nComplete Word Segmentation!!!"
    return each_weibo_fenci, all_weibo_word

if __name__ == '__main__':
    
    start = datetime.now()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = root_directory + u'dataset/第一夫人彭丽媛.xlsx'
    write_filename1 = root_directory + u"dataset/batch_word_segment/第一夫人彭丽媛1.txt"
    write_filename2 = root_directory + u"dataset/batch_word_segment/第一夫人彭丽媛2.txt"

    r1, r2 = fenci_process(read_filename1)
    
    f = open(write_filename1, 'w')
    line = ''
    for i in range(len(r1)):
        line = " ".join(r1[i]) 
        line += '\n'
        f.write(line)

    f.close
    
    f2 = open(write_filename2, 'w')
    line2 = ''
    for i in range(len(r2)):
        line2 = r2[i]
        line2 += '\n'
        f2.write(line2)
    
    f2.close
    print '总共花了 %d 秒' % ((datetime.now() - start).seconds)
    print 'complete'
