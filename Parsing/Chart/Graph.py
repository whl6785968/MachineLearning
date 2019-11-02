#chart 用nxn数组表示
#agenda 用栈或者线性队列表示
#活动边集 用列表或者数组
class Graph4Chart:
    def __init__(self,V):
        self.V = V
        self.E = 0
        self.adj_dict = {}
        self.init()
        self.rule = {'S':['VP','NP'],'NP':['Det','N'],'VP':['VP','PP'],'VP':['V','NP'],'PP':['Prep','NP']}
        self.old_E = 0

    def init(self):
        for v in self.V:
            self.adj_dict[v] = {}

    def add_edge(self,v,w,e):
        self.adj_dict[v][w] = e
        self.E += 1
        self.old_E += 1

    def adj(self,v):
        return self.adj_dict[v]

    def add_rule(self):
        pass

    def add_activeArc(self):
        pass

if __name__ == '__main__':
    v = ['begin','the','boy','hits','the','dog','with','a','rod']
    index = [i for i in range(len(v))]
    e_tag = ['Det','N','V','Det','N','Prep','Det','N']
    gc = Graph4Chart(index)
    # gc.add_edge(v[0],v[1],e_tag[0])
    for i in range(len(v)-1):
        gc.add_edge(index[i],index[i+1],e_tag[i])

    print(gc.adj_dict)
    print(gc.E)
    print(gc.rule)

    for i in range(len(gc.adj_dict)):
        print(gc.adj_dict[i])




