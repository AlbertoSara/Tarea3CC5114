# -*- coding: utf-8 -*-
#numpy 1.14.0
#matplotlib 2.1.2

import numpy as np
import matplotlib.pyplot as plt
import time
import neuralnetwork
import pygame
import sys

plt.ioff()


if __name__ == "__main__":

    population = 80
    mutation_rate = 0.10
    total_generations = 80
    filename = "grafico.png"
    
    show_last = 5
    x = 16
    y = 10
    ticks = 120
    bonus_ticks = 80
    visual_delay = 0.1
    score_mult = 5
    
    net_arch = [7,5,3]  #el primer elemento es la cantidad de inputs, el ultimo de outputs,
                        #y los intermedios son capas ocultas. [7,5,3] son 7 inputs, 3 outputs
                        #y una sola capa oculta con 5 neuronas
    
    pop = []
    for i in range(population):
        pop.append(neuralnetwork.NeuralNetwork(net_arch))
    
    
    
    graphics_enabled = False
    delay = 0
    generations = 0
    best = []
    best_nn = []
    avg = []
    avg_score = []
    best_score = []
    
    start = time.time()
    while generations < total_generations:
        fitness_array = []
        score_array = []
        for i in pop:
            fitness_array.append(i.fitness(x, y, graphics_enabled, ticks, bonus_ticks, delay, score_mult,0, None))
            score_array.append(i.game_score)
            
        fitness_array.sort()
        score_array.sort()
        best.append(fitness_array[-1])
        avg.append(sum(fitness_array)/population)
        avg_score.append(sum(score_array)/population)
        best_score.append(score_array[-1])
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
    plt.plot(np.arange(len(best_score)), best_score, label="Mejor de cada generación")
    plt.plot(np.arange(len(avg_score)), avg_score, label="Promedio de cada generación")
    plt.xlabel("Generación")
    plt.ylabel("Puntaje")
    
    plt.legend()
    plt.ylim(ymin=min(avg_score))
    plt.xlim(xmin=0)
    
    plt.savefig(filename)
    plt.close()
    print("\n")
    print("Tiempo total: " + str(end-start))
    
    pygame.init()
    screen = pygame.display.set_mode((20*x,20*y))
    for i in range(total_generations - show_last,len(best_nn)):
        best_nn[i].fitness(x, y, True, ticks, bonus_ticks, visual_delay, 1, i+1, screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

    pygame.display.quit()
    pygame.quit()
    sys.exit()