import logistic_regression as lr #for test_1
import l_r #for test_2
import lr_tensor as lt

from lr_utils import read_data
import numpy as np
import matplotlib.pyplot as plt
import h5py
import scipy
from PIL import Image
from scipy import ndimage

all_step = 1001
learning_rate = 0.005
f_name = "test_3"

def test_1(train_set_x, train_set_y, test_set_x, test_set_y):
	d = lr.model(train_set_x, train_set_y, test_set_x, test_set_y,\
			num_iterations = all_step, learning_rate = learning_rate, print_cost = True)

	#plot learning curve(with costs)  
	costs = np.squeeze(d['costs'])
	#print(costs.shape)
	plt.plot(costs)  
	plt.ylabel('cost')
	plt.xlabel('iterations (per hundreds)')  
	plt.title("learning rate = " + str(d['learning_rate']))  
	plt.show()

def test_2(train_set_x, train_set_y, test_set_x, test_set_y):
	d = l_r.model(train_set_x, train_set_y, test_set_x, test_set_y,\
			num_iterations = all_step, learning_rate = learning_rate, print_cost = True)

	#plot learning curve(with costs)  
	costs = np.squeeze(d['costs'])
	#print(costs.shape)
	plt.plot(costs)  
	plt.ylabel('cost')
	plt.xlabel('iterations (per hundreds)')  
	plt.title("learning rate = " + str(d['learning_rate']))  
	plt.show()

	#plot learning curve(with train_accs)  
	train_accs = np.squeeze(d['train_accs'])
	#print(train_accs.shape)
	plt.plot(train_accs)  
	plt.ylabel('train_acc')
	plt.xlabel('iterations (per hundreds)')  
	plt.title("learning rate = " + str(d['learning_rate']))  
	plt.show()

	#plot learning curve(with test_accs)  
	test_accs = np.squeeze(d['test_accs'])
	#print(test_accs.shape)
	plt.plot(test_accs)  
	plt.ylabel('test_acc')
	plt.xlabel('iterations (per hundreds)')  
	plt.title("learning rate = " + str(d['learning_rate']))  
	plt.show()

def test_3(train_set_x, train_set_y, test_set_x, test_set_y):
	lt.model(train_set_x, train_set_y, test_set_x, test_set_y,\
		num_iterations = all_step, learning_rate = learning_rate)

if __name__ == '__main__':
	train_set_x, train_set_y, test_set_x, test_set_y = read_data()
	if f_name == "test_1":
		test_1(train_set_x, train_set_y, test_set_x, test_set_y)  #use logistic_regression.py
	elif f_name == "test_2":
		test_2(train_set_x, train_set_y, test_set_x, test_set_y)	#use l_r.py
	elif f_name == "test_3":
		test_3(train_set_x, train_set_y, test_set_x, test_set_y)	#use lr_tensor.py
