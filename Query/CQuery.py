# coding: utf-8
'''
Created on 2013年12月11日

@author: ZhuJiahui506
'''

import os
from TextToolkit import get_text_to_complex_list, quick_write_list_to_text
from operator import itemgetter
from datetime import datetime

def query_time_format(time_interval):
    '''
    2013-01-01----41275
    :param time_interval:
    '''
    
    result_time = []
    each_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    for each in time_interval:
        data_list = each.strip().split('-')
        data_list = [int(x) for x in data_list]
        this_result = 41274
        
        for i in range(data_list[1] - 1):
            this_result += each_month_days[i]
        
        this_result += data_list[-1]
        result_time.append(this_result)
    
    return result_time 
    

def vsm_map_word(vsm, all_word_list):
    '''
    
    :param vsm:
    :param all_word_list:
    '''
    result = []
    for i in range(len(vsm)):
        if float(vsm[i]) > 0.0001:
            result.append(all_word_list[i])
    
    return result
        

def cquery(keyword_list, mode, time_interval, select, read_directory1, read_directory2, write_filename):
    '''
    
    :param keyword_list:
    :param mode:
    :param time_interval:
    :param select:
    :param read_directory1: 数据总目录
    :param read_directory2: 索引目录
    :param write_filename:
    '''

    if len(time_interval) != 2:
        print "Set Time Error!"
        return
    
    if (mode != "AND") and (mode != "OR"):
        print "Mode Error!"
        return
    
    start = time_interval[0]
    end = time_interval[1]
    
    #文件个数
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory2)])
    
    query_result = []
    entropy_result = []
    
    #当前目录下进行搜索
    for i in range(file_number):
        #读取时间信息
        f = open(read_directory1 + '/update_id_time/' + str(i + 1) + '.txt')
        time_lines = f.readlines()
        f.close()
        
        #当前片的最晚时间比查询设定的开始时间还早，则跳过该片
        if float(time_lines[-1].strip().split()[-1]) < start:
            #print float(time_lines[-1].strip().split()[-1])
            pass
        #当前片的最早时间比查询设定的结束时间晚，则结束
        elif float(time_lines[-1].strip().split()[-1]) > end:
            
            break
        else:
            #压缩后的数据项对应原始数据的索引
            f1 = open(read_directory2 + '/' + str(i + 1) + '.txt')
            data_index = f1.readlines()
            data_index = [int(x) for x in data_index]
            #print data_index
            f1.close()
            
            #数据的VSM表示的向量
            each_weibo_vsm = []
            get_text_to_complex_list(each_weibo_vsm, u'D:/Local/DataStreamMining/dataset/non_orthogonal/topics_data1/重构数据/' + str(i + 1) + '.txt', 0)
            
            #VSM所对应的词汇列表
            word_list = []
            f4 = open(read_directory1 + '/top_n_word/' + str(i + 1) + '.txt')
            word_lines = f4.readlines()
            f4.close()
            for each in word_lines:
                word_list.append(each.strip().split()[0])
            
            #信息熵值列表
            f5 = open(read_directory1 + '/entropy/' + str(i + 1) + '.txt')
            entropy_list = f5.readlines()
            f5.close()
            entropy_list = [float(x.strip()) for x in entropy_list]

            #每一个数据片中逐行遍历
            for j in range(len(time_lines)):
                #当前遍历时的时间
                now_t = float(time_lines[j].strip().split()[-1])
                
                if (now_t >= start) and (now_t <= end) and (j in data_index):
                    if mode == "OR":
                        flag = 0
                        for each1 in keyword_list:
                            for k in range(len(word_list)):
                                if (each1 in word_list[k]) and (float(each_weibo_vsm[j][k]) > 0.000001):
                                    this_message = " ".join(vsm_map_word(each_weibo_vsm[j], word_list))
                                    if this_message not in query_result:
                                        query_result.append(this_message)
                                        entropy_result.append(entropy_list[j])
                                    flag = 1
                                    break
                            if flag == 1:
                                break
                    else:
                        flag = 0
                        for each1 in keyword_list:
                            for k in range(len(word_list)):
                                if (each1 in word_list[k]) and (float(each_weibo_vsm[j][k]) > 0.000001):
                                    flag += 1
                                    break
                                
                        if flag == len(keyword_list):
                            this_message = " ".join(vsm_map_word(each_weibo_vsm[j], word_list))
                            if this_message not in query_result:
                                query_result.append(this_message)
                                entropy_result.append(entropy_list[j])
     
    #按熵值降序排序
    el = zip(entropy_result, query_result)
    el1 = sorted(el, key = itemgetter(0), reverse = True)
    #选择对应的行号索引
    query_result2 = []
    count_number = 1
    for each in el1:
        query_result2.append(each[1])
        count_number += 1
        if count_number > select:
            break    
    
    quick_write_list_to_text(query_result2, write_filename)

if __name__ == '__main__':
    start = datetime.now()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory1 = root_directory + u'dataset/batch_data_segment/topics_data1'
    read_directory2 = root_directory + u'dataset/pyramid/topics_data1/index'
    
    write_directory = root_directory + u'dataset/query/topics_data1'
    
    if (not(os.path.exists(root_directory + u'dataset/query'))):
        os.mkdir(root_directory + u'dataset/query')
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)

    keyword_list = ["李", "天一"]
    mode = "AND"
    time_interval = ["2013-07-01", "2013-07-10"]
    time_interval = query_time_format(time_interval)
    select = 30
    print time_interval
    write_filename = write_directory + u'/q2.txt'
    
    cquery(keyword_list, mode, time_interval, select, read_directory1, read_directory2, write_filename)
    
    print 'Total time %d seconds' % ((datetime.now() - start).seconds)
    print 'Complete !!!'
    