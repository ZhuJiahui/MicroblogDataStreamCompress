# -*- coding: utf-8 -*-
'''
Created on 2013年7月10日

@author: ZhuJiahui
'''

def heapify(list1, heapSize, index, list2):
    '''
    将index节点制作成堆
    :param list1:
    :param heapSize:
    :param index:
    :param list2: 非搜索关键字列表
    '''
    left = 2 * index + 1
    right = left + 1
    large = index
    if right < heapSize and list1[large] < list1[right]:
        large = right
    if left < heapSize and list1[large] < list1[left]:
        large = left
    if large != index:
        list1[large], list1[index] = list1[index], list1[large]
        list2[large], list2[index] = list2[index], list2[large]
        heapify(list1, heapSize, large, list2)
 
def build_max_heap(list1, list2):
    '''
    创建一个最大堆（初始化堆）
    :param list1:
    :param list2:
    '''
    heapSize = len(list1)
    for i in range(heapSize / 2 - 1, -1, -1):
        heapify(list1, heapSize, i, list2)
 
def heap_sort(list1, list2):
    '''
    堆排序时间
    :param list1:
    :param list2:
    '''
    build_max_heap(list1, list2)
    for i in range(len(list1) - 1, -1, -1):
        list1[0], list1[i] = list1[i], list1[0]  # move the largest value to the end
        list2[0], list2[i] = list2[i], list2[0]
        heapify(list1, i, 0, list2)
    return list1, list2

