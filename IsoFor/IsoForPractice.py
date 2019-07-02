import numpy as np
import pandas as pd
import random
from sklearn.utils.fixes import euler_gamma
import time
import math
class Input_Data(object):
    def __init__(self,sub_sample_size):
        self.sub_sample_size = sub_sample_size

    def input(self):
        self.address = "C:/Users/dell/Desktop/spark_if_train.csv"
        self.Init_data = pd.read_csv(self.address)

        self.Sample = self.Init_data.values
        self.Sample = list(self.Sample)
        self.length = len(self.Sample)

        if(self.sub_sample_size>self.length):
            self.sub_sample_size = self.length

        self.ranges = list(range(self.length))
    #从数据集中抽取subsample_size个子数据
    def getSubSample(self):
        if self.sub_sample_size > len(self.ranges):
            self.sub_sample_size = len(self.ranges)
        self.random_data = random.sample(self.ranges,self.sub_sample_size)
        self.sub_sample = []
        for i in self.random_data:
            self.sub_sample.append(i)
        for i in self.random_data:
            self.ranges.remove(i)


class Select_Attribute(object):
    def __init__(self,sample):
        self.sample = sample
    def get_random_attr(self):
        self.random_attr = np.random.randint(len(self.sample[0]))

    def getRandomValue(self):
        random_row = np.random.randint(len(self.sample))
        random_value = self.sample[random_row][self.random_attr]
        return random_value

class ITree(object):
    def __init__(self, depth, subsample, Sample):
        self.depth = depth
        self.root = subsample
        self.sample = Sample
    def itree(self):
        attr = 0
        depth = 0

        self.Tree_1 = []
        self.tree = [[self.root, 0, attr]]

        while (depth < self.depth and self.tree):
            self.left = []
            self.right = []
            root,depth,attr = self.tree.pop(0)
            attr_setter = Select_Attribute(self.sample)
            attr_setter.get_random_attr()
            random_attr = attr_setter.random_attr
            random_value = attr_setter.getRandomValue()


            i = 0
            while(i<len(root)):
                if(len(root)==1 or depth == self.depth-1 ):
                    self.Tree_1.append([root,depth])
                    break
                if(self.sample[root[i]][random_attr]<random_value):
                    self.left.append(root[i])
                else:
                    self.right.append(root[i])
                i+=1
            depth+=1

            if(not(self.left == [])):
                self.tree.append([self.left,depth,random_attr])
            if(not(self.right == [])):
                self.tree.append([self.right,depth,random_attr])

    def prediction(self):
        self.cn = 2*(math.log(len(self.root)-1,math.e)+euler_gamma)-(2*(len(self.root)-1)/(len(self.root)))

        self.orgin = sorted(self.root)
        self.path = []
        #这里的主要目标是求出来根据50个抽样样本所得出来的异常数据的path
        i = 0
        while i < len(self.orgin):
            self.path.append(0)
            i += 1
        i = 0
        while i<len(self.orgin):
            j = 0
            while j<len(self.Tree_1):
                k=0
                while k<len(self.Tree_1[j][0]):
                    if(self.Tree_1[j][0][k] == self.orgin[i]):
                        self.path[i] = self.Tree_1[j][1]
                    k+=1
                j+=1
            i+=1

class IsoForest:
    #256 50 15
    def __init__(self,max_sample,sub_sample,depth):
        self.max_sample = max_sample
        self.sub_sample = sub_sample
        self.depth = depth

    def buildForest(self):
        ranges = [0]
        self.score_1 = []
        self.index = []

        #初始化
        input = Input_Data(self.sub_sample)
        input.input()

        while ranges:
            input.getSubSample()
            subsample = input.sub_sample
            ranges = input.ranges
            i=0
            j=0
            itree = ITree(self.depth, subsample, input.Sample)
            level_path = []
            score = []
            while j<input.sub_sample_size:
                level_path.append(0)
                score.append(0)
                j+=1
            while i<self.max_sample:
                itree.itree()
                itree.prediction()
                k=0
                while k<input.sub_sample_size:
                    level_path[k] = level_path[k] + itree.path[k]
                    k+=1
                i+=1

            m = 0
            while m<input.sub_sample_size:
                level_path[m] = level_path[m]/self.max_sample
                score[m] = 2**(-level_path[m]/itree.cn)
                m+=1

            for temp in score:
                self.score_1.append(temp)
            for temp in itree.orgin:
                self.index.append(temp)

        a = self.sort_1(self.score_1, self.index)
        n = 0
        sum = 0
        while n<len(a):
            # print(str(self.index[n]) + ":" + str(self.score_1[n]))
            if(a[n]>0.6):
                # print(self.index[n])
                sum +=1
            n+=1
        print(sum)
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
if __name__=='__main__':
    start = time.time()
    iforest = IsoForest(256,50,15)
    iforest.buildForest()
    end = time.time()
    print(end-start)