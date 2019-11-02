import tensorflow as tf
import numpy as np

if __name__ == '__main__':
    graph = tf.Graph()
    session = tf.InteractiveSession(graph=graph)
    #占位符，在session.run时提供数据即可
    # x = tf.placeholder(shape=[1,10],dtype=tf.float32,name='x')
    x = tf.constant(value=[[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]],dtype=tf.float32,name='x')
    #在minval = -0.1和maxval = 0.1之间均匀采样
    W = tf.Variable(tf.random_uniform(shape=[10,5],minval=-0.1,maxval=0.1,dtype=tf.float32),name='W')
    b = tf.Variable(tf.zeros(shape=[5],dtype=tf.float32),name='b')
    h = tf.nn.sigmoid(tf.matmul(x,W) + b)
    #初始化图中的变量W和b
    tf.global_variables_initializer().run()
    h_eval = session.run(h)
    print(h_eval)
    session.close()