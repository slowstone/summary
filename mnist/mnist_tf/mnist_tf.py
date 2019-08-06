from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

import tensorflow.examples.tutorials.mnist.input_data as input_data
mnist = input_data.read_data_sets('../data', one_hot=True)

sess = tf.InteractiveSession()

with tf.name_scope('input') as scope:
	x = tf.placeholder("float", shape=[None, 784])
	y_ = tf.placeholder("float", shape=[None, 10])
	W = tf.Variable(tf.zeros([784,10]))
	#b = tf.Variable(tf.zeros([10]))

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

with tf.name_scope('conv1') as scope:
	#第一层卷积
	W_conv1 = weight_variable([5, 5, 1, 32])
	b_conv1 = bias_variable([32])

	x_image = tf.reshape(x, [-1,28,28,1])

	h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
	h_pool1 = max_pool_2x2(h_conv1)

with tf.name_scope('conv2') as scope:
	#第二层卷积
	W_conv2 = weight_variable([5, 5, 32, 64])
	b_conv2 = bias_variable([64])

	h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
	h_pool2 = max_pool_2x2(h_conv2)

with tf.name_scope('fc1') as scope:
	#密集连接层
	W_fc1 = weight_variable([7 * 7 * 64, 1024])
	b_fc1 = bias_variable([1024])

	h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
	h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

with tf.name_scope('Dropout') as scope:
	#Dropout防止过拟合
	keep_prob = tf.placeholder("float")
	h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

with tf.name_scope('output') as scope:
	#输出层
	W_fc2 = weight_variable([1024, 10])
	b_fc2 = bias_variable([10])

	y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

with tf.name_scope('accuracy') as scope:
	#准确率
	cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))

	#tf.summary.scalar('loss',cross_entropy)

	train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
	#train_step = tf.train.GradientDescentOptimizer(1e-4).minimize(cross_entropy)
	correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
	#tf.summary.scalar('accuracy', accuracy)

with tf.name_scope('train') as scope:
	#训练

	#merged = tf.summary.merge_all()
	#writer = tf.summary.FileWriter("logs/", sess.graph)

	sess.run(tf.global_variables_initializer())
	for i in range(6001):
		batch = mnist.train.next_batch(50)
		if i%1000 == 0:
			train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
			#评估
			test_accuracy = accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0})
			#print("test_accuracy %g"%(test_accuracy))
			#tf.summary.scalar('test_accuracy', test_accuracy)
			#summary_str = sess.run(merged)
			print ("step %d, training accuracy %g, test_accuracy %g"%(i, train_accuracy, test_accuracy))
			#writer.add_summary(summary_str, train_accuracy)
	   		#writer.add_summary (summary_str, i)  
		train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})