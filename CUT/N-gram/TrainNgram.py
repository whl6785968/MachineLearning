class TrainNgram:
    def __init__(self):
        self.word_dict = {}
        self.trans_dict = {}

    def save_mode(self,word_dict,model_path):
        f = open(model_path,'w')
        f.write(str(word_dict))
        f.close()

    def train(self,train_data_path,word_dict_path,trans_dict_path):
        self.trans_dict[u'<BEG>'] = {}
        self.word_dict['<BEG>'] = 0

        for sentence in open(train_data_path,encoding='utf8'):
            self.word_dict['<BEG>'] += 1
            sentence = sentence.strip()
            sentence = sentence.split(' ')
            sentence_list = []
            for pos,words in enumerate(sentence):
                if words != '':
                    sentence_list.append(words)

            for pos,words in enumerate(sentence_list):
                if words not in self.word_dict.keys():
                    self.word_dict[words] = 1
                else:
                    self.word_dict[words] += 1

                if pos == 0:
                    word1,word2 = 'u<BEG>',words
                elif pos == len(sentence_list) - 1:
                    word1,word2 = words,u'END'
                else:
                    word1,word2 = words,sentence_list[pos+1]

                if words not in self.trans_dict.keys():
                    self.trans_dict[word1] = {}
                if word2 not in self.trans_dict[word1]:
                    self.trans_dict[word1][word2] = 1
                else:
                    self.trans_dict[word1][word2] += 1

        self.save_mode(self.word_dict,word_dict_path)
        self.save_mode(self.trans_dict,trans_dict_path)

if __name__ == '__main__':
    train_data_path = './data/train.txt'
    word_dict_path = './model/word_dict.txt'
    trans_dict_path = './model/trans_dict.txt'
    tn = TrainNgram()
    tn.train(train_data_path,word_dict_path,trans_dict_path)