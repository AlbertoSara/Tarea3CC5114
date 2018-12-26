# Tarea3CC5114

Este proyecto consiste en una red neuronal, que entrenada utilizando algoritmos genéticos, logra aprender a jugar y obtener altos puntajes en el juego "Snake".

Contiene 3 archivos:


-neuralnetwork.py

  Contiene la implementación de la red neuronal. Como este es el objeto que evoluciona durante el proyecto, es menos generalizada y tiene detalles de implementación para funcionar con este proyecto en particular.
  
  
-snake.py

  Contiene la implementación del juego. Además, contiene la función de fitness, y genera el vector de características para la red. Actualmente no tiene gráficos dedicados, e imprime el tablero en pantalla para cada paso del juego.


-gen_algorithm.py

  Contiene el algoritmo genético en si. En las primeras líneas se puede configurar distintos aspectos (población, número de generaciones, tamaño del tablero, etc.). Itera por la población calculando su fitness, elige un porcentaje de los mejores, los reproduce, y repite el proceso por las generaciones deseadas. Finalmente, genera un gráfico y hace un juego de demostración con la mejor inteligencia artificial. 
  

Dependencias:

-numpy

-matplotlib

-pygame

Python 3.6

  
  
