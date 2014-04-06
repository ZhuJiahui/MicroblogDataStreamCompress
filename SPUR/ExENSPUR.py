# -*- coding: utf-8 -*-
'''
Created on 2013年12月22日

@author: ZhuJiahui506
'''


import os
from TextToolkit import quick_write_list_to_text
import time

def generate_transactions(read_filename):
    '''
    将向量空间矩阵转化为事务列表
    :param read_filename: 向量空间文件
    '''
    trans = []
    trans_size = 0
    
    f = open(read_filename)
    vsm = f.readlines()
    f.close()
    
    #每一行是一个事务，事务由项组成
    for each in vsm:
        vsm_line = each.split()
        this_line = []
        for i in range(len(vsm_line)):
            if float(vsm_line[i]) > 0.1:
                this_line.append(i)
        
        trans_size += len(this_line)
        trans.append(this_line)
    
    #返回向量空间的事务表示，同时返回总项数（每一行是一个事务，事务由项组成）
    #trans是int型的二维列表
    return trans, trans_size
     

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset/batch_data_segment/Music/Music5/update_vsm'
    
    write_directory1 = root_directory + u'dataset/spur/Music5/compress'
    write_directory2 = root_directory + u'dataset/spur/Music5'
    
    if (not(os.path.exists(root_directory + u'dataset/spur'))):
        os.mkdir(root_directory + u'dataset/spur')
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)
    if (not(os.path.exists(write_directory1))):
        os.mkdir(write_directory1)
    
    result = []
    trans, trans_size = generate_transactions(read_directory + '/47.txt')
    for each in trans:
        result.append(" ".join([str(x) for x in each]))
    
    quick_write_list_to_text(result, write_directory1 + '/47.txt')
    
    print 'Total time %f seconds' % (time.clock() - start) 
    print 'Complete !!!'