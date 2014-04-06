# -*- coding: utf-8 -*-
'''
Created on 2013年12月22日

@author: ZhuJiahui506
'''


import os
import numpy as np
from fp_growth import find_frequent_itemsets
from operator import itemgetter
from TextToolkit import quick_write_list_to_text, write_list_to_text_by_row
from Utility import utility_f
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


def replace_trans_with_pattern_strict(o_trans, pattern_key, pattern_value):
    for i in range(len(o_trans)):
        if set(o_trans[i]) & set(pattern_value) == set(pattern_value):
            for j in range(len(o_trans[i])):
                if o_trans[i][j] in pattern_value:
                    o_trans[i][j] = pattern_key
            
            o_trans[i] = list(set(o_trans[i]))
            
def replace_trans_with_pattern(o_trans, pattern_key, pattern_value, coverage_trans):
    for each in coverage_trans:
        for i in range(len(o_trans[each])):
            if o_trans[each][i] in pattern_value:
                o_trans[each][i] = pattern_key
        
        o_trans[each] = list(set(o_trans[each]))

            
def spur(read_directory, write_directory1, write_directory2):
    '''
    SPUR压缩
    Summarization via Pattern Utility and Ranking
    Summarize a batch of transactions with low compression ratio and high quality.
    
    Xintian Yang, Amol Ghoting, Yiye Ruan, A Framework for Summarizing and Analyzing Twitter Feeds, KDD'12,August 12–16, 2012, Beijing, China.
    
    :param read_directory: VSM文件目录
    :param write_directory1: 压缩结果文件目录
    :param write_directory2: 压缩比例文件目录
    '''
    
    #频繁项集挖掘的支持度
    minimun_support = 80
    
    #误报率
    f = 0.1
    
    #压缩比率
    ratio = []
    
    #压缩时间
    compress_time = []
    
    #文件总数
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    
    #循环遍历所有VSM文件
    for i in range(file_number):
        print 'Batch: %d' % (i + 1)
        start = time.clock()
        
        '''
        #挖掘频繁项集，并得到相应的频繁项集的支持度
        #频繁项集挖掘采用FP-Growth算法
        #参考 https://github.com/enaeseth/python-fp-growth
        '''
        o_trans, trans_size = generate_transactions(read_directory + '/' + str(i + 1) + '.txt')
        print trans_size
        
        #压缩预算，压缩的上限是原始事务中的总项数items的0.6
        #M = 0.7 * trans_size
        #M = 85000
        M = 30000
        #频繁项及其对应的长度、支持度的列表
        frequent_patterns = []  #二维int列表
        length_all = []
        support_all = []
        
        #find_frequent_itemsets返回的结果类型为"generator"
        #The type of the return of the "find_frequent_itemsets" is "generator"
        for each, support in find_frequent_itemsets(o_trans, minimun_support, include_support=True):
            each.sort()
            frequent_patterns.append(each)
            length_all.append(len(each))
            support_all.append(support)
        
        print len(frequent_patterns)           
        #频繁项按照长度由高到低排序
        fl = zip(frequent_patterns, length_all, support_all)
        fl1 = sorted(fl, key = itemgetter(1), reverse = True)
        
        '''
        #为便于表示原始事务，每一个频繁项pattern用一个字符串来表示，作为其id
        #每一个pattern的表示格式"p*"，*为数字，从0开始
        '''
        #pattern的id与pattern所代表的事务中的项关系的字典
        #类型：'id':int[item]
        id_pattern_dict = {}
        #pattern的id与pattern的长度关系的字典
        #类型：'id':int
        pattern_length_dict = {}
        #pattern的id与pattern的支持度关系的字典
        #类型：'id':int
        pattern_support_dict = {}
        
        id1 = 0
        for each in fl1:
            id_pattern_dict['p' + str(id1)] = each[0]
            pattern_length_dict['p' + str(id1)] = each[1]
            pattern_support_dict['p' + str(id1)] = each[2]         
            id1 += 1
            if id1 >= 9000:
                break
            
        id2 = 9000
        for each in fl1[(len(fl1) - 1) : (len(fl1) - 1001) : -1]:
            id_pattern_dict['p' + str(id2)] = each[0]
            pattern_length_dict['p' + str(id2)] = each[1]
            pattern_support_dict['p' + str(id2)] = each[2]

        #pattern的id与含有该pattern的事务关系的字典
        #事务的编号的排列方式以原始事务顺序为依据，为int型
        #类型：'id':int[trans]
        pattern_trans_dict = {}
        for each in id_pattern_dict.keys():
            value_list = []
            for j in range(len(o_trans)):
                if set(id_pattern_dict[each]).issubset(o_trans[j]):  #后面无需集合化
                    value_list.append(j)
            
            pattern_trans_dict[each] = value_list
        
        #获取每个频繁项的子频繁项，不包含本身
        #类型：'id':str[id]
        sub_pattern_dict = {}
        #获取每个频繁项的父频繁项，不包含本身
        #类型：'id':str[id]
        super_pattern_dict = {}
        #获取每个与每个频繁项相交的但不属于以上2种情况的频繁项
        #类型：'id':str[id]
        overlap_pattern_dict = {}
        for each in id_pattern_dict.keys():
            value_list1 = []
            value_list2 = []
            value_list3 = []
            for each1 in id_pattern_dict.keys():
                if each != each1:
                    intersection = set(id_pattern_dict[each1]) & set(id_pattern_dict[each])
                    if intersection == set():
                        pass
                    elif set(id_pattern_dict[each1]) == intersection:
                        value_list1.append(each1)
                    elif set(id_pattern_dict[each]) == intersection:
                        value_list2.append(each1)
                    else:
                        value_list3.append(each1)
                else:
                    pass
            
            sub_pattern_dict[each] = value_list1
            super_pattern_dict[each] = value_list2
            overlap_pattern_dict[each] = value_list3
        
        '''
        初始化utility值
        返回pattern的id与该pattern的utility值关系的字典
        返回pattern的id与包含该pattern的事务列表关系的字典
        '''
        pattern_utility , pattern_coverage_set = utility_f(id_pattern_dict, pattern_trans_dict, pattern_support_dict, sub_pattern_dict, f)
        
        #获取utility值最大的pattern
        max_index = np.argmax(pattern_utility.values())
        Q_top = pattern_utility.keys()[max_index]
        
        #pattern_utility的复制
        Q_utility = pattern_utility.copy()
        
        '''
        将原始事务用当前pattern表示，根据utility进行
        同时不断更新utility值
        '''
        #current_size = trans_size
        current_size = 0
        iter_count = 0
        
        while current_size < M:
            #当前选择的pattern
            this_pattern = Q_top
            
            if Q_utility[this_pattern] >= 0.0:
                
                '''
                  #用当前频繁项this_pattern表示原始事务
                  #this_pattern是该pattern的键，是一个字符串
                  '''
                replace_trans_with_pattern(o_trans, this_pattern, id_pattern_dict[this_pattern], pattern_coverage_set[this_pattern])
                #此时，o_trans已经改变
                #注意，之后o_trans中既包含int型，又包含string型
                
                '''
                  当前pattern表示完后，更新其余pattern的utility值
                  '''
                for each1 in super_pattern_dict[this_pattern]:
                    covered_set = set(pattern_coverage_set[each1]) & set(pattern_coverage_set[this_pattern])
                    pattern_utility[each1] = pattern_utility[each1] - len(id_pattern_dict[this_pattern]) * len(covered_set)
                    if each1 in Q_utility.keys():
                        Q_utility[each1] = pattern_utility[each1]
                
                for each2 in sub_pattern_dict[this_pattern]:
                    covered_set = set(pattern_coverage_set[each2]) & set(pattern_coverage_set[this_pattern])
                    pattern_utility[each2] = pattern_utility[each2] - (len(id_pattern_dict[each2]) - 1) * len(covered_set)
                    
                    if each2 in Q_utility.keys():
                        Q_utility[each2] = pattern_utility[each2]
                    
                    pattern_coverage_set[each2] = [x for x in pattern_coverage_set[each2] if x not in covered_set]
                    if (len(pattern_coverage_set[each2]) == 0) and (each2 in Q_utility.keys()):
                        del Q_utility[each2]
                
                for each3 in overlap_pattern_dict[this_pattern]:
                    covered_set = set(pattern_coverage_set[each3]) & set(pattern_coverage_set[this_pattern])
                    pattern_utility[each3] = pattern_utility[each3] - len(covered_set) * len(set(id_pattern_dict[each3]) & set(id_pattern_dict[this_pattern]))
                    if each3 in Q_utility.keys():
                        Q_utility[each3] = pattern_utility[each3]
                
                #if len(pattern_coverage_set[this_pattern]) == 0:
                    #flag += 1
                #else:
                    #flag = 0
                    
                current_size = current_size + len(pattern_coverage_set[this_pattern])
                iter_count += 1
                if iter_count >= 20000:
                    break
                
                #if flag == 3:
                    #break
                #current_size = np.sum([len(x) for x in o_trans])
                #print current_size
                
                #当前pattern已表示过 删除之
                del Q_utility[this_pattern]
                
                #重新按照utility值降序排序 选取utility值最大的一项
                if Q_utility != {}:
                    max_index = np.argmax(Q_utility.values())
                    Q_top = Q_utility.keys()[max_index]
                else:
                    break
                            
            else:
                break  
        
        #final_size = np.sum([len(x) for x in o_trans])

        final_size = current_size
        print 'Final size: ', final_size
        this_ratio = np.true_divide(final_size, trans_size)
        print 'Ratio: ', this_ratio
        
        ratio.append(str(this_ratio))
        
        interval = time.clock() - start
        print 'Time: %f' % interval
        compress_time.append(str(interval))
        
        write_list_to_text_by_row(o_trans, write_directory1 + '/' + str(i + 1) + '.txt') 
    
    quick_write_list_to_text(ratio, write_directory2 + '/ratio.txt')
    quick_write_list_to_text(compress_time, write_directory2 + '/compress_time.txt')
        

if __name__ == '__main__':

    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    #read_directory = root_directory + u'dataset/batch_data_segment/Music/Music5/update_vsm'
    read_directory = root_directory + u'dataset/batch_data_segment/topics_data2/update_vsm'
    #read_filename = root_directory + u'dataset/batch_data_segment/Music/Music5/update_vsm/1.txt'
    #o_trans = [[1,2,5],[1,2,3],[3,4,5],[2,4,5],[2,3,5]]
    #o_trans = generate_transactions(read_filename)
    #minimun_support = 60
    #frequent_patterns = find_frequent_itemsets(o_trans, minimun_support)
    
    #print type(frequent_patterns)
    
    write_directory1 = root_directory + u'dataset/spur/topics_data2/compress'
    write_directory2 = root_directory + u'dataset/spur/topics_data2'
    
    if (not(os.path.exists(root_directory + u'dataset/spur'))):
        os.mkdir(root_directory + u'dataset/spur')
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)
    if (not(os.path.exists(write_directory1))):
        os.mkdir(write_directory1)
        
    spur(read_directory, write_directory1, write_directory2)
        
    print 'SPUR Complete !!!'