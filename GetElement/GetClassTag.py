#coding:utf-8
'''
Created on 2013年11月10日

@author: ZhuJiahui
'''
import os
from ExcelToolkit import open_sheet
from datetime import datetime

def get_class_tag(read_filename, write_filename):
    weibo_sheet = open_sheet(read_filename)
    weibo_row = weibo_sheet.nrows
    all_weibo_class_tag = ''
    
    f = open(write_filename, 'w')
    
    for i in range(1, weibo_row):
        all_weibo_class_tag += str(int(weibo_sheet.cell(i, 5).value))
        all_weibo_class_tag += '\n'
    
    f.write(all_weibo_class_tag)
    f.close

if __name__ == '__main__':
    start = datetime.now()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory)

    read_filename = root_directory + u'/dataset/mixture_topics/王菲薛蛮子类别标注.xlsx'
    write_filename = root_directory + u'/dataset/class_tag/王菲薛蛮子.txt'
    get_class_tag(read_filename, write_filename)
    print '总共花了 %d 秒' % ((datetime.now() - start).seconds)
    print "complete"