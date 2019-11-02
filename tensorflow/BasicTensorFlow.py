import tensorflow as tf

if __name__ == '__main__':
    #矩阵1 op1
    matrix1 = tf.constant([[3.,3.]])
    #矩阵2 op2
    matrix2 = tf.constant([[2.],[2.]])
    #矩阵3 op3
    product = tf.matmul(matrix1,matrix2)
    print(product)
    #启动图
    sess = tf.Session()
    #run方法会触发图中三个op的执行
    result = sess.run(product)
    print(result)
    sess.close()