# -*- coding: utf-8 -*-
'''
Created on 2014年1月6日

@author: ZhuJiahui506
'''

import os
import time
from TextToolkit import quick_write_list_to_text
from ExcelToolkit import open_sheet
from TimeConvert import time_convert
import numpy as np

def compute_purity(read_filename1, read_filename2, read_filename3, write_filename):
    
    #文件总数
    file_number = np.sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    weibo_sheet = open_sheet(read_filename3)
    weibo_row = weibo_sheet.nrows
        
    id_series = []
    time_series = []
    f1 = open(read_filename2)
    line = f1.readline()
    while line:
        id_series.append(line.split('\x7f')[0])
        time_series.append(float(line.split('\x7f')[1]))
        line = f1.readline()
    f1.close()

        
    cluster_tag = []
    f2 = open(read_filename1)
    line = f2.readline()
    while line:
        cluster_tag.append(int(line.strip()))
        line = f2.readline()
    f2.close()
        
        
    i = 1
    k = 0
    # 第一个元素代表的聚类编号：1或2
    tag1 = 0
    tag2 = 0
            
    # 第一个元素代表的原始标记编号：整数
    tag3 = 0
        
    correct = 0
        
    while i < weibo_row:
        weibo_id = str(weibo_sheet.cell(i, 0).value).split('.')[0]
        weibo_time = weibo_sheet.cell(i, 2).value
        weibo_time = time_convert(weibo_time)
        weibo_tag = int(weibo_sheet.cell(i, 5).value)
      
        if weibo_id == id_series[k] and np.abs(weibo_time - time_series[k]) < 0.01:
            if k == 0:
                tag1 = cluster_tag[0]
                if tag1 == 1:
                    tag2 = 2
                else:
                    tag2 = 1
                    
                tag3 = weibo_tag

                correct += 1                
            else:
                if (cluster_tag[k] == tag1 and weibo_tag == tag3) or (cluster_tag[k] == tag2 and weibo_tag != tag3):
                    correct += 1
                        
            k += 1
            
        if k >= len(cluster_tag):
            break
            
        i += 1
        
    purity = str(np.true_divide(correct, len(cluster_tag)))
    
    quick_write_list_to_text([purity], write_filename)
        

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = 'D:/Local/DataStreamMining/dataset/cluster/c2/final_cluster_tag/5.txt'
    read_directory2 = 'D:/Local/DataStreamMining/dataset/cluster/c2/final_id_time/5.txt'
    read_filename3 = root_directory + u'dataset/mixture_topics/topics_data2.xlsx'
    write_filename = 'D:/Local/DataStreamMining/dataset/cluster/c2/purity5.txt'

    compute_purity(read_directory1, read_directory2, read_filename3, write_filename)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'