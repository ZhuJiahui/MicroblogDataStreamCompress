# -*- coding: utf-8 -*-
'''
Created on 2013年11月16日
Last on 2014年1月2日

@author: ZhuJiahui506
'''
import os
from datetime import datetime
from ExcelToolkit import open_sheet
from TimeConvert import time_convert
from WordSegment import word_segment, get_stopwords
from TextToolkit import quick_write_list_to_text

def data_segment(read_filename, write_directory):
    weibo_sheet = open_sheet(read_filename)
    
    weibo_column = weibo_sheet.ncols
    weibo_row = weibo_sheet.nrows
    print 'Number of the Weibo row: %d' % weibo_row
    
    stopwords_list = get_stopwords()
    
    all_weibo_word = []
    each_weibo_fenci = []
    file_number = 1
    
    piece = 3000
    if weibo_row < piece:
        print "Exception:Data is too small!!!"
    else:
        for i in range(1, weibo_row):
            weibo_id = str(int(weibo_sheet.cell(i, 0).value))
               
            weibo_time = weibo_sheet.cell(i, 2).value
            weibo_time = time_convert(weibo_time)
        
            weibo_content = str(weibo_sheet.cell(i, weibo_column - 1).value)
            fenci_result = word_segment(weibo_content, stopwords_list)
            each_weibo_fenci.append(weibo_id.strip() + " " + str(weibo_time) + " " + " ".join(fenci_result))
            
            for word in set(fenci_result).difference(all_weibo_word):
                all_weibo_word.append(word)     
            
            if i % piece == 0:
                quick_write_list_to_text(each_weibo_fenci, write_directory + u'/each_weibo_fenci/' + str(file_number) + '.txt')
                quick_write_list_to_text(all_weibo_word, write_directory + u'/all_weibo_word/' + str(file_number) + '.txt')
                file_number = file_number + 1
                each_weibo_fenci = []
                all_weibo_word = []
                if weibo_row - i < piece:
                    break;
        
    print "Data Segmentation Complete!!!"
    print "Total Segments: %d" % (file_number - 1)    

if __name__ == '__main__':
    start = datetime.now()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    #read_filename = root_directory + u'dataset/mixture_topics/topics_data1.xlsx'
    #write_directory = root_directory + u'dataset/batch_data_segment/topics_data1'
    read_filename = root_directory + u'dataset/mixture_topics/topics_data2.xlsx'
    write_directory = root_directory + u'dataset/batch_data_segment/topics_data2'
    
    #read_filename = root_directory + u'dataset/test.xlsx'
    #write_directory = root_directory + u'dataset/batch_data_segment/test'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
        os.mkdir(write_directory + u'/each_weibo_fenci')
        os.mkdir(write_directory + u'/all_weibo_word')
        
    if (not(os.path.exists(write_directory + u'/each_weibo_fenci'))):
        os.mkdir(write_directory + u'/each_weibo_fenci')
    
    if (not(os.path.exists(write_directory + u'/all_weibo_word'))):
        os.mkdir(write_directory + u'/all_weibo_word')
    
    data_segment(read_filename, write_directory)
    
    print 'Total time: %d seconds!!!' % ((datetime.now() - start).seconds)
    print 'Complete !!!'
    
    