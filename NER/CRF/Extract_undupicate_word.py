def save_model(model_path, word_dict):
    f = open(model_path, 'w')
    f.write(str(word_dict))
    f.close()


def load_model(model_path):
    f = open(model_path,'r')
    a = f.read()
    word_dict = eval(a)
    f.close()
    return word_dict


def init(word_dict):
    word_trans = {}
    for word in word_dict:
        word_trans[word] = {}
    return word_trans


if __name__ == '__main__':
    word_dict = load_model('./model/set_list.txt')
    word_trans = init(word_dict)
    count_dict = {}

    for line in open('../data/train.txt', encoding='utf-8'):
        words_list = []
        if line:
            line = line.strip()
            wl = line.split(' ')
            for w in wl:
                word,tag = w.split('/')
                words_list.append(word)
                if word not in count_dict:
                    count_dict[word] = 1
                else:
                    count_dict[word] += 1

            for i in range(len(words_list) - 1):
                if words_list[i+1] not in word_trans[words_list[i]]:
                    word_trans[words_list[i]][words_list[i + 1]] = 1
                else:
                    word_trans[words_list[i]][words_list[i + 1]] += 1
    save_model('./model/word_trans.txt', word_trans)
    save_model('./model/count_dict.txt', word_trans)
    for key in word_trans.keys():
        for key1 in word_trans[key].keys():
            word_trans[key][key1] = word_trans[key][key1]/count_dict[key]


    save_model('./model/prob_word_trans.txt',word_trans)




