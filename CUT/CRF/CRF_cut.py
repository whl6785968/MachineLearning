class CRF_cut:
    def __init__(self):
        emit_path = './model/emit_dict.txt'
        trans_path = './model/trans_dict.txt'
        self.prob_trans = self.load_mode(trans_path)
        self.prob_emit = self.load_mode(emit_path)



    def load_mode(self,model_path):
        f = open(model_path,encoding='utf-8')
        a = f.read()
        word_dict = eval(a)
        f.close()
        return word_dict

    def verbiter(self,sent,states,prob_emit,prob_trans):
        V = [{}]
        path = {}

        for state in states:
            V[0][state] = self.prob_emit[state].get(sent[0],0)
            path[state] = state

        for t in range(1,len(sent)):
            V.append({})
            newpath = {}
            for state in states:
                state_path = [(V[t-1][y0] * self.prob_trans[y0].get(state,0) * self.prob_emit[state].get(sent[0],0),y0) for y0 in states if V[t-1][y0] > 0]