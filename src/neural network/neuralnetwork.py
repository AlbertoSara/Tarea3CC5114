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
        self.layers = [0]*(len(hidden_layers)+2)
        self.layers[0] = np.copy(self.input)
        self.layers[len(self.layers) - 1] = self.output
        self.n_layer = len(self.layers)
        
    def feedforward(self):
        for i in range(1, self.n_layer - 1):    
            self.layers[i] = self.sigmoid(np.dot(self.layers[i-1], self.weights[i-1]))

    def backpropagate(self, rate):

        self.errors[len(self.errors)-1] = self.layers[self.n_layer-1] - self.y

        for i in range(len(self.errors) - 2, 0, -1):
            self.errors[i] = np.dot(self.errors[i+1], self.weight[i+1]) *  self.sigmoid_deriv(self.layers[i])

        for i in range(len(self.errors) - 1):
            grad = np.dot(self.errors[i].T, self.layers[i+1].T) / self.input.shape[0]
            self.weights[i] = self.weights[i] - rate*grad
            
    def sigmoid(self, x):
        return 1.0/(1+ np.exp(-x))

    def sigmoid_deriv(self, x):
        return x * (1.0 - x)

    def train(self, e, rate):
        for i in range(e):
            self.feedforward()
            self.backpropagate(rate)


if __name__ == "__main__":

    inpt = np.zeros([1,42])
    clss = np.zeros([1,3])
    with open('data/connect-4.data', 'r') as f:
        i = 0
        for line in f:
            i = i + 1
            if i == 10:
                break
            l = line.replace("b","0").strip(' \t\n\r')
            l = l.replace("x","1")
            l = l.replace("o","2")
            l = l.split(",")
            numbers = np.array([list(map(int, l[0:42]))])
            inpt = np.concatenate((numbers, inpt))   
            if l[42] == "win":
                clss = np.concatenate((np.array([[1,0,0]]),clss))
            elif l[42] == "loss":
                clss = np.concatenate((np.array([[0,1,0]]),clss))
            elif l[42] == "draw":
                clss = np.concatenate((np.array([[0,0,1]]),clss))

    hidden = [3]
    nn = NeuralNetwork(inpt, clss, hidden)

    nn.train(100, 0.1)


input("\n presione enter para continuar")
#TODO no empezar las tareas el mismo dia de la entrega