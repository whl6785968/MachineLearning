class CRF_train:
    def __init__(self):
        self.state_list = ['O','B-LOCATION','I-LOCATION','O-LOCATION','B-ORGANIZATION','I-ORGANIZATION','O-ORGANIZATION','B-PERSON','B-TIME']
        self.trans_dict = {}
        self.emit_dict = {}
        self.count_dict = {}
        self.word_trans = {}
        self.word_count = {}
        self.words_list = []

    def init(self):
        for state in self.state_list:
            self.emit_dict[state] = {}
            self.count_dict[state] = 0

        for state in self.state_list:
            self.trans_dict[state] = {}
            for state1 in self.state_list:
                self.trans_dict[state][state1] = 0

    def train(self):
        self.init()
        for line in open('../data/train.txt',encoding='utf-8'):
            if line:
                line = line.strip()
                word_list = line.split(' ')
                char_list = []

                for word in word_list:
                    word1,tag = word.split('/')
                    char_list.append((word1,tag))

                for i in range(len(char_list) - 1):
                    self.trans_dict[char_list[i][1]][char_list[i+1][1]] += 1
                    self.count_dict[char_list[i][1]] += 1

                for i in range(len(char_list)):
                    state = char_list[i][1]
                    word = char_list[i][0]
                    if word not in self.emit_dict[state]:
                        self.emit_dict[state][word] = 1
                    else:
                        self.emit_dict[state][word] += 1

                for i in range(len(char_list)):
                    word = char_list[i][0]
                    if word not in self.word_count:
                        self.word_count[word] = 1
                    else:
                        self.word_count[word] += 1
            else:
                continue

        for state in self.state_list:
            for state1 in self.state_list:
                self.trans_dict[state][state1] = self.trans_dict[state][state1] / self.count_dict[state]

        for state in self.state_list:
            for word in self.emit_dict[state]:
                self.emit_dict[state][word] = self.emit_dict[state][word] / self.count_dict[state]

        self.save_model(self.emit_dict, './model/emit_dict.txt')
        self.save_model(self.trans_dict, './model/trans_dict.txt')

    def save_model(self,word_dict,model_path):
        f = open(model_path,'w')
        f.write(str(word_dict))
        f.close()

if __name__ == '__main__':
    ct = CRF_train()
    ct.train()
