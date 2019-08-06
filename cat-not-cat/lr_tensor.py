import tensorflow as tf
from lr_utils import read_data
import numpy

def model(train_set_x, train_set_y, test_set_x, test_set_y,num_iterations=1001,learning_rate=0.005):
	X = tf.placeholder(tf.float32,shape=[12288,None])
	Y = tf.placeholder(tf.float32,shape=[1,None])

	w = tf.Variable(tf.zeros([1,12288]),name='weight',dtype=tf.float32)
	b = tf.Variable(tf.zeros([1]),name='bias',dtype=tf.float32)

	#hypothesis = tf.matmul(X,w)+b
	hypothesis = tf.sigmoid(tf.matmul(w,X)+b)

	cost = -tf.reduce_mean(Y*tf.log(hypothesis)+(1-Y)*tf.log(1-hypothesis))
	#cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(hypothesis,Y))
	train = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

	predicted = tf.cast(hypothesis > 0.5,dtype=tf.float32)
	accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted,Y),dtype=tf.float32))

	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())

		train_feed = {X: train_set_x, Y: train_set_y}
		for step in range(num_iterations):
			c,_ = sess.run([cost,train],feed_dict=train_feed)
			if step%100 ==0:
				print(step,c)

		test_feed = {X: test_set_x, Y: test_set_y}
		#h,c,a = sess.run([hypothesis,predicted,accuracy],feed_dict=test_feed)
		a = sess.run([accuracy],feed_dict=test_feed)
		print("\nAccuracy:",a)

if __name__ == '__main__':
	train_set_x, train_set_y, test_set_x, test_set_y = read_data()
	modle(train_set_x, train_set_y, test_set_x, test_set_y,1001,0.005)