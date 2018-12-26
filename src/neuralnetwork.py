# -*- coding: utf-8 -*-
#numpy 1.14.0

import numpy as np
import snake

class NeuralNetwork:
    def __init__(self, layer_array):
        self.layer_shape = layer_array
        self.layers = []
        self.n_layers = len(layer_array)
        self.fit = 0
        self.game_score = 0
        for i in range(len(layer_array)-1):
                self.layers.append(2*np.random.random((layer_array[i],layer_array[i+1])) - 1)
                

    def feedforward(self, vector):
        output = np.dot(self.layers[0].transpose(), vector)
        for i in range(1, self.n_layers - 1):
            output = self.relu(np.dot(self.layers[i].transpose(), output))
        return output
    
    def relu(self, x):
        y = np.copy(x)
        y[y<0]=0
        return y
        
    def sigmoid(self, x):
        return 1.0/(1+ np.exp(-x))


    def sigmoid_deriv(self, x):
        return x * (1.0 - x)


    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()


    def fitness(self, x, y, graphics_enabled, ticks, bonus_ticks, delay=0, score_mult = 2, gen = 0):
        game = snake.Game(y,x, True)
        self.fit = game.mainloop(graphics_enabled, ticks, bonus_ticks, self, delay, score_mult, gen)
        self.game_score = game.score
        return self.fit


    def reproduce(self, mate, mutation_chance):
        offspring = NeuralNetwork(self.layer_shape)
        
        #transformamos las matrices que representan a las capas en arreglos
        parent1_genes = []
        for i in range(len(self.layers)):
            parent1_genes.append(np.reshape(self.layers[i], (self.layer_shape[i]*self.layer_shape[i+1])))
        
        parent2_genes = []
        for i in range(len(mate.layers)):
            parent2_genes.append(np.reshape(mate.layers[i], (mate.layer_shape[i]*mate.layer_shape[i+1])))
            
        #los arreglos se les puede hacer crossover muy facilmente
        offspring_genes = []
        for i in range(len(parent1_genes)):
            layer_genes = list(parent1_genes[i])
            a = np.random.randint(len(layer_genes))
            layer_genes[0:a] = parent1_genes[i][0:a]
            layer_genes[a:] = parent2_genes[i][a:]
            offspring_genes.append(layer_genes)
        
        #mutamos
        for layer in offspring_genes:
            for i in range(len(layer)):
                if mutation_chance > np.random.random():
                    layer[i] = 2*np.random.random()-1
        
        #transformamos los arreglos de vuelta en matrices
        final_layers = []
        for i in range(len(offspring_genes)):
            final_layers.append(np.reshape(offspring_genes[i],(self.layer_shape[i],self.layer_shape[i+1])))
        
        offspring.layers = final_layers
        
        return offspring
