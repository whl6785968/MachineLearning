import tensorflow as tf

class tensorflowTest:
    def interactive(self):
        sess = tf.InteractiveSession()
        x = tf.Variable([1.0,2.0])
        y = tf.Variable([3.0,3.0])

        x.initializer.run()
        sub = tf.subtract(x,y)
        return sub

    def varibale_test(self):
        state = tf.Variable(0,name='counter')
        one = tf.constant(1)
        new_value = tf.add(state,one)
        update = tf.assign(state,new_value)
        init_op = tf.initialize_all_variables()

        with tf.Session() as sess:
            sess.run(init_op)
            print(sess.run(state))

            for _ in range(3):
                sess.run(update)
                print(sess.run(state))

if __name__ == '__main__':
    tt = tensorflowTest()
    # result = tt.interactive()
    # print(result)
    tt.varibale_test()