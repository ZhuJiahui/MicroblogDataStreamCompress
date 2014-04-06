# -*- coding: utf-8 -*-
'''
Created on 2014年2月21日

@author: ZhuJiahui506
'''
from TextToolkit import quick_write_list_to_text

if __name__ == '__main__':
    read_filename = 'dataset/TextVector.txt'
    write_filename = 'dataset/TextVector11.txt'
    data_list = []
    result = []
    
    f = open(read_filename, 'r')
    line = f.readline()
    while line:
        aa = line.strip().split()
        bb = [int(each1) for each1 in aa]
        cc = [str(each2) for each2 in bb]
        data_list.append(" ".join(cc))
        line = f.readline()
    f.close()

    quick_write_list_to_text(data_list, write_filename)
    
    print 'Complete!!!'