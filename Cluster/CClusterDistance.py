# -*- coding: utf-8 -*-
'''
Created on 2014年1月6日

@author: ZhuJiahui506
'''

import os
import time
from TextToolkit import quick_write_list_to_text
import numpy as np
from KLDistance import KL_distance

def compute_distance(read_directory1, read_directory2, read_directory3, write_filename, write_directory):
    #文件总数
    file_number = np.sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    
    center_d = []
    
    for i in range(file_number):
        center = np.loadtxt(read_directory1 + '/' + str(i + 1) + '.txt')
        center = center.T
        
        kl1 = KL_distance(center[0], center[1])
        kl2 = KL_distance(center[1], center[0])
        
        center_d.append(str(np.max([kl1, kl2])))
        
        cluster_data = np.loadtxt(read_directory2 + '/' + str(i + 1) + '.txt')
        cluster_data = cluster_data.T
        
        f = open(read_directory3 + '/' + str(i + 1) + '.txt')
        cluster_tag = f.readlines()
        f.close()
        
        final_distance = []
        distance1 = 0.0
        distance2 = 0.0
        count1 = 0
        count2 = 0
        for j in range(len(cluster_tag)):
            if cluster_tag[j].strip() == '1':
                kl1 = KL_distance(center[0], cluster_data[j])
                kl2 = KL_distance(cluster_data[j], center[0])
                distance1 += np.max([kl1, kl2])
                count1 += 1
            if cluster_tag[j].strip() == '2':
                kl1 = KL_distance(center[1], cluster_data[j])
                kl2 = KL_distance(cluster_data[j], center[1])
                distance2 += np.max([kl1, kl2])
                count2 += 1
                
        final_distance.append(str(np.true_divide(distance1, count1)))
        final_distance.append(str(np.true_divide(distance2, count2)))
        quick_write_list_to_text(final_distance, write_directory + '/' + str(i + 1) + '.txt')
    
    quick_write_list_to_text(center_d, write_filename)

        

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = 'D:/Local/DataStreamMining/dataset/cluster/c1/final_cluster_center'
    read_directory2 = 'D:/Local/DataStreamMining/dataset/cluster/c1/final_cluster_data'
    read_directory3 = 'D:/Local/DataStreamMining/dataset/cluster/c1/cluster_tag2'

    write_directory = 'D:/Local/DataStreamMining/dataset/cluster/c1/distance'
    write_filename = 'D:/Local/DataStreamMining/dataset/cluster/c1/center_d.txt'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    compute_distance(read_directory1, read_directory2, read_directory3, write_filename, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'