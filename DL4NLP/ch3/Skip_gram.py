from matplotlib import pylab
import tensorflow as tf
import collections
import math
import numpy as np
import os
import random
import bz2
from six.moves import range
from six.moves.urllib.request import urlretrieve
from sklearn.cluster import KMeans
import operator
import csv
import os
from sklearn.manifold import TSNE
from math import ceil
import spectral


# https://www.evanjones.ca/software/wikipedia2text.tar.bz2
class Skip_gram:
    def __init__(self):
        self.url = 'http://www.evanjones.ca/software/'
        self.word_list = []
        self.voca_size = 20000
        self.data_index = 0
        self.batch_size = 128
        self.embedding_size = 128
        self.window_size = 4
        self.valid_size = 10
        self.valid_window = 50
        #从0-50中随机采样10个数据
        self.valid_examples = np.array(random.sample(range(self.valid_window),self.valid_size))
        #再从1000-1050中采样10个数据
        #结果如[  46   17   16   19   34   41    2    4   43   28 1016 1035 1002 1005 1024 1034 1037 1041 1032 1028]
        self.valid_examples = np.append(self.valid_examples,random.sample(range(1000,1000+self.valid_window),self.valid_size),axis=0)


    def maybe_download(self,filename,expected_bytes):
        if not os.path.exists(filename):
            print('Downloading file')
            filename,_ = urlretrieve(self.url + filename,filename)
        statInfo = os.stat(filename)
        if statInfo.st_size == expected_bytes:
            print('Found and verified %s' % filename)
        else:
            print(statInfo.st_size)
            raise Exception(
                'Failed to verify ' + filename + '. Can you get to it with a browser?')
        return filename

    def read_data(self,filename):
        for line in open(filename,encoding='utf8'):
            if line:
                sub_word_list = line.split(' ')
                for word in sub_word_list:
                    if word not in ['\n','，','“','”','、','。',',','的','了','在','和','有','是']:
                        self.word_list.append(word)


    #dictionary:{voca1:0,voca2:1,voca3:2}
    #reverse_dictionary:{0:voca1,1:voca2,2:voca3}
    #count：{voca1:2,voca2:3,voca3:5}
    #data:Contains the string of text we read.where string words are replaced with word IDs
    def build_dataset(self,words):
        count = [['UNK',-1]]
        count.extend(collections.Counter(words).most_common(self.voca_size-1))
        word_dictionary = dict()
        for word,_ in count:
            word_dictionary[word] = len(word_dictionary)


        data = list()
        unk_count = 0
        #常用单词用自己的索引
        #不常用单词用UNK索引(0)
        for word in words:
            if word in word_dictionary:
                index = word_dictionary[word]
            else:
                index = 0
                unk_count = unk_count + 1

            data.append(index)

        count[0][1] = unk_count
        reverse_dictionary = dict(zip(word_dictionary.values(),word_dictionary.keys()))
        assert len(word_dictionary) == self.voca_size

        return data,word_dictionary,reverse_dictionary,count

    def generat_batch_skip_gram(self,batch_size,window_size):
        #存储target word
        batch = np.ndarray(shape=(batch_size),dtype=np.int32)

        #用于存储上下文 word
        label = np.ndarray(shape=(batch_size,1),dtype=np.int32)

        #上下文单词数量+target word
        span = 2*window_size+1

        #用于存储在span中的所有word的索引，包括target
        buffer = collections.deque(maxlen=span)

        for _ in range(span):
            buffer.append(data[self.data_index])
            self.data_index = (self.data_index+1)%len(data)

        #为单个target word所需采样的上下文word数量
        num_sample = 2 * window_size

        #把batch的读取分为两个循环
        #内循环负责用span中num_sample数量的data填充labels和batch
        #外循环负责重复batch_size//num_sample次这个过程产出完成的batch
        for i in range(batch_size//num_sample):
            k=0
            #target word不作为预测
            for j in list(range(window_size)) + list(range(window_size+1,2*window_size+1)):
                #存储target word
                #[0,1,2,3,target word,5,6,7,8]
                #batch[0] = buffer[4]  batch[1] = buffer[4]
                batch[i*num_sample + k] = buffer[window_size]
                #label[0...7] = buffer[1,2,3,4]和buffer[5,6,7,8]即tarword的上下文单词
                label[i*num_sample + k,0] = buffer[j]
                k += 1
            #存储完一个span,span(buffer)向右移动一个单位,因为span(buffer)是一个deque，即双向队列
            #且上面设置其最大长度为9，再添加一个元素，则队首出队，新元素加入队尾
            #即span由[0,1,2,3,4,5,6,7,8] 变为 [1,2,3,4,5,6,7,8,9]  此时的target word则变成了5
            #故每一个batch有16个target word 对应128个 context word
            buffer.append(data[self.data_index])
            self.data_index = (self.data_index + 1) % len(data)
        return batch,label

    def skip_gram(self):
        tf.reset_default_graph()
        train_dataset = tf.placeholder(tf.int32, shape=[self.batch_size])
        train_labels = tf.placeholder(tf.int32, shape=[self.batch_size, 1])
        valid_dataset = tf.constant(self.valid_examples, dtype=tf.int32)
        #初始化embedding
        embeddings = tf.Variable(tf.random_uniform([self.voca_size, self.embedding_size], -1.0, 1.0))
        #初始化softmax的权重，注意的是softmax就是将原来得到的值映射到[0,1]区间，也可以看作为概率值
        #根据此进行分类和预测
        #算法流程为:词经过嵌入层后变为词向量，再经过softmax函数进行预测和分类得到预测值a，
        #logits = wx + b   softmax(logits) --> a
        #根据交叉熵的作为损失函数 Loss=-Σy*lna，优化权重  y为真实值， a为经过softmax后的预测值
        softmax_weights = tf.Variable(
            tf.truncated_normal([self.voca_size, self.embedding_size],
                                stddev=0.5 / math.sqrt(self.embedding_size))
        )
        softmax_biases = tf.Variable(tf.random_uniform([self.voca_size], 0.0, 0.01))
        #tf.nn.embedding_lookup函数的用法主要是选取一个张量里面索引对应的元素
        #用train_dataset寻找embedding里的张量
        embed = tf.nn.embedding_lookup(embeddings, train_dataset)
        num_sampled = 2*self.window_size
        #定义损失函数
        loss = tf.reduce_mean(
            tf.nn.sampled_softmax_loss(
                weights=softmax_weights, biases=softmax_biases, inputs=embed,
                labels=train_labels, num_sampled=num_sampled, num_classes=self.voca_size)
        )
        #计算minibatch和all embeddings 之间的相似度，用余弦距离
        #规范化因子
        norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keepdims=True))
        normalized_embeddings = embeddings / norm
        valid_embeddings = tf.nn.embedding_lookup(
            normalized_embeddings, valid_dataset)
        similarity = tf.matmul(valid_embeddings, tf.transpose(normalized_embeddings))

        #优化
        optimizer = tf.train.AdagradOptimizer(1.0).minimize(loss)

        num_steps = 100001
        skip_losses = []
        # ConfigProto is a way of providing various configuration settings
        # required to execute the graph
        with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as session:
            # Initialize the variables in the graph
            tf.global_variables_initializer().run()
            print('Initialized')
            average_loss = 0

            # Train the Word2vec model for num_step iterations
            for step in range(num_steps):
                # Generate a single batch of data
                batch_data, batch_labels = self.generat_batch_skip_gram(
                    self.batch_size, self.window_size)

                # Populate the feed_dict and run the optimizer (minimize loss)
                # and compute the loss
                feed_dict = {train_dataset: batch_data, train_labels: batch_labels}
                _, l = session.run([optimizer, loss], feed_dict=feed_dict)

                # Update the average loss variable
                average_loss += l

                if (step + 1) % 2000 == 0:
                    if step > 0:
                        average_loss = average_loss / 2000

                    skip_losses.append(average_loss)
                    # The average loss is an estimate of the loss over the last 2000 batches.
                    print('Average loss at step %d: %f' % (step + 1, average_loss))
                    average_loss = 0

                # Evaluating validation set word similarities
                if (step + 1) % 10000 == 0:
                    sim = similarity.eval()
                    # Here we compute the top_k closest words for a given validation word
                    # in terms of the cosine distance
                    # We do this for all the words in the validation set
                    # Note: This is an expensive step
                    for i in range(self.valid_size):
                        valid_word = reverse_dictionary[self.valid_examples[i]]
                        top_k = 8  # number of nearest neighbors
                        nearest = (-sim[i, :]).argsort()[1:top_k + 1]
                        log = 'Nearest to %s:' % valid_word
                        for k in range(top_k):
                            close_word = reverse_dictionary[nearest[k]]
                            log = '%s %s,' % (log, close_word)
                        print(log)
            skip_gram_final_embeddings = normalized_embeddings.eval()

        # We will save the word vectors learned and the loss over time
        # as this information is required later for comparisons
        np.save('skip_embeddings', skip_gram_final_embeddings)

        with open('skip_losses.csv', 'wt') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(skip_losses)

        num_points = 1000
        tsne = TSNE(perplexity=30,n_components=2,init='pca',n_iter=5000)
        print('Fitting embeddings to T-SNE. This can take some time ...')
        selected_embeddings = skip_gram_final_embeddings[:num_points,:]
        two_d_embeddings = tsne.fit_transform(selected_embeddings)

        print('Pruning the T-SNE embeddings')
        # prune the embeddings by getting ones only more than n-many sample above the similarity threshold
        # this unclutters the visualization
        selected_ids = self.find_cluster_embeddings(selected_embeddings, .25, 10)
        two_d_embeddings = two_d_embeddings[selected_ids, :]

        print('Out of ', num_points, ' samples, ', selected_ids.shape[0], ' samples were selected by pruning')

        # words = [reverse_dictionary[i] for i in selected_ids]
        # self.plot(two_d_embeddings,words)

    def find_cluster_embeddings(self,embeddings,distance_threshold,sample_threshold):
        consine_sim = np.dot(embeddings,np.transpose(embeddings))
        norm = np.dot(np.sum(embeddings ** 2, axis=1).reshape(-1, 1),
                      np.sum(np.transpose(embeddings) ** 2, axis=0).reshape(1, -1))
        assert consine_sim.shape == norm.shape
        consine_sim /= norm
        np.fill_diagonal(consine_sim,-1,0)
        argmax_cos_sim = np.argmax(consine_sim,axis=1)
        mod_cos_sim = consine_sim
        for _ in range(sample_threshold - 1):
            argmax_cos_sim = np.argmax(consine_sim, axis=1)
            mod_cos_sim[np.arange(mod_cos_sim.shape[0]), argmax_cos_sim] = -1

        max_cosine_sim = np.max(mod_cos_sim, axis=1)

        return np.where(max_cosine_sim>distance_threshold)[0]

    def plot(self,embeddings, labels):
        n_clusters = 20  # number of clusters

        # automatically build a discrete set of colors, each for cluster
        label_colors = [pylab.cm.spectral(float(i) / n_clusters) for i in range(n_clusters)]

        assert embeddings.shape[0] >= len(labels), 'More labels than embeddings'

        # Define K-Means
        kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=0).fit(embeddings)
        kmeans_labels = kmeans.labels_

        pylab.figure(figsize=(15, 15))  # in inches

        # plot all the embeddings and their corresponding words
        for i, (label, klabel) in enumerate(zip(labels, kmeans_labels)):
            x, y = embeddings[i, :]
            pylab.scatter(x, y, c=label_colors[klabel])

            pylab.annotate(label, xy=(x, y), xytext=(5, 2), textcoords='offset points',
                           ha='right', va='bottom', fontsize=10)

        # use for saving the figure if needed
        # pylab.savefig('word_embeddings.png')
        pylab.show()

if __name__ == '__main__':
    filename = 'C:/Users/dell/Desktop/WordSegment-master/data/train.txt'
    sg = Skip_gram()
    sg.read_data(filename)
    # print(len(sg.word_list))
    data,word_dictionary,reverse_dictionary,count = sg.build_dataset(sg.word_list)
    # batch,label = sg.generat_batch_skip_gram(8,1)
    sg.skip_gram()