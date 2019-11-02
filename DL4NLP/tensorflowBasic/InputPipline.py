import tensorflow as tf
import numpy as np

if __name__ == '__main__':
    path = 'C:\\Users\\dell\\Desktop\\Natural-Language-Processing-with-TensorFlow-master\\ch2\\'
    graph = tf.Graph()
    session = tf.InteractiveSession(graph=graph)

    #定义文件名队列,它将作为参数传递给读取器，读取器根据此读取文件
    filenames = [path+'test%d.txt' % i for i in range(1,4)]

    for f in filenames:
        if not tf.gfile.Exists(f):
            raise ValueError('Failed to find file:' + f)
        else:
            print('File %s found' % f)
    #capacity：给定时间队列持有的数据量
    filename_quque = tf.train.string_input_producer(filenames,capacity=3,shuffle=True,name='string_input_producer')
    reader = tf.TextLineReader()

    key,value = reader.read(filename_quque,name='text_read_op')
    #定义record_defaults，如果发现任何错误记录，则输出他
    record_defaults = [[-1.0], [-1.0], [-1.0], [-1.0], [-1.0], [-1.0], [-1.0], [-1.0], [-1.0], [-1.0]]
    #将读取到的文本行解码为数字列
    col1,col2,col3,col4,col5,col6,col7,col8,col9,col10 = tf.decode_csv(value,record_defaults=record_defaults)
    print('col1 is ' + str(col1))
    #拼接列，形成单个张量
    features = tf.stack([col1,col2,col3,col4,col5,col6,col7,col8,col9,col10])
    print('features is ' + str(features))
    #batch_size:在给定步骤中对数据采样的批次大小
    #capcity：数据队列的容量
    #min_after_dequeue：表示出队后留在队列中的最小元素数量
    x = tf.train.shuffle_batch([features],batch_size=5,capacity=5,name='data_batch',min_after_dequeue=1,num_threads=1)
    #线程管理器
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord,sess=session)

    W = tf.Variable(tf.random_uniform(shape=[10, 5], minval=-0.1, maxval=0.1, dtype=tf.float32), name='W')
    b = tf.Variable(tf.zeros(shape=[5], dtype=tf.float32), name='b')
    h = tf.nn.sigmoid(tf.matmul(x, W) + b)

    tf.global_variables_initializer().run()


    for step in range(3):
        x_eval, h_eval = session.run([x, h])
        print('====Step %d====' % step)
        print('Evaluated data (x)')
        print(x_eval)
        print('Evaluated data (h)')
        print(h_eval)

    coord.request_stop()
    coord.join(threads)
    session.close()

    # # Defining the graph and session
    # graph = tf.Graph()  # Creates a graph
    # session = tf.InteractiveSession(graph=graph)  # Creates a session
    #
    # # The filename queue
    # filenames = [path+'test%d.txt' % i for i in range(1, 4)]
    # filename_queue = tf.train.string_input_producer(filenames, capacity=3, shuffle=True, name='string_input_producer')
    #
    # # check if all files are there
    # for f in filenames:
    #     if not tf.gfile.Exists(f):
    #         raise ValueError('Failed to find file: ' + f)
    #     else:
    #         print('File %s found.' % f)
    #
    # # Reader which takes a filename queue and
    # # read() which outputs data one by one
    # reader = tf.TextLineReader()
    #
    # # ready the data of the file and output as key,value pairs
    # # We're discarding the key
    # key, value = reader.read(filename_queue, name='text_read_op')
    #
    # # if any problems encountered with reading file
    # # this is the value returned
    # record_defaults = [[-1.0], [-1.0], [-1.0], [-1.0], [-1.0], [-1.0], [-1.0], [-1.0], [-1.0], [-1.0]]
    #
    # # decoding the read value to columns
    # col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = tf.decode_csv(value, record_defaults=record_defaults)
    # features = tf.stack([col1, col2, col3, col4, col5, col6, col7, col8, col9, col10])
    #
    # # output x is randomly assigned a batch of data of batch_size
    # # where the data is read from the txt files
    # x = tf.train.shuffle_batch([features], batch_size=3,
    #                            capacity=5, name='data_batch',
    #                            min_after_dequeue=1, num_threads=1)
    #
    # # QueueRunner retrieve data from queues and we need to explicitly start them
    # # Coordinator coordinates multiple QueueRunners
    # coord = tf.train.Coordinator()
    # threads = tf.train.start_queue_runners(coord=coord, sess=session)
    #
    # # Building the graph by defining the variables and calculations
    #
    # W = tf.Variable(tf.random_uniform(shape=[10, 5], minval=-0.1, maxval=0.1, dtype=tf.float32), name='W')  # Variable
    # b = tf.Variable(tf.zeros(shape=[5], dtype=tf.float32), name='b')  # Variable
    #
    # h = tf.nn.sigmoid(tf.matmul(x, W) + b)  # Operation to be performed
    #
    # # Executing operations and evaluating nodes in the graph
    # tf.global_variables_initializer().run()  # Initialize the variables
    #
    # # Calculate h with x and print the results for 5 steps
    # for step in range(5):
    #     x_eval, h_eval = session.run([x, h])
    #     print('========== Step %d ==========' % step)
    #     print('Evaluated data (x)')
    #     print(x_eval)
    #     print('Evaluated data (h)')
    #     print(h_eval)
    #     print('')
    #
    # # We also need to explicitly stop the coordinator
    # # otherwise the process will hang indefinitely
    # coord.request_stop()
    # coord.join(threads)
    # session.close()