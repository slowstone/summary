import numpy as np

def sigmoid(z):
	output = 1/(1+np.exp(-z))
	return output

def sigmoid_derivative(z):
	s = sigmoid(z)
	output = s*(1-s)
	return s

def initialize_with_zeros(dim):
	w = np.zeros((dim,1))
	b = 0

	assert(w.shape==(dim,1))
	assert(isinstance(b, float) or isinstance(b, int))

	return w,b

#L1(ŷ ,y)=∑(y(i)−ŷ (i))2
def L1(y,yhat):
	loss = np.sum(np.dot(yhat-y,yhat-y))
	return loss

#L2(ŷ ,y)=∑(ylog(ŷ)+(1-y)log(1-ŷ))
def L2(y,yhat):
	s1 = np.log(yhat)
	s2 = np.log(1-yhat)
	loss = np.sum(y*s1+(1-y)*s2)
	return -loss


#前项、后项传播  
def propagate(w, b, X, Y):  
    """ 
    Arguments: 
    w -- weights, a numpy array of size (num_px * num_px * 3, 1) 
    b -- bias, a scalar 
    X -- data of size (num_px * num_px * 3, number of examples) 
    Y -- true "label" vector (containing 0 if non-cat, 1 if cat) of size (1, number of examples) 
     
    Return: 
    cost -- negative log-likelihood cost 
    dw -- gradient of the loss with respect to w 
    db -- gradient of the loss with respect to b 
    """  
    m = X.shape[1]  
    #forward propagation (from X to cost)  
    A = sigmoid(np.dot(w.T, X) + b)  
    cost = -1./m * np.sum(Y * np.log(A) + (1 - Y) * np.log(1 - A))
    #cost = 1/m * L2(Y,A)
      
    #backward propagation
    dw = 1 / m * np.dot(X, (A - Y).T)  
    db = 1 / m * np.sum(A - Y, axis = 1, keepdims = True)  
      
    assert(dw.shape == w.shape)  
    assert(db.dtype == float)  
    cost = np.squeeze(cost)  
    assert(cost.shape == ())  
      
    grads = {"dw" : dw,  
             "db" : db}  
    return grads, cost 

#optimization  
def optimize(w,b,X,Y,num_iterations,learning_rate,print_cost=False):  
    """ 
    This function optimizes w and b by running a gradient descent algorithm 
     
    Arguments: 
    w -- weights, a numpy array of size (num_px * num_px * 3, 1) 
    b -- bias, a scalar 
    X -- data of shape (num_px * num_px * 3, number of examples) 
    Y -- true "label" vector (containing 0 if non-cat, 1 if cat), of shape (1, number of examples) 
    num_iterations -- number of iterations of the optimization loop 
    learning_rate -- learning rate of the gradient descent update rule 
    print_cost -- True to print the loss every 100 steps 
     
    Returns: 
    params -- dictionary containing the weights w and bias b 
    grads -- dictionary containing the gradients of the weights and bias with respect to the cost function 
    costs -- list of all the costs computed during the optimization, this will be used to plot the learning curve. 
     
    Tips: 
    You basically need to write down two steps and iterate through them: 
        1) Calculate the cost and the gradient for the current parameters. Use propagate(). 
        2) Update the parameters using gradient descent rule for w and b. 
    """  
    costs = []  
      
    for i in range(num_iterations):  
        grads, cost = propagate(w, b, X, Y)  
          
        dw = grads['dw']  
        db = grads['db']  
          
        #update rule  
        w = w - learning_rate * dw  
        b = b - learning_rate * db  
        
        if i % 100 == 0:  
            costs.append(cost)  
          
        if print_cost and i % 100 == 0:  
            print("cost after iteration %i: %f" % (i, cost))  
              
    params = {'w' : w,  
              'b' : b}  
      
    return params, grads, costs

def predict(w,b,X):  
    ''''' 
    Predict whether the label is 0 or 1 using learned logistic regression parameters (w, b) 
     
    Arguments: 
    w -- weights, a numpy array of size (num_px * num_px * 3, 1) 
    b -- bias, a scalar 
    X -- data of size (num_px * num_px * 3, number of examples) 
     
    Returns: 
    Y_prediction -- a numpy array (vector) containing all predictions (0/1) for the examples in X 
    '''  
    m = X.shape[1]  
    Y_prediction = np.zeros((1,m))  
    w = w.reshape(X.shape[0], 1)  
      
    A = sigmoid(np.dot(w.T, X) + b)  
      
    for i in range(A.shape[1]):  
        if A[0,i] > 0.5:  
            Y_prediction[0,i] = 1  
        else:  
            Y_prediction[0,i] = 0  
      
    assert(Y_prediction.shape == (1, m))  
      
    return Y_prediction

def model(X_train,Y_train,X_test,Y_test,num_iterations=2000,learning_rate=0.5,print_cost=True):  
    """ 
    Builds the logistic regression model by calling the function you've implemented previously 
     
    Arguments: 
    X_train -- training set represented by a numpy array of shape (num_px * num_px * 3, m_train) 
    Y_train -- training labels represented by a numpy array (vector) of shape (1, m_train) 
    X_test -- test set represented by a numpy array of shape (num_px * num_px * 3, m_test) 
    Y_test -- test labels represented by a numpy array (vector) of shape (1, m_test) 
    num_iterations -- hyperparameter representing the number of iterations to optimize the parameters 
    learning_rate -- hyperparameter representing the learning rate used in the update rule of optimize() 
    print_cost -- Set to true to print the cost every 100 iterations 
     
    Returns: 
    d -- dictionary containing information about the model. 
    """  
      
    ### START CODE HERE ###  
      
    # initialize parameters with zeros (≈ 1 line of code)  
    w, b = initialize_with_zeros(X_train.shape[0])  
  
    # Gradient descent (≈ 1 line of code)  
    parameters, grads, costs = optimize(w,b,X_train,Y_train,num_iterations,learning_rate,print_cost)  
      
    # Retrieve parameters w and b from dictionary "parameters"  
    w = parameters["w"]  
    b = parameters["b"]  
      
    # Predict test/train set examples (≈ 2 lines of code)  
    Y_prediction_test = predict(w,b,X_test)
    Y_prediction_train = predict(w,b,X_train)
  
    ### END CODE HERE ###  
  
    # Print train/test Errors  
    print("train accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_train - Y_train)) * 100))  
    print("test accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_test - Y_test)) * 100))  
  
      
    d = {"costs": costs,  
         "Y_prediction_test": Y_prediction_test,   
         "Y_prediction_train" : Y_prediction_train,   
         "w" : w,   
         "b" : b,  
         "learning_rate" : learning_rate,  
         "num_iterations": num_iterations}  
      
    return d