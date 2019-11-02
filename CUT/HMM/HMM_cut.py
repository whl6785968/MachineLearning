class HMM_cut:
    def __init__(self):
        trans_path = './model/prob_trans.txt'
        emit_path = './model/prob_emit.txt'
        start_path = './model/prob_start.txt'
        self.prob_trans = self.load_model(trans_path)
        self.prob_emit = self.load_model(emit_path)
        self.prob_start = self.load_model(start_path)


    def load_model(self,model_path):
        f = open(model_path,'r')
        a = f.read()
        word_dict = eval(a)
        f.close()
        return word_dict

    def viterbi(self,obs,states,start_p,trans_p,emit_p):
        V = [{}]
        path = {}
        #1.初始化 a(i) = 初始概率*发射概率
        for y in states:
            V[0][y] = start_p[y] * emit_p[y].get(obs[0],0)
            path[y] = [y]
        #2.循环
        for t in range(1,len(obs)):
            V.append({})
            newpath = {}
            for y in states:
                #当前是某个状态下，找出最有可能的转移至该状态的状态
                state_path = ([(V[t - 1][y0] * trans_p[y0].get(y, 0) * emit_p[y].get(obs[t], 0), y0) for y0 in states if V[t - 1][y0] > 0])
                if state_path == []:
                    (prob,state) = (0.0,'S')
                else:
                    (prob,state) = max(state_path)

                V[t][y] = prob
                newpath[y] = path[state] + [y]
            path = newpath

        (prob,state) = max([(V[len(obs) - 1][y], y) for y in states])

        return (prob,path[state])

    def cut(self,sent):
        prob,pos_list = self.viterbi(sent,['B','M','E','S'],self.prob_start,self.prob_trans,self.prob_emit)

        seglist = list()
        word = list()

        for index in range(len(pos_list)):
            if pos_list[index] == 'S':
                word.append(sent[index])
                seglist.append(word)
                word = []
            elif pos_list[index] in ['B','M']:
                word.append(sent[index])
            elif pos_list[index] == 'E':
                word.append(sent[index])
                seglist.append(word)
                word = []

        seglist = [''.join(tmp) for tmp in seglist]

        return seglist

if __name__ == '__main__':
    hc = HMM_cut()
    # sent = '我们在野生动物园玩'
    # sent = '我不想上班，我想放假'
    # sent = '何时才能找到女朋友'
    # sent = '是你的丈夫吗'
    # sent = '王海龙的梦想是上清华大学'
    sent = '清华大学副校长尤政宣布成立清华大学人工智能研究院,张钹院士担任新研究院的院长。清华大学成立人工智能研究院再次反映出了国内高校设立人工智能学科的热潮。2017年7月,国务院颁布《新一代人工智能发展规划》明确提出,大力建设人工智能学'
    seglist = hc.cut(sent)
    print(seglist)