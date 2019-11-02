from Parsing.Chart.LinearQueue import Queue


class parsing_chart:
    def __init__(self,voca_tag):
        queue = Queue()
        self.agenda = queue
        self.voca_tag = voca_tag
        self.ActiveArc = []
        self.chart = []
        self.rules = [['S','NP','VP',0,0],['NP','Det','N',0,0],['VP','VP','PP',0,0],['VP','V','NP',0,0],['PP','Prep','NP',0,0]]
        self.changed_rules = self.rules.copy()
        self.rowFirst = None
        self.columnFirst = None

    def parsing(self,sentence):
        print('=======开始分析句子结构=======')
        # self.agenda = LinearQueue()
        s_length = len(sentence)
        count = -1
        for i in range(s_length+1):
            self.chart.append([0]*(s_length+1))
        while(count < len(sentence)):
            if self.agenda.isEmpty():
                # word_pos = self.voca_tag[i] + '('+str(i)+','+str(i+1)+')'
                count += 1
                if count == len(sentence):
                    break
                word_pos = [self.voca_tag[count],count, count + 1]
                self.agenda.enqueue(word_pos)
            else:
                word_pos = self.agenda.unqueue().item
                for i in range(len(self.rules)):
                    rule = self.changed_rules[i]
                    if word_pos[0] == rule[1]:
                        self.add_ActiveArc(rule,word_pos)

                self.extend_arc(word_pos,s_length,count)

        # self.get_text_struc(sentence)


    def add_ActiveArc(self,rule,word_pos):
        word = word_pos[0]
        if '。' in rule:
            rule.remove('。')

        # 有些规则如VP -> VP PP 需要将。移动到后面的VP处
        index = [i for i,x in enumerate(rule) if x == word]
        if len(index) > 1:
            real_index = index[len(index)-1]
        else:
            real_index = index[0]
        rule.insert(real_index+1,'。')
        rule[4] = word_pos[1]
        rule[5] = word_pos[2]
        self.ActiveArc.append(rule)

    def extend_arc(self,word_pos,s_length,count):
        self.chart[word_pos[1]][word_pos[2]] = word_pos[0]
        for i in range(len(self.ActiveArc)):
            if word_pos[0] == self.ActiveArc[i][3]:
                if 'S' == self.ActiveArc[i][0]:
                    self.chart[0][s_length] = 'S'
                else:
                    self.ActiveArc[i] =[self.ActiveArc[i][0],self.ActiveArc[i][1],self.ActiveArc[i][3],self.ActiveArc[i][2],self.ActiveArc[i][4],self.ActiveArc[i][5]]
                    self.agenda.enqueue([self.ActiveArc[i][0],self.ActiveArc[i][4],word_pos[2]])

    def get_text_struc(self,sentence):
        print('=======句子结构如下=======')
        # print(self.chart)
        for i in range(len(self.chart)-1):
            for j in range(len(self.chart)):
                if self.chart[i][j] != 0:
                    print(str(sentence[i:j])+ ':' + self.chart[i][j])

    def get_structure_tree(self,sentence,row,column):
        col_value = None
        row_value = None
        n_row1 = None
        n_col1 = None
        n_row2 = None
        n_col2 =None
        if row is None or column is None:
            return

        curr_tag = self.chart[row][column]

        for i in range(column-1,-1,-1):
            if self.chart[row][i] != 0:
                row_value = self.chart[row][i]
                # print(row_value)
                n_row1 = row
                n_col1 = i
                break

        for r in range(row+1,len(self.chart) - 1):
            if self.chart[r][column] != 0:
                col_value = self.chart[r][column]
                # print(col_value)
                n_row2 = r
                n_col2 = column
                break

        if col_value is not None and row_value is not None:
            print(' '.join(sentence[row:column])+'/'+curr_tag + '  ->  ' + ' '.join(sentence[n_row1:n_col1]) + '/' + row_value + '   ' + ' '.join(sentence[n_row2:n_col2]) + '/' + col_value)

        self.get_structure_tree(sentence,n_row1,n_col1)
        self.get_structure_tree(sentence,n_row2,n_col2)




if __name__ == '__main__':
    sentence = ['the', 'boy', 'hits', 'the', 'dog', 'with', 'a', 'rod']
    voca_tag = ['Det','N','V','Det','N','Prep','Det','N']
    pc = parsing_chart(voca_tag)
    pc.parsing(sentence)
    nrow = 0
    ncol = len(pc.chart)-1
    print('======chart======')
    for i in range(len(pc.chart)-1):
        print(pc.chart[i])
    print('======句子结构======')
    pc.get_structure_tree(sentence,nrow,ncol)

