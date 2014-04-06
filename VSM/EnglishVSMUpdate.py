# -*- coding: utf-8 -*-
'''
Created on 2013年11月28日

@author: ZhuJiahui506
'''

import os
import time
import numpy as np
from TextToolkit import quick_write_list_to_text2


def vsm_update(read_directory1, read_directory2, write_directory1, write_directory2):
    '''
    除去全0的行
    :param read_directory1:
    :param read_directory2:
    :param write_directory1:
    :param write_directory2:
    '''
    file_number = np.sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    for i in range(file_number):
        update_vsm = []
        update_phst = [] 
        
        f1 = open(read_directory1 + '/' + str(i + 1) + '.txt')
        each_weibo_vsm = f1.readlines()
        f1.close()
        
        f2 = open(read_directory2 + '/' + str(i + 1) + '.txt')
        phst = f2.readlines()
        f2.close()
        
        for j in range(len(each_weibo_vsm)):
            int_each_weibo_vsm = [int(x) for x in each_weibo_vsm[j].split()]
            #去掉全0行
            if np.sum(int_each_weibo_vsm) > 0.1:
                update_vsm.append(each_weibo_vsm[j])
                update_phst.append(phst[j])

        quick_write_list_to_text2(update_vsm, write_directory1 + '/' + str(i + 1) + '.txt')
        quick_write_list_to_text2(update_phst, write_directory2 + '/' + str(i + 1) + '.txt')
    
    print "VSM Update Complete!!!"

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset/batch_data_segment/Music/Music2/vsm'
    read_directory2 = root_directory + u'dataset/batch_data_segment/Music/Music2/phst'
    write_directory1 = root_directory + u'dataset/batch_data_segment/Music/Music2/update_vsm'
    write_directory2 = root_directory + u'dataset/batch_data_segment/Music/Music2/update_phst'
    
    if (not(os.path.exists(write_directory1))):
        os.mkdir(write_directory1)
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)
    
    vsm_update(read_directory1, read_directory2, write_directory1, write_directory2)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
