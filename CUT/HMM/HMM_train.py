class HMM_train:
    def __init__(self):
        self.line_index = -1
        self.char_set = set()

    def init(self):
        trans_dict = {}
        emit_dict = {}
        count_dict = {}
        start_dict = {}
        state_list = ['B','M','E','S']

        for state in state_list:
            trans_dict[state] = {}
            for state1 in state_list:
                trans_dict[state][state1] = 0.0

        for state in state_list:
            start_dict[state] = 0.0
            emit_dict[state] = {}
            count_dict[state] = 0

        return trans_dict,emit_dict,start_dict,count_dict

    def save_model(self,word_dict,model_path):
        f = open(model_path,'w')
        f.write(str(word_dict))
        f.close()

    def get_word_status(self,word):
        word_status = []

        if len(word) == 1:
            word_status.append('S')
        elif len(word) == 2:
            word_status = ['B','E']
        else:
            M_num = len(word) - 2
            M_list = ['M'] * M_num
            word_status.append('B')
            word_status.extend(M_list)
            word_status.append('E')

        return word_status

    def train(self,trainfile_path,trans_path,emit_path,start_path):
        print('======Start Train Model======')
        trans_dict,emit_dict,start_dict,count_dict = self.init()
        for line in open(trainfile_path,encoding='utf-8'):
            print(count_dict)
            self.line_index += 1
            line = line.strip()
            if not line:
                continue
            char_list = []
            for i in range(len(line)):
                if line[i] == " ":
                    continue
                char_list.append(line[i])

            self.char_set = set(char_list)
            word_list = line.split()
            line_status = []
            #过去 的 一 年 ，
            #char_list['过去','的','一','年','，']
            #word_list['过去','的','一','年','，']
            #list_status['B','E','S','S','S','S']
            for word in word_list:
                line_status.extend(self.get_word_status(word))

            if len(line_status) == len(char_list):
                for i in range(len(line_status)):
                    #根据每个句子的第一个字得出初始的BMES概率
                    if i == 0:
                        start_dict[line_status[0]] += 1
                        count_dict[line_status[0]] += 1
                    else:
                        trans_dict[line_status[i-1]][line_status[i]] += 1
                        count_dict[line_status[i]] += 1

                        if char_list[i] not in emit_dict[line_status[i]]:
                            emit_dict[line_status[i]][char_list[i]] = 1.0
                        else:
                            emit_dict[line_status[i]][char_list[i]] += 1
            else:
                continue
        for key in start_dict:
            start_dict[key] =start_dict[key] * 1.0/self.line_index

        for key in trans_dict:
            for key1 in trans_dict:
                trans_dict[key][key1] = trans_dict[key][key1]/count_dict[key]

        for key in emit_dict:
            for word in emit_dict[key]:
                emit_dict[key][word] = emit_dict[key][word]/count_dict[key]

        self.save_model(trans_dict,trans_path)
        self.save_model(emit_dict,emit_path)
        self.save_model(start_dict,start_path)

        return trans_dict,emit_dict,start_dict

if __name__ == '__main__':
    ht = HMM_train()
    # trans_dict,emit_dict,start_dict,count_dict = ht.init()
    # print(trans_dict)
    # print(emit_dict)
    # print(start_dict)
    # print(count_dict)

    # word_status = ht.get_word_status('我不想上班')
    # print(word_status)

    trainfile_path = 'C:/Users/dell/Desktop/WordSegment-master/data/train.txt'
    trans_path = './model/prob_trans.txt'
    emit_path = './model/prob_emit.txt'
    start_path = './model/prob_start.txt'
    ht.train(trainfile_path,trans_path,emit_path,start_path)
