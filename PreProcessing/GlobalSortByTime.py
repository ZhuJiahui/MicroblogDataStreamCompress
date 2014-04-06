# -*- coding: utf-8 -*-
'''
Created on 2013年12月12日
Last on 2013年12月12日

As the original data is too big
In convenient of the later processing, we sort after segmentation 

@author: ZhuJiahui506
'''
import os
from datetime import datetime
from operator import itemgetter
from TextToolkit import quick_write_list_to_text, write_list_to_text_by_row


def generate_sort_index(read_directory, write_directory):
    '''
    排序索引的产生
    :param read_directory:
    :param write_directory:
    '''
    time_series = []
    item_index = []
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    
    for i in range(file_number):
        line_count = 1
        f = open(read_directory + '/' + str(i + 1) + '.txt', 'rb')
        line = f.readline()
        while line:
            if line_count % 9 == 6:
                time_series.append(float(line.strip()[13:]))
                item_index.append([str(i + 1), str(line_count)])
            line = f.readline()
            line_count += 1
        f.close()
    
    #按时间升序排序
    tsi = zip(time_series, item_index)
    tsi1 = sorted(tsi, key = itemgetter(0))
            
    #选择对应的行号索引
    update_item_index = []
    for each in tsi1:
        update_item_index.append(each[1])
    
    write_list_to_text_by_row(update_item_index, write_directory + u'/update_item_index.txt')
    
    return update_item_index



def global_sort_by_time(update_item_index, read_directory, write_directory):
    
    print "Begin sorting." 
    print "May take a long time, Please Wait..."
    line_count = 1
    file_count = 880
    review_result = []
    
    for i in range(len(update_item_index)):
        
        f1 = open(read_directory + "/" + update_item_index[i][0] + ".txt", "rb")
        each_review_text = f1.readlines()
        f1.close()
        
        #try:
        time_index = int(update_item_index[i][1])
        review_result.append(each_review_text[time_index - 6].strip())
        review_result.append(each_review_text[time_index - 5].strip())
        review_result.append(each_review_text[time_index - 4].strip())
        review_result.append(each_review_text[time_index - 3].strip())
        review_result.append(each_review_text[time_index - 2].strip())
        review_result.append(each_review_text[time_index - 1].strip())
        review_result.append(each_review_text[time_index].strip())
        review_result.append(each_review_text[time_index + 1].strip())
        review_result.append("")
        
        #except IndexError:
            #review_result.append("\n")
               
        line_count += 1
        
        if line_count > 5000:
            quick_write_list_to_text(review_result, write_directory + "/" + str(file_count) + ".txt")
            
            review_result = []
            line_count = 1
            file_count += 1
            
    print "Sort Complete!!!"


if __name__ == "__main__":

    start = datetime.now()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset/batch_data_segment/Music/original_data'
    
    write_directory1 = root_directory + u'dataset/batch_data_segment/Music'
    write_directory2 = root_directory + u'dataset/batch_data_segment/Music/sort_original_data'
    
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)
    
    #update_item_index = generate_sort_index(read_directory, write_directory1)
    
    update_item_index = []
    f = open(root_directory + u'dataset/batch_data_segment/Music/update_item_index.txt')
    line = f.readline()
    while line:
        update_item_index.append(line.split())
        line = f.readline()    
    f.close()
    
    
    update_item_index = update_item_index[4395000:4895000]
        
    global_sort_by_time(update_item_index, read_directory, write_directory2)
    
    print 'Total time: %d seconds' % ((datetime.now() - start).seconds)
    print 'Complete !!!'
    
