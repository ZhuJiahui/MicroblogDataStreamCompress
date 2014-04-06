'''
@author: ZhuJiahui506
'''
import os
import numpy as np
from TextToolkit import quick_write_list_to_text2

if __name__ == '__main__':
    read_directory = 'D:/Local/FTP/gsod_2013'
    file_number = np.sum([len(files) for root, dirs, files in os.walk(read_directory)])
    write_filename = 'D:/Local/FTP/2013_all.op'
    
    result = []
    for i in range(file_number):
        f1 = open(read_directory + '/1 (' + str(i + 1) + ').op')
        each_file = f1.readlines()
        f1.close()
        
        for each in each_file:
            result.append(each)
    
    quick_write_list_to_text2(result, write_filename)
    print "Complete"    
        