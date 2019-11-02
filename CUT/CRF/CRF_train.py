class CRF_train:
    def __init__(self):
        print(1)
        self.trans_dict = {}
        self.emit_dict = {}
        self.state_list = ['B','M','E','S']
        self.vocabulary_freq = {}
        self.count_dict = {}
        self.char_set = set()
        self.init()

    def init(self):
        for state in self.state_list:
            self.trans_dict[state] = {}
            for state1 in self.state_list:
                self.trans_dict[state][state1] = 0

        for state in self.state_list:
            self.emit_dict[state] = {}
            self.count_dict[state] = 0


    def get_word_state(self,word):
        word_status = []
        if len(word) == 1:
            word_status.append('S')
        elif len(word) == 2:
            word_status = ['B','E']
        else:
            m_num = len(word) - 2
            m_list = ['M'] * m_num
            word_status.append('B')
            word_status.extend(m_list)
            word_status.append('E')

        return word_status


    def train(self,train_path,trans_path,emit_path):
        for line in open(train_path,encoding='utf-8'):
            line = line.strip()
            if not line:
                continue

            word_states = []
            word_list = line.split(' ')

            char_list = []
            for i in range(len(line)):
                if line[i] == ' ':
                    continue
                char_list.append(line[i])

            self.char_set = set(char_list)

            for word in word_list:
                word_state = self.get_word_state(word)
                word_states.extend(word_state)

            if len(char_list) == len(word_states):
                for i in range(len(word_states)):
                    if i == 0:
                        continue
                    else:
                        self.trans_dict[word_states[i-1]][word_states[i]] += 1
                        if char_list[i] not in self.emit_dict[word_states[i]]:
                            self.emit_dict[word_states[i]][char_list[i]] = 1
                        else:
                            self.emit_dict[word_states[i]][char_list[i]] += 1

                        self.count_dict[word_states[i]] += 1
            else:
                continue

        for key in self.trans_dict:
            for key1 in self.trans_dict:
                self.trans_dict[key][key1] = self.trans_dict[key][key1]/self.count_dict[key]

        for key in self.emit_dict:
            for word in self.emit_dict[key]:
                self.emit_dict[key][word] = self.emit_dict[key][word]/self.count_dict[key]

        self.save_model(self.trans_dict,trans_path)
        self.save_model(self.emit_dict,emit_path)


    def save_model(self,word_dict,model_path):
        f = open(model_path,'w')
        f.write(str(word_dict))
        f.close()


if __name__ == '__main__':
    ct = CRF_train()
    train_path = './data/train.txt'
    trans_path = './model/trans_dict.txt'
    emit_path = './model/emit_dict.txt'
    ct.train(train_path,trans_path,emit_path)




