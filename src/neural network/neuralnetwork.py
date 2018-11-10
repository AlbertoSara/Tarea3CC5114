# -*- coding: utf-8 -*-
#numpy 1.14.0

import numpy as np



class NeuralNetwork:
    def __init__(self, inp, outp, hidden_layers):
        self.input = inp           
        self.y = outp
        self.output = np.zeros(self.y.shape)
        self.weights = [0]*(len(hidden_layers) + 1)
        self.errors = [0]*(len(hidden_layers) + 1)
        self.weights[0] = np.random.rand(self.input.shape[1],hidden_layers[0])
        self.errors[0] = np.zeros([self.input.shape[1],hidden_layers[0]])
        
        for i in range (1, len(hidden_layers) + 1):
            self.weights[i] = np.random.rand(self.weights[i-1].shape[1], hidden_layers[i-1])
            self.errors[i] = np.zeros([self.errors[i-1].shape[1], hidden_layers[i-1]])   
        self.weights[len(self.weights) - 1] = np.random.rand(self.weights[len(self.weights) - 1].shape[1], self.y.shape[0])    
        self.errors[len(self.errors) - 1] = np.zeros([self.errors[len(self.errors) - 1].shape[1], self.y.shape[0]])    
        print(self.weights)
        print("---")
        print(self.errors)
        print("---")
        print("---")
        print("---")
        print("---")
        self.layers = [0]*(len(hidden_layers)+2)
        self.layers[0] = np.copy(self.input)
        self.layers[len(self.layers) - 1] = self.output
        self.n_layer = len(self.layers)
        
    def feedforward(self):
        for i in range(1, self.n_layer - 1):    
            self.layers[i] = self.sigmoid(np.dot(self.layers[i-1], self.weights[i-1]))

    def backpropagate(self, rate):

        self.errors[len(self.errors)-1] = self.layers[self.n_layer-1] - self.y
        print("---")
        print("---")
        print("---")
        print("layers")
        print(self.layers)
        print("---")
        print("---")
        print("---")
        print("---")
        print("---")
        
        print(self.errors)
        print("---")
        print("---")
        print("---")
        print("---")
        print("---")
        for i in range(len(self.errors) - 2, 0, -1):
            self.errors[i] = np.dot(self.errors[i+1], self.weight[i+1]) *  self.sigmoid_deriv(self.layers[i])
        print(self.errors)
        print("---")
        print(self.weights)
        print("---")
        print(self.layers)
        for i in range(len(self.errors) - 1):
            grad = np.dot(self.errors[i].T, self.layers[i+1].T) / self.input.shape[0]
            self.weights[i] = self.weights[i] - rate*grad
            
    def sigmoid(self, x):
        return 1.0/(1+ np.exp(-x))

    def sigmoid_deriv(self, x):
        return x * (1.0 - x)

 #   def backpropagation(self):
        
 #       self.errors[]

    def train(self, e, rate):
        for i in range(e):
            self.feedforward()
            self.backpropagation()


if __name__ == "__main__":
    X = np.array([[0,0,1],
                  [0,1,1]])
    
    y = np.array([[0],[1],[1],[0]])
    z = [3]
    nn = NeuralNetwork(X,y, z)

    for i in range(4):
#        print(nn.layers)
#        print("\n layers")
#        print(nn.input)
#        print("\n input")
#        print(nn.output)
#        print("\n output")
#        print(nn.y)
#        print("\n target")
#        print(nn.weights)
#        print("\n weights")
        nn.feedforward()
        nn.backpropagate(0.1)
