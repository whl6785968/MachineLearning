def save_model(word_dict,model_path):
    f = open(model_path,'w')
    f.write(str(word_dict))
    f.close()

if __name__ == '__main__':
    start_dict = {}
    line_index = 0
    for line in open('../data/train.txt', encoding='utf-8'):
        if line:
            line = line.strip()
            word_list = line.split(' ')
            init_word,init_tag = word_list[0].split('/')
            if init_word not in start_dict:
                start_dict[init_word] = 1
            else:
                start_dict[init_word] += 1

            line_index += 1

    for key in start_dict:
        start_dict[key] = start_dict[key] / line_index

    save_model(start_dict,'./model/start_word.txt')

