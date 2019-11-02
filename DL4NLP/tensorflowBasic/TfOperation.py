import tensorflow as tf

class TfOperation:
    def compareOp(self):
        x = tf.constant([[1,2],[3,4]],dtype=tf.int32)
        y = tf.constant([[4,3],[3,2]],dtype=tf.int32)

        x_equal_y = tf.equal(x,y,name=None)
        x_less_y = tf.less(x,y,name=None)
        x_greater_equal_y = tf.greater_equal(x,y,name=None)

        condition = tf.constant([[True,False],[True,False]],dtype=tf.bool)
        x_cond_y = tf.where(condition,x,y,name=None)

    def mathOp(self):
        x = tf.constant([[1, 2], [3, 4]], dtype=tf.int32)
        y = tf.constant([[4, 3], [3, 2]], dtype=tf.int32)

        x_add_y = tf.add(x,y)

        x_mul_y = tf.matmul(x,y)

        log_x = tf.log(x)

        x_sum_1 = tf.reduce_sum(x,axis=[1],keepdims=False)
        x_sum_2 = tf.reduce_sum(x,axis=[0],keepdims=True)

        #Segments the tensor acccording to segment_id(item with same id in the same segment)
        #and computes a segmented sum of the data
        data = tf.constant([1,2,3,4,5,6,7,8,9,10],dtype=tf.int32)
        segment_id = tf.constant([0,0,0,1,1,2,2,2,2,2],dtype=tf.int32)
        x_seg_sum = tf.segment_sum(data,segment_id)

    def sepAreduOp(self):
        #1-D scatter op
        #Scatter Update Operation for 1-D
        #[1. 2. 3. 4. 5.]
        #把位置1，3更新为2 4
        ref = tf.Variable(tf.constant([1,9,3,10,5],dtype=tf.float32),name='scatter_update')
        indices = [1,3]
        updates = tf.constant([2,4],dtype=tf.float32)
        tf_scatter_update = tf.scatter_update(ref,indices,updates,use_locking=None,name=None)

        #n-D scatter Op
        #Scatter Operation for n-D
        # [[0 0 0]
        #  [1 1 1]
        #  [0 0 0]
        #  [2 2 2]]
        indices = [[1],[3]]
        updates = tf.constant([[1,1,1],[2,2,2]])
        shape = [4,3]
        tf_scatter_nd_1 = tf.scatter_nd(indices,updates,shape,name=None)

        #1-D gather Op
        params = tf.constant([1,2,3,4,5],dtype=tf.float32)
        indices=[1,4]
        tf_gather = tf.gather(params,indices,validate_indices=True,name=None)

        #n-D gther Op
        params  = tf.constant([[0,0,0],[1,1,1],[2,2,2],[3,3,3]],dtype=tf.float32)
        indices = [[0],[2]]
        tf_gather_nd = tf.gather_nd(params,indices,name=None)

    def nnOp(self):
        #0.active func
        x = tf.constant(value=[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]], dtype=tf.float32, name='x')
        tf.nn.sigmoid(x,name=None)

        #relu activaation of x is given by max(0,x)
        tf.nn.relu(x,name=None)

        #1.conv Op
        #输入通常是四维张量，其维度按[batch_size,height,width,channles]
        x = tf.constant(
            [[
                [[1], [2], [3], [4]],
                [[4], [3], [2], [1]],
                [[5], [6], [7], [8]],
                [[8], [7], [6], [5]]
            ]],
            dtype=tf.float32)
        #4-D tensor [height,weight,in_channels,out_channels]
        #用于 卷积运算的窗口
        x_filter = tf.constant(
            [
                [
                    [[0.5]], [[1]]
                ],
                [
                    [[0.5]], [[1]]
                ]
            ],
            dtype=tf.float32)
        #步长
        x_stride = [1,1,1,1]
        #有SAME和Valid  SAME用0填充输入，使得输入和输出维数一样
        x_padding = 'Valid'
        x_conv = tf.nn.conv2d(input=x,filter=x_filter,strides=x_stride,padding=x_padding)

        #2.pooling Op
        x_ksize= [1,2,2,1]
        x_pool = tf.nn.max_pool(value=x,ksize=x_ksize,strides=x_stride,padding=x_padding)


        #3.define loss
        x = tf.constant([[2,4],[4,8]],dtype=tf.float32)
        x_hat = tf.constant([[1,2],[3,4]],dtype=tf.float32)
        #(pow(1,2) + pow(2,2) + pow(3,2) + pow(4,2)) /2
        MSE = tf.nn.l2_loss(x-x_hat)

        y = tf.constant([[1,0],[0,1]],dtype=tf.float32)
        y_hat = tf.constant([[3,1],[2,5]],dtype=tf.float32)
        CE= tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=y_hat,labels=y))

        #4.optimization
        tf_x = tf.Variable(tf.constant(2.0,dtype=tf.float32),name='x')
        tf_y = tf_x**2
        minimize_Op = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(tf_y)


        #4.control flow
        x = tf.Variable(tf.constant(2.0),name='x')
        with tf.control_dependencies([tf.assign(x,x+5)]):
            z = x*2
