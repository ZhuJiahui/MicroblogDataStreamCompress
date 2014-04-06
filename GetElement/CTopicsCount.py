# -*- coding: utf-8 -*-
'''
Created on 2014年1月6日

@author: ZhuJiahui506
'''

import os
import time
from TextToolkit import quick_write_list_to_text
from TimeConvert import time_convert
from ExcelToolkit import open_sheet
import numpy as np

def topics_count(read_directory1, read_filename, write_directory):
    
    #文件总数
    file_number = np.sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    weibo_sheet = open_sheet(read_filename)
    weibo_row = weibo_sheet.nrows
    
    for i in range(file_number):    
        id_series = []
        time_series = []
        
        f1 = open(read_directory1 + '/' + str(i + 1) + '.txt')
        line = f1.readline()
        while line:
            id_series.append(line.split('\x7f')[0])
            #try:
            time_series.append(float(line.split('\x7f')[1]))
            #except:
                #time_series.append(41275.0)
            line = f1.readline()
        f1.close()
      
        all_tag = []
        topic_dict = {}
        j = 1
        k = 0

        while j < weibo_row:
            weibo_id = str(weibo_sheet.cell(j, 0).value).split('.')[0]
            weibo_time = weibo_sheet.cell(j, 2).value
            weibo_time = time_convert(weibo_time)
            weibo_tag = str(int(weibo_sheet.cell(j, 5).value))
            
            if weibo_id == id_series[k] and np.abs(weibo_time - time_series[k]) < 0.01:
            #if weibo_id == id_series[k] and weibo_time >= 41538 and weibo_time < 41548:
                if weibo_tag in all_tag:
                    topic_dict[weibo_tag] += 1
                else:
                    all_tag.append(weibo_tag)
                    topic_dict[weibo_tag] = 1
                
                k += 1
            
            j += 1
            if k >= len(id_series):
                break
             
        
        result = []
        for each in all_tag:
            result.append(each + ' ' + str(topic_dict[each]))
    
        quick_write_list_to_text(result, write_directory + '/' + str(i + 1) + '.txt')
        

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = 'D:/Local/DataStreamMining/dataset/cluster/topics_data23/final_id_time'
    read_filename = root_directory + u'dataset/mixture_topics/topics_data2.xlsx'
    write_directory = 'D:/Local/DataStreamMining/dataset/cluster/topics_data23/topics_count'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)

    topics_count(read_directory1, read_filename, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'