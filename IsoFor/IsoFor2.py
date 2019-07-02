# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 09:04:19 2019

@author: dell
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import random
import math
import time

class Input_Datas(object):
    """
    该方法用于导入数据，与选取子样本
    """
    def __init__(self, subsample_size):
        # 子样本大小
        self.subsample_size = subsample_size

    def  Input(self):
        """导入数据，并将数据转换成list格式"""
        self.Address = "C:/Users/dell/Desktop/spark_if_train.csv"
        self.Initial_Datas = pd.read_csv(self.Address)
        # self.Sample（总样本）
        self.Sample = self.Initial_Datas.values
       # self.Sample = np.delete(self.Sample, 0, axis=1)
        self.Sample = list(self.Sample)
        #557
        self.length = len(self.Sample)
        if self.subsample_size >= self.length:
            self.subsample_size = self.length
        #list(0...557)
        self.ranges = list(range(self.length))

    def Subsample(self):
        """从Input处理后的数据中，选取子样本"""
        if self.subsample_size >= len(self.ranges):
            self.subsample_size = len(self.ranges)
        #生成随机数据 random.sample(557,50)
        self.random_datas = random.sample(self.ranges, self.subsample_size)
        self.subsample = []
        #
        for temp in self.random_datas:
            self.subsample.append(temp)
        for temp in self.random_datas:
            #507
            self.ranges.remove(temp)


class Select_Attribute(object):
    """
    挑选数据属性，并随机挑选一个该属性中的最大值与最小值
    """
    def __init__(self, sample):
        self.Sample = sample

    def random_attribute(self):
        """随机挑选一个属性"""
        length = len(self.Sample[0])
        ranges = list(range(length))
        self.random_attribute_datas = random.sample(ranges, 1)

    def random_values(self, Sample):
        """在所挑选属性中随机挑选一个值"""
        i = 0
        max = self.Sample[Sample[0]][self.random_attribute_datas[0]]
        min = max
        while i < len(Sample):
            if self.Sample[Sample[i]][self.random_attribute_datas[0]] > max:
               max = self.Sample[Sample[i]][self.random_attribute_datas[0]]

            if self.Sample[Sample[i]][self.random_attribute_datas[0]] < min:
                min = self.Sample[Sample[i]][self.random_attribute_datas[0]]
            i += 1

        self.attribute_value = max - random.random() * (max - min)


class ITree(object):
    """
    建立孤立树
    """

    def __init__(self, depth, subsample, Sample):
        self.root = subsample
        self.depth = depth
        self.Sample = Sample

    def itree(self):
        """建立孤立树"""
        attribute = 0
        depth = 0
        self.Tree_1 = []
        self.Tree = [[self.root, 0, attribute]]
        while self.Tree and (depth <= self.depth):
            self.lift = []
            self.right = []
            root, depth, attribute = self.Tree.pop(0)
            #初始化
            set_attribute = Select_Attribute(self.Sample)
            #随机挑选一个属性
            set_attribute.random_attribute()
            #获取属性值
            attribute = set_attribute.random_attribute_datas[0]
            #选择split value
            set_attribute.random_values(root)
            attribute_value = set_attribute.attribute_value
            # i = 0
            # while i < len(self.Sample[0]):
            #     j = 0
            #     while j < len(self.root):
            #         if self.Sample[self.root[0]][i] == self.Sample[self.root[j]][i]:
            #             self.judge = True
            #         else:
            #             self.judge = False
            #             break
            #         j += 1
            #     if self.judge == False:
            #         break
            #     i += 1

            i = 0
            while i < len(root):
                if (len(root) == 1)or(depth == self.depth - 1):
                    self.Tree_1.append([root, depth+1])
                    break

                if self.Sample[root[i]][attribute] < attribute_value:
                    self.lift.append(root[i])
                else:
                    self.right.append(root[i])
                i += 1
            depth += 1
            if not(self.lift == []):
                self.Tree.append([self.lift, depth, attribute])
            if not(self.right == []):
                self.Tree.append([self.right, depth, attribute])


    def prediction(self):
        """计算每一个数据的路径长度"""
        self.cn = 2*(math.log(len(self.root) - 1, math.e) + 0.5772156649) - (2*(len(self.root) - 1)/(len(self.root)))

        # 对子样本从小到大进行排序
        self.original = sorted(self.root)
        self.path = []
        i = 0
        while i < len(self.original):
            self.path.append(0)
            i += 1
        i = 0
        while i < len(self.original):
            j = 0
            while j < len(self.Tree_1):
                k = 0
                while k < len(self.Tree_1[j][0]):
                    if self.Tree_1[j][0][k] == self.original[i]:
                        self.path[i] = self.Tree_1[j][1]
                    k += 1
                j += 1
            i += 1


class IForest(object):
    
    """
    建立多棵树，并求出每一个数据的异常分数
    
    """
    def __init__(self, Number, subsmaple_size, max_depth):
        self.number = Number
        self.subsample_size = subsmaple_size
        #树最大高度
        self.max_depth = max_depth

            #孤立树数量
            
    def Build_Forest(self):
        """建立孤立森林"""
        ranges =[0]
        self.scores_1 = []
        self.index = []
        example_a = Input_Datas(self.subsample_size)
        example_a.Input()
        while ranges:
            example_a.Subsample()
            ranges = example_a.ranges
            example_b = ITree(self.max_depth, example_a.subsample, example_a.Sample)
            # 平均路径长度
            level_path = []
            # 异常分数
            score = []
            i = 0
            j = 0
            while j < example_a.subsample_size:
                level_path.append(0)
                score.append(0)
                j += 1

            while i < self.number:
                example_b.itree()
                example_b.prediction()
                k = 0
                while k < example_a.subsample_size:
                    level_path[k] = level_path[k] + example_b.path[k]
                    k += 1
                i += 1
            k = 0
            while k < example_a.subsample_size:
                level_path[k] = level_path[k]/self.number
                score[k] = 2**(-level_path[k]/example_b.cn)
                k += 1

            for temp in score:
                self.scores_1.append(temp)
            for temp in example_b.original:
                self.index.append(temp)

        a = self.sort_1(self.scores_1, self.index)
        # print(a)
        i = 0
        sum = 0
        while i < len(a):
            if a[i] > 0.60:
                sum += 1
            i += 1
        print(sum)

        # print(sum/len(a))


    def sort_1(self, scores_1, index):
        """排序"""
        i = 0
        score = []
        while i < len(index):
            score.append(0)
            i += 1

        i = 0
        while i < len(index):
            result = index[i]
            score[result] = scores_1[i]
            i += 1
        return score

if __name__ == '__main__':

    start = time.time()
    forest = IForest(256, 50, 15)
    forest.Build_Forest()
    end = time.time()
    print(end-start)