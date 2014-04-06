# -*- coding: utf-8 -*-
'''
Created on 2013年12月26日

@author: ZhuJiahui506
'''

def utility_f(id_pattern_dict, pattern_trans_dict, pattern_support_dict, sub_pattern_dict, f):
    '''
    计算每一个pattern的utility值
    
    :param id_pattern_dict: pattern的id与pattern所代表的事务中的项关系的字典  
    #类型：'id':int[item]
    
    :param pattern_trans_dict: pattern的id与含有该pattern的事务关系的字典  
    #类型：'id':int[trans]
    
    :param pattern_support_dict: pattern的id与含有该pattern的支持度（频数）关系的字典  
    #类型：'id':int
    
    :param sub_pattern_dict: pattern的id与该pattern的子pattern关系的字典  
    #类型：'id':str[psttern_id]
    
    :param f: false positive error 误报率
    '''
    
    #pattern的id与该pattern的utility值关系的字典
    #类型：'id':int   
    pattern_utility = {}
    #pattern的id与包含该pattern的事务列表关系的字典
    #类型：'id':int[trans]
    pattern_coverage_set = {}
    #pattern的id与可被该pattern替换的pattern的关系的字典
    #类型：'id':str[id]
    replaced_patterns = {}

    #遍历每一个频繁项pattern
    #此处的each是pattern的id
    for each in id_pattern_dict.keys():
        if len(id_pattern_dict[each]) == 1:
            pattern_utility[each] = 0
            pattern_coverage_set[each] = pattern_trans_dict[each]
            replaced_patterns[each] = [each]
        else:
            
            #初始化utility值
            pattern_utility[each] = len(id_pattern_dict[each]) * pattern_support_dict[each] - pattern_support_dict[each] - len(id_pattern_dict[each])
            #初始化pattern覆盖的事务集合
            pattern_coverage_set[each] = pattern_trans_dict[each]
            #初始化pattern能够替换的其他pattern集合，包含本身
            replaced_patterns[each] = [each]
        
            area = len(id_pattern_dict[each]) * pattern_support_dict[each]
            fp_error = 0
            #trans = []
    
            #sort is already done
        
            #此处的each_sub是pattern的子pattern的id
            for each_sub in sub_pattern_dict[each]:
                if len(id_pattern_dict[each_sub]) >= ((len(id_pattern_dict[each]) + 1) / 2.0):
                    new_trans = [x for x in pattern_trans_dict[each_sub] if x not in pattern_coverage_set[each]]
                    #trans = list(set(trans).union(set(new_trans)))
                
                    new_area = area + len(id_pattern_dict[each]) * len(new_trans)
                
                    new_error = fp_error + (len(id_pattern_dict[each]) - len(id_pattern_dict[each_sub])) * len(new_trans)
                
                    if float(new_error) / new_area <= f:
                    #更新当前pattern的utility值
                        pattern_utility[each] = pattern_utility[each] + len(new_trans) * (2 * len(id_pattern_dict[each_sub]) - len(id_pattern_dict[each]) - 1)
                        pattern_coverage_set[each] = list(set(pattern_coverage_set[each]).union(new_trans))
                        replaced_patterns[each] = list(set(replaced_patterns[each]).union(each_sub))
                        area = new_area
                        fp_error = new_error
                    else:
                        break
                else:
                    break
    
    #无需返回replaced_patterns
    return pattern_utility, pattern_coverage_set



if __name__ == '__main__':
    pass