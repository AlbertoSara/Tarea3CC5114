# -*- coding: utf-8 -*-
#numpy 1.14.0
#matplotlib 2.1.2

import numpy as np
import matplotlib.pyplot as plt
import time
import neuralnetwork

if __name__ == "__main__":

    population = 50
    mutation_rate = 0.10
    total_generations = 200
    filename = "grafico.png"
    
    x = 16
    y = 10
    graphics_enabled = False
    ticks = 50
    bonus_ticks = 10 
    delay = 0
    score_mult = 5
    
    pop = []
    for i in range(population):
        pop.append(neuralnetwork.NeuralNetwork([7,5,3]))
    
    generations = 0
    best = []
    best_nn = []
    avg = []
    
    start = time.time()
    while generations < total_generations:
        fitness_array = []
        
        for i in pop:
            fitness_array.append(i.fitness(x, y, graphics_enabled, ticks, bonus_ticks, delay, score_mult))
            
        fitness_array.sort()
        best.append(fitness_array[-1])
        avg.append(sum(fitness_array)/population)
        threshold = fitness_array[int(population*.90)]
        mating_pool = []
        
        for i in pop:
            if i.fit >= threshold:
                mating_pool.append(i)
            if i.fit == fitness_array[-1]:
                best_nn.append(i)
                
        pop = []
        for i in range(population):
            a = np.random.randint(len(mating_pool))
            b = np.random.randint(len(mating_pool))
            pop.append(mating_pool[a].reproduce(mating_pool[b], mutation_rate))
            
        generations += 1
        
    end = time.time()
    plt.plot(np.arange(len(best)), best, label="Mejor de cada generación")
    plt.plot(np.arange(len(avg)), avg, label="Promedio de cada generación")
    plt.xlabel("Generación")
    plt.ylabel("Puntaje (fitness)")
  #  plt.title("Evolución de la población de soluciones para \n" \
  #            "el problema de N-Queens con n = " + str(board_size) + 
  #            ",\n probablidad de mutación: " + str(mutation_rate) +
  #            ", y población por generación de: " + str(population))
    
    plt.legend()
    plt.ylim(ymin=min(avg))
    plt.xlim(xmin=0)
    
    #plt.show()
    plt.savefig(filename)
    print("\n")
    print("Generaciones totales: " + str(generations))
    print("Tiempo total: " + str(end-start))
    
    best_nn[-1].fitness(x, y, True, ticks, bonus_ticks, 0.5)