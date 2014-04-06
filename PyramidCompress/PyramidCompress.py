# -*- coding: utf-8 -*-
'''
Created on 2013年12月2日
Last on 2013年12月4日
@author: ZhuJiahui506
'''

import os
from TextToolkit import quick_write_list_to_text
from operator import itemgetter
from datetime import datetime

def pyramid_index(total):
    '''
    产生合并压缩的索引
    :param total:文件总个数
    '''
    
    #金字塔初始设置
    level_element = [2]
    pyramid_all = [[1,2]]
    
    #以2片数据为单位进行压缩
    for i in range(4, total + 1, 2):
        flag = 0
        level = len(pyramid_all)
        
        for j in range(level - 1, -1, -1):
            if (len(pyramid_all[j]) < level_element[j]):
                # 若某一层未满，则合并压缩
                pyramid_all[j] += pyramid_all[j + 1]
                pyramid_all.remove(pyramid_all[j + 1])
                pyramid_all.append([i - 1, i])
                flag = 1
                break;
        
        # 若所有层均满，则新建一层
        if flag == 0:
            pyramid_all.append([i - 1, i])
            level_element.insert(0, 2 ** (level + 1))
    
    return pyramid_all


def pyramid_compress(compress_index, read_directory1, read_directory2, write_directory1, write_directory2):
    '''
    根据产生的金字塔索引进行压缩
    :param compress_index:
    :param read_directory1:
    :param read_directory2:
    :param write_directory1:
    :param write_directory2:
    '''
    
    #设置每一层窗口的大小
    gram = 4096
    
    #遍历所有的层
    for i in range(len(compress_index)):
        #根据压缩的规律选择该层的每个数据片的信息条数
        select = gram // len(compress_index[i])     
        
        #每一层的所有数据片压缩后的数据列表
        level_result = []
        
        #遍历每一层的每一个数据片编号
        for j in range(len(compress_index[i])):
            entropy = []
            line_count = 0
            line_index = []
            
            #读取熵值和行数索引编号，作为待排序的数据项
            f = open(read_directory2 + '/' + str(compress_index[i][j]) + '.txt')
            line = f.readline()
            while line:
                line_index.append(line_count)
                entropy.append(float(line.strip()))  #注意此处的float不可少
                line = f.readline()
                line_count += 1
            f.close()
            
            #按熵值降序排序
            el = zip(entropy, line_index)
            el1 = sorted(el, key = itemgetter(0), reverse = True)
            
            #选择对应的行号索引
            update_index = []
            for each in el1:
                update_index.append(each[1])
            
            #选择前select项行号索引
            #进行升序排序，确保压缩后的信息的相对位置不变
            update_index = update_index[:select]
            update_index.sort()
            update_index2 = [str(x) for x in update_index]
            quick_write_list_to_text(update_index2, write_directory2 + '/' + str(compress_index[i][j]) + '.txt')
            
            #定义该片数据中选取的信息列表，二维
            this_result = []
            for k in range(len(update_index)):
                this_result.append([])
            
            #注意，读入的数据每一列代表一条信息
            #因此，处理较为不便，要根据选择的行号索引跳跃式地一个个获取每一个元素
            #若条件允许，可先将其转置，则可按行直接选取
            f = open(read_directory1 + '/' + str(compress_index[i][j]) + '.txt')
            line = f.readline()
            while line:
                line_element = line.strip().split()
                for k in range(len(update_index)):
                    this_result[k].append(line_element[update_index[k]])
                line = f.readline()
            f.close()
            
            #将当前层的该片数据选出的信息加入该层的所有数据片压缩后的数据列表（该层的结果列表）
            for each in this_result:
                level_result.append(" ".join(each))
        
        #一层遍历完后，将该层的所有数据片压缩后的数据列表（该层的结果列表）写入文件
        #写入后每一行代表一条信息（未压缩的数据每一列代表一条信息）
        quick_write_list_to_text(level_result, write_directory1 + '/' + str(i + 1) + '.txt')    
        
    
if __name__ == '__main__':
    start = datetime.now()
    
    #获取当前目录
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    #注意此处的采样信号目录不在当前工程文件夹下
    read_directory1 = u'D:/Local/DataStreamMining/dataset/non_orthogonal/topics_data1/采样信号'
    read_directory2 = root_directory + u'dataset/batch_data_segment/topics_data1/entropy'
    write_directory1 = root_directory + u'dataset/pyramid/topics_data1/data'
    write_directory2 = root_directory + u'dataset/pyramid/topics_data1/index'
    
    if (not(os.path.exists(root_directory + u'dataset/pyramid/topics_data1'))):
        os.mkdir(root_directory + u'dataset/pyramid/topics_data1')
    if (not(os.path.exists(write_directory1))):
        os.mkdir(write_directory1)
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)
    
    #待压缩的数据片总数
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory1)])
    #file_number = 100
    
    #生成压缩金字塔索引
    compress_index = pyramid_index(file_number)
    
    lines = []
    for each_line in compress_index:
        lines.append(" ".join([str(x) for x in each_line]))
        
    quick_write_list_to_text(lines, root_directory + u'dataset/pyramid/topics_data1/pyramid_index.txt')
    
    #按生成的索引压缩
    pyramid_compress(compress_index, read_directory1, read_directory2, write_directory1, write_directory2)
    
    print 'Total time: %d seconds' % ((datetime.now() - start).seconds)
    print 'Complete !!!'

