# -*- coding: utf-8 -*-
"""
Created on Tue May  7 21:39:48 2019

@author: 95713
"""
import numpy as np
import pandas as pd 
import re
import pickle
def odd_internal(start, end):
    '''
    生成区间内的奇数序列
    '''
    if start % 2 == 0:
        return np.arange(start+1, end+1, 2, int)
    else:
        return np.arange(start, end+1, 2, int)
    
def even_internal(start, end):
    '''
    生成区间内的偶数序列
    '''
    if start % 2 == 0:
        return np.arange(start, end+1, 2, int)
    else:
        return np.arange(start+1, end+1, 2, int)
    
#读取原始数据
course = pd.read_excel('./course.xls')

#数据预处理，删除一些多余信息
del course['Unnamed: 12']
workday = ['Mon','Tues','Wed','Thur','Fri']
data_columns = ['major']
for i in workday:
    for j in range(1,6):
        data_columns.append(i+str(j))
data_index = [i for i in range(238)]
    
course = course.drop([0,1,2])
course.columns = data_columns
course.index = data_index

#生成一学期的所有专业所有时间内的课程矩阵，专业之间以字典形式组织
major_dict = {}

pattern = re.compile(r'\[[^\[\]]*\]\[[^\[\]]*\]\[[^\[\]]*\]')#查找课程中的有用信息
pattern1 = re.compile(r'\]\[.*\]\[')#查找上课的周数
pattern2 = re.compile(r'\d\d*')


for i in range(course.shape[0]):
    temp_major = course.at[i,'major']#专业
    temp_course = course.iloc[i,:].tolist()[1:]#该专业的所有课
    temp_matrix = np.zeros((18,25),dtype = int)#有无课时的矩阵
    for j in range(len(temp_course)):
        sub_course = temp_course[j]
        try:
            sub_course = sub_course.replace('\n','')
            result = pattern.findall(sub_course)#list,可能有好几种课
            for sub_result in result:
                result1 = pattern1.findall(sub_result)[0][2:-2]#上课周数字符串
                
                week_list = pattern2.findall(result1)
                max_size = max([int(i) for i in week_list])
                if max_size > len(temp_matrix):
                    add_matrix = np.zeros((max_size - len(temp_matrix), 25), dtype = int)
                    temp_matrix = np.r_[temp_matrix, add_matrix]
                
                result1 = result1.split(',')
                
                if '单周' in result1:
                    result1 = result1[:-1]
                    for sub_result1 in result1:
                        week_list = pattern2.findall(sub_result1)
                        if len(week_list) == 1 and week_list[0] % 2 != 0:
                            temp_matrix[int(week_list[0]) - 1, j] = 1
                            
                        else:
                            temp_week = odd_internal(int(week_list[0]), int(week_list[1]))
                            temp_matrix[temp_week - 1, j] = 1
                            
                elif '双周' in result1:
                    result1 = result[:-1]
                    for sub_result1 in result1:
                        week_list = pattern2.findall(sub_result1)
                        if len(week_list) == 1 and week_list[0] % 2 == 0:
                            temp_matrix[int(week_list[0]) - 1, j] = 1
                            
                        else:
                            temp_week = even_internal(int(week_list[0]), int(week_list[1]))
                            temp_matrix[temp_week - 1, j] = 1
                            
                else:
                    for sub_result1 in result1:
                        week_list = pattern2.findall(sub_result1)
                        if len(week_list) == 1:
                            temp_matrix[int(week_list[0]) - 1, j] = 1
                        else:
                            temp_week = np.arange(int(week_list[0]), int(week_list[1]) + 1, 1, int)
                            temp_matrix[temp_week - 1, j] = 1                   
        except:
            pass
    major_dict[temp_major] = temp_matrix

with open('major_dict.pkl','wb')as f:
    pickle.dump(major_dict, f)      
   




