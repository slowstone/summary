#lr_utils.py  
import numpy as np
import h5py

'''
train_set_x_orig shape (209, 64, 64, 3)
train_set_y shape (1, 209)
test_set_x_orig shape (50, 64, 64, 3)
test_set_y shape (1, 50)
train_set_x_flatten shape (209, 12288)
test_set_x_flatten shape (50, 12288)
train_set_x shape (209, 12288)
train_set_y shape (209, 1)
test_set_x shape (50, 12288)
test_set_y shape (50, 1)

'''
def load_dataset():  
    train_dataset = h5py.File('dataset/train_catvnoncat.h5', "r")  
    train_set_x_orig = np.array(train_dataset["train_set_x"][:]) # your train set features  
    train_set_y_orig = np.array(train_dataset["train_set_y"][:]) # your train set labels  
  
    test_dataset = h5py.File('dataset/test_catvnoncat.h5', "r")  
    test_set_x_orig = np.array(test_dataset["test_set_x"][:]) # your test set features  
    test_set_y_orig = np.array(test_dataset["test_set_y"][:]) # your test set labels  
  
    classes = np.array(test_dataset["list_classes"][:]) # the list of classes  
      
    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))  
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))  
      
    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes

def reshape_image(image):
    return image.reshape(-1,image.shape[0])

def read_data():
    train_set_x_orig,train_set_y,test_set_x_orig,test_set_y,classes= load_dataset()

    print('train_set_x_orig shape ' + str(train_set_x_orig.shape))  
    print('train_set_y shape ' + str(train_set_y.shape))  
    print('test_set_x_orig shape ' + str(test_set_x_orig.shape))  
    print('test_set_y shape ' + str(test_set_y.shape)) 

    #reshape the training and test examples  
    train_set_x_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T 
    test_set_x_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T
    print('train_set_x_flatten shape ' + str(train_set_x_flatten.shape))  
    print('test_set_x_flatten shape ' + str(test_set_x_flatten.shape))  

    #standardize our dataset  
    train_set_x = train_set_x_flatten / 255
    test_set_x = test_set_x_flatten / 255

    print('train_set_x shape ' + str(train_set_x.shape))  
    print('train_set_y shape ' + str(train_set_y.shape))  
    print('test_set_x shape ' + str(test_set_x.shape))  
    print('test_set_y shape ' + str(test_set_y.shape))

    return train_set_x, train_set_y, test_set_x, test_set_y

if __name__ == '__main__':
    read_data()