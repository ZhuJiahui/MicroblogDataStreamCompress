#coding:utf-8
'''
Created on 2013年12月26日

@author: ZhuJiahui506
'''

from SPUR import replace_trans_with_pattern

if __name__ == '__main__':
    o_trans = [[1,2,3,4,5],[1,3,5],[1,2,5]]
    pattern_key = '2'
    pattern_value = [1,3,5]
    coverage_set = [0,1,2]
    
    replace_trans_with_pattern(o_trans, pattern_key, pattern_value, coverage_set)    
    
    print o_trans