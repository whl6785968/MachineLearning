import math


class MaxNgram:
    def __init__(self):
        self.word_dict = {}
        self.word_count_dict = {}
        self.trans_dict = {}
        self.trans_count_dict = {}
        self.max_word_len = 0
        self.all_freq = 0
        word_dict_path = './model/word_dict.txt'
        trans_dict_path = './model/trans_dict.txt'
        self.init(word_dict_path,trans_dict_path)

    def init(self,word_dict_path,trans_dict_path):
        self.word_count_dict = self.load(word_dict_path)
        self.all_freq = sum(self.word_count_dict.values())
        self.max_word_len = max(len(word) for word in self.word_count_dict.keys())
        for key in self.word_count_dict:
            self.word_dict[key] = math.log(self.word_count_dict[key]/self.all_freq)

        Trans_dict = self.load(trans_dict_path)

        for pre_word,post_info in Trans_dict.items():
            for post_word,count in post_info.items():
                word_pair = pre_word + ' ' + post_word
                self.trans_count_dict[word_pair] = float(count)
                #P(post_word|pre_word) = p(post_word * pre_word)/p(pre_word) = count(post_word,pre_word)/count(pre_word)
                if pre_word in self.word_count_dict.keys():
                    self.trans_dict[key] = math.log(count/self.word_count_dict[pre_word])
                else:
                    self.trans_dict[key] = self.word_dict[post_word]

    def unknown_word(self,word):
        return math.log(1/(self.all_freq ** len(word)))

    def get_word_prob(self,word):
        if word in self.word_dict.keys():
            prob = self.word_dict[word]
        else:
            prob = self.unknown_word(word)

        return prob

    def get_trans_prob(self,pre_word,post_word):
        word_pair = pre_word + ' ' + post_word

        if word_pair in self.trans_count_dict.keys():
            trans_prob = math.log(self.trans_count_dict[word_pair] / self.word_count_dict[pre_word])
        else:
            trans_prob = self.get_word_prob(post_word)
        return trans_prob

    def get_best_pre_node(self,sentence,node,node_state_list):
        max_seg_length = min([node,self.max_word_len])
        pre_node_list = []

        for segment_length in range(1,max_seg_length+1):
            segment_start_node = node - segment_length
            segment = sentence[segment_start_node:node]
            pre_node = segment_start_node

            if pre_node == 0:
                segment_prob = self.get_trans_prob('<BEG>',segment)
            else:
                pre_pre_node = node_state_list[pre_node]['pre_node']
                pre_pre_word = sentence[pre_pre_node:pre_node]
                segment_prob = self.get_trans_prob(pre_pre_word,segment)

            pre_node_prob_sum = node_state_list[pre_node]['prob_sum']
            candidate_prob_sum = pre_node_prob_sum + segment_prob
            pre_node_list.append((pre_node,candidate_prob_sum))

        (best_pre_node,best_prob_sum) = max(pre_node_list,key=lambda d: d[1])
        return best_pre_node,best_prob_sum

    def cut(self,sentence):
        sentence = sentence.strip()
        # 初始化
        node_state_list = []  # 记录节点的最佳前驱，index就是位置信息
        # 初始节点，也就是0节点信息
        ini_state = {}
        ini_state["pre_node"] = -1  # 前一个节点
        ini_state["prob_sum"] = 0  # 当前的概率总和
        node_state_list.append(ini_state)
        # 字符串概率为2元概率， P(a b c) = P(a|<S>)P(b|a)P(c|b)
        # 逐个节点寻找最佳前驱节点
        for node in range(1, len(sentence) + 1):
            # 寻找最佳前驱，并记录当前最大的概率累加值
            (best_pre_node, best_prob_sum) = self.get_best_pre_node(sentence, node, node_state_list)

            # 添加到队列
            cur_node = {}
            cur_node["pre_node"] = best_pre_node
            cur_node["prob_sum"] = best_prob_sum
            node_state_list.append(cur_node)
            # print "cur node list",node_state_list

        # step 2, 获得最优路径,从后到前
        best_path = []
        node = len(sentence)  # 最后一个点
        best_path.append(node)
        while True:
            pre_node = node_state_list[node]["pre_node"]
            if pre_node == -1:
                break
            node = pre_node
            best_path.append(node)
        best_path.reverse()

        # step 3, 构建切分
        word_list = []
        for i in range(len(best_path) - 1):
            left = best_path[i]
            right = best_path[i + 1]
            word = sentence[left:right]
            word_list.append(word)

        return word_list


    def load(self,model_path):
        f = open(model_path,'r')
        a = f.read()
        word_dict = eval(a)
        f.close()
        return word_dict


if __name__ == '__main__':
    mn = MaxNgram()
    # sent = '何时才能找到女朋友？？？'
    # sent = '长短期记忆网络（LSTM，Long Short-Term Memory）是一种时间循环神经网络，是为了解决一般的RNN（循环神经网络）存在的长期依赖问题而专门设计出来的，所有的RNN都具有一种重复神经网络模块的链式形式。在标准RNN中，这个重复的结构模块只有一个非常简单的结构，例如一个tanh层。'
    # sent = '长短期记忆网络（Long-Short Term Memory,LSTM）论文首次发表于1997年。由于独特的设计结构，LSTM适合于处理和预测时间序列中间隔和延迟非常长的重要事件。'
    # sent = '王海龙的梦想是上清华大学'
    sent = '清华大学在北京市海淀区清华园1号'
    seglist = mn.cut(sent)
    print(seglist)