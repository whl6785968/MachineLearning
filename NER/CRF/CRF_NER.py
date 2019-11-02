

class CRF_ner:
    def __init__(self):
        trans_path = './model/trans_dict.txt'
        emit_path = './model/emit_dict.txt'
        word_trans_path = './model/prob_word_trans.txt'
        start_word_path = './model/start_word.txt'

        self.prob_trans = self.load_model(trans_path)
        self.prob_emit = self.load_model(emit_path)
        self.prob_word_trans = self.load_model(word_trans_path)
        self.prob_start_word = self.load_model(start_word_path)

    def load_model(self,model_path):
        f = open(model_path,'r')
        a = f.read()
        word_dict = eval(a)
        f.close()
        return word_dict

    def verbiter(self,sent,state_list):
        V = [{}]
        path = {}
        #state_list = ['O', 'B-LOCATION', 'I-LOCATION', 'O-LOCATION', 'B-ORGANIZATION', 'I-ORGANIZATION',
        #'O-ORGANIZATION', 'B-PERSON', 'B-TIME']
        #初始化
        for state in state_list:
            if self.prob_word_trans.get(sent[0],0) == 0:
                V[0][state] = self.prob_start_word.get(sent[0],0) + self.prob_emit[state].get(sent[0],0)
            else:
                V[0][state] = self.prob_start_word.get(sent[0], 0) + self.prob_emit[state].get(sent[0], 0) + self.prob_word_trans[sent[0]].get(sent[1], 0)
            path[state] = [state]
        for i in range(1,len(sent)):
            V.append({})
            newpath = {}
            state_path = []
            for state in state_list:
                if i == len(sent) - 1:
                    if self.prob_word_trans.get(sent[i-1], 0) == 0:
                        W = self.prob_emit[state].get(sent[i], 0)
                    else:
                        W = self.prob_word_trans[sent[i - 1]].get(sent[i], 0) + self.prob_emit[state].get(sent[i], 0)
                else:
                    W = (self.prob_word_trans[sent[i - 1]].get(sent[i], 0) if self.prob_word_trans.get(sent[i-1],0) != 0 else 0) + self.prob_emit[state].get(sent[i],0) + (self.prob_word_trans[sent[i]].get(sent[i + 1], 0) if self.prob_word_trans.get(sent[i],0) != 0 else 0)
                for state1 in state_list:
                    R = V[i-1][state1] * self.prob_trans[state1].get(state,0)
                    state_path.append((R,state1))
                if state_path == []:
                    (prob,y) = (0.0,'O')
                else:
                    (prob,y) = max(state_path)
                V[i][state] = prob * W
                newpath[state] = path[y] + [state]
            path = newpath
        (prob, state) = max([(V[len(sent) - 1][y], y) for y in state_list])
        return (prob,path[state])

    def cut(self,sent):
        print('========开始计算========')
        state_list = ['O', 'B-LOCATION', 'I-LOCATION', 'O-LOCATION', 'B-ORGANIZATION', 'I-ORGANIZATION','O-ORGANIZATION', 'B-PERSON', 'B-TIME']
        prob,pos_list = self.verbiter(sent,state_list)
        result = []
        sub_result = []
        for i in range(len(pos_list)-1):
            if pos_list[i] in ['B-ORGANIZATION','I-ORGANIZATION','O-ORGANIZATION'] and pos_list[i+1] in ['B-ORGANIZATION','I-ORGANIZATION','O-ORGANIZATION']:
                sub_result.append(sent[i])
            elif pos_list[i] in ['B-ORGANIZATION','I-ORGANIZATION','O-ORGANIZATION'] and pos_list[i+1] not in ['B-ORGANIZATION','I-ORGANIZATION','O-ORGANIZATION']:
                result.append(sub_result)
                sub_result = []

        last = len(pos_list) - 1
        print(pos_list)
        if pos_list[last-1] in ['B-ORGANIZATION','I-ORGANIZATION','O-ORGANIZATION'] and pos_list[last] in ['B-ORGANIZATION','I-ORGANIZATION','O-ORGANIZATION']:
            sub_result.append(sent[last])
            result.append(sub_result)
        elif pos_list[last-1] not in ['B-ORGANIZATION','I-ORGANIZATION','O-ORGANIZATION'] and pos_list[last] in ['B-ORGANIZATION','I-ORGANIZATION','O-ORGANIZATION']:
            sub_result.append(sent[last])
            result.append(sub_result)

        entities = []
        for entity_list in result:
            entity = ''
            for tmp in entity_list:
                entity += tmp
            entities.append(entity)
        return entities

if __name__ == '__main__':
    sent = ['陈','鼎立','毕业','于','西南','科技','大学']
    # sent = ['中国','政府','要求','美方','遵守','条约']
    # sent = ['清华大学', '在', '北京市', '海', '淀', '区', '清', '华', '园', '1', '号']
    # sent = ['清华大学','副','校长','尤政','宣布','成立','人工','智能','研究院','张钹','院士','担任','新','研究院','院长']
    ce = CRF_ner()
    result = ce.cut(sent)
    print(result)