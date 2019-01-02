import numpy as np
import time
import pygame
import sys


class Board:
    '''
    Tablero
    Se genera un tablero, que se representa con una matriz de numpy
    0 es una celda vacia, 1 un muro, food.val la comida y snake.val la serpiente
        
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.board = np.zeros((x,y))
        self.board[0,:] = 1
        self.board[:,0] = 1
        self.board[x-1,:] = 1
        self.board[:,y-1] = 1
    
    #resetea el tablero
    def update(self):
        self.board = np.zeros((self.x,self.y))
        self.board[0,:] = 1
        self.board[:,0] = 1
        self.board[self.x-1,:] = 1
        self.board[:,self.y-1] = 1
        
        
class Snake:
    '''
    Serpiente
    Es la serpiente del juego
    Se mueve, crece al comer la comida, y muere al chocar consigo misma/una pared
    '''
    def __init__(self, x, y):
        self.body = [(x,y)]
        self.body.append((x, y - 1))
        self.body.append((x, y - 2))
        self.head = self.body[0]
        self.val = 3
        self.nextX = 1
        self.nextY = 0
        
        self.alive = True
    
    def move_right(self, pos):
        posY, posX = self.body[0]
        self.body.insert(0,(posY,posX + 1))
        self.head = self.body[0]
        if not self.body[0] == pos:
            self.body.pop()
            return False
        return True
    
    def move_left(self, pos):
        posY, posX = self.body[0]
        self.body.insert(0,(posY,posX - 1))
        self.head = self.body[0]
        if not self.body[0] == pos:
            self.body.pop()
            return False
        return True
        
    def move_up(self, pos):
        posY, posX = self.body[0]
        self.body.insert(0,(posY - 1,posX))
        self.head = self.body[0]
        if not self.body[0] == pos:
            self.body.pop()
            return False
        return True
    
    def move_down(self, pos):
        posY, posX = self.body[0]
        self.body.insert(0,(posY + 1,posX))
        self.head = self.body[0]
        if not self.body[0] == pos:
            self.body.pop()
            return False
        return True
        
    def check_self_collision(self):
        if len(self.body) == len(set(self.body)):
            return False
        return True

class Food:
    '''
    Comida
    Hace crecer a la serpiente
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.val = 2
        self.pos = (x,y)
        
    def update(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x,y)
        
        
class Game:
    '''
    Juego
    Controla el estado del juego y entrega el vector de input para la
    red neuronal
    '''
    def __init__(self, screen_x, screen_y, normalize):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.board = Board(self.screen_x, self.screen_y)
        
        self.normalize = normalize
        self.fitness_score = 0
        self.snake = Snake(int(screen_x/2), int(screen_y/2))
        self.food = Food(1,1)
        self.place_food()
        
        self.next_move = "RIGHT"
        self.score = 0
        
        self.ticks = 0
        self.size = 20
        self.screen = None
        
        self.gen = 0
    def update_screen(self):
        self.screen.fill((0,0,0))
        for i in range(self.screen_x):
            for j in range(self.screen_y):
                if self.board.board[i,j] == 1:
                    pygame.draw.rect(self.screen, (255,255,255), (j*self.size,i*self.size,self.size,self.size),0)
                    pygame.draw.rect(self.screen, (155,155,155), (j*self.size,i*self.size,self.size,self.size),2)
                elif self.board.board[i,j] == self.food.val:
                    pygame.draw.rect(self.screen, (255,0,0), (j*self.size,i*self.size,self.size,self.size),0)
                    pygame.draw.rect(self.screen, (155,0,0), (j*self.size,i*self.size,self.size,self.size),2)
                elif self.board.board[i,j] == self.snake.val:
                    pygame.draw.rect(self.screen, (0,255,0), (j*self.size,i*self.size,self.size,self.size),0)
                    pygame.draw.rect(self.screen, (0,155,0), (j*self.size,i*self.size,self.size,self.size),2)
        pygame.display.update()       
        pygame.display.set_caption("Generation: " + str(self.gen) + "  Score: " + str(self.score))
    
    def init_screen(self, screen):
        self.screen = screen
        self.screen.fill((0,0,0))
        
    def place_food(self):
        self.food.update(np.random.randint(1, self.screen_x- 1), np.random.randint(1, self.screen_y - 1))
        (x, y) = self.food.pos
        while self.food.pos in self.snake.body or x == 0 or x == (self.screen_x - 1) or y == 0 or y == (self.screen_y - 1):
            self.food.update(np.random.randint(1, self.screen_x- 1), np.random.randint(1, self.screen_y - 1))
            
    def check_collision(self):
        (x,y) = self.snake.head
        if x == 0 or x == (self.screen_x - 1) or y == 0 or y == (self.screen_y - 1):
            return True
        return self.snake.check_self_collision()
    
    def next_frame(self, graphics_enabled):
        
        if self.next_move == "UP":
            self.move_selected = False
            if self.snake.move_up(self.food.pos):
                self.place_food()
                self.score = self.score + 1
        
        elif self.next_move == "DOWN":
            self.move_selected = False
            if self.snake.move_down(self.food.pos):
                self.place_food()
                self.score = self.score + 1
        
        elif self.next_move == "LEFT":
            self.move_selected = False
            if self.snake.move_left(self.food.pos):
                self.place_food()
                self.score = self.score + 1
                
        elif self.next_move == "RIGHT":
            self.move_selected = False
            if self.snake.move_right(self.food.pos):
                self.place_food()
                self.score = self.score + 1       
        
        self.board.update()
        for i in self.snake.body:
            self.board.board[i] = self.snake.val
        
        self.board.board[self.food.pos] = self.food.val
        
        if self.check_collision():
            return False
        
        #wow such graphics
        if graphics_enabled:
            self.update_screen()
        
        return True

    def snake_up(self):
        if self.next_move != "DOWN":
            self.next_move = "UP"

    def snake_down(self):
        if self.next_move != "UP":
            self.next_move = "DOWN"

    def snake_left(self):
        if self.next_move != "RIGHT":
            self.next_move = "LEFT"

    def snake_right(self):
        if self.next_move != "LEFT":
            self.next_move = "RIGHT"

    def snake_turn_left(self):
        if self.next_move == "LEFT":
            self.snake_down()
            return 0
        elif self.next_move == "RIGHT":
            self.snake_up()
            return 0
        elif self.next_move == "UP":
            self.snake_left()
            return 0
        elif self.next_move == "DOWN":
            self.snake_right()
            return 0
            
    def snake_turn_right(self):
        if self.next_move == "LEFT":
            self.snake_up()
            return 0
        elif self.next_move == "RIGHT":
            self.snake_down()
            return 0
        elif self.next_move == "UP":
            self.snake_right()
            return 0
        elif self.next_move == "DOWN":
            self.snake_left()
            return 0
   
    def snake_no_turn(self):
        if self.next_move == "LEFT":
            self.snake_left()
            return 0
        elif self.next_move == "RIGHT":
            self.snake_right()
            return 0
        elif self.next_move == "UP":
            self.snake_up()
            return 0
        elif self.next_move == "DOWN":
            self.snake_down()
            return 0
        
    
    def snake_rays(self, normalize=False):
        c = 1
        up_v = 0
        down_v = 0
        left_v = 0
        right_v = 0
        while c < 2:
            y, x = self.snake.head
            if self.board.board[y - c, x] == 0 or self.board.board[y - c, x] == self.food.val:
                up = 1
            else:
                up = 0
            while self.board.board[y - c, x] != 1:
                if self.board.board[y - c, x] == self.food.val:
                    up_v = 1
                    break
                else:
                    up_v = 0
                c = c + 1
            c = c + 1
            
        c = 1
        while c < 2:
            y, x = self.snake.head
            if self.board.board[y + c, x] == 0 or self.board.board[y + c, x] == self.food.val:
                down = 1
            else:
                down = 0
            while self.board.board[y + c, x] != 1:
                if self.board.board[y + c, x] == self.food.val:
                    down_v = 1
                    break
                else:
                    down_v = 0
                c = c + 1
            c = c + 1
            
        c = 1
        while  c < 2:
            y, x = self.snake.head
            if self.board.board[y, x - c] == 0 or self.board.board[y, x - c] == self.food.val:
                left = 1
            else:
                left = 0
            while self.board.board[y, x - c] != 1:
                if self.board.board[y, x - c] == self.food.val:
                    left_v = 1
                    break
                else:
                    left_v = 0
                c = c + 1
            c = c + 1
            
        c = 1
        while  c < 2:
            y, x = self.snake.head
            if self.board.board[y, x + c] == 0 or self.board.board[y, x + c] == self.food.val:
                right = 1
            else:
                right = 0
            while self.board.board[y, x + c] != 1:
                if self.board.board[y, x + c] == self.food.val:
                    right_v = 1
                    break
                else:
                    right_v = 0
                c = c + 1
            c = c + 1
        
        if normalize:
            sy, sx = self.snake.head
            sy = sy/self.screen_y
            sx = sx/self.screen_x
            fy, fx = self.food.pos
            fy = fy/self.screen_y
            fx = fx/self.screen_x
        else:
            sy, sx = self.snake.head
            fy, fx = self.food.pos
            
        dist = np.linalg.norm((fy - sy, fx - sx))
        
        if self.next_move == "UP":
            return [up, left, right, up_v, left_v, right_v, dist]
        if self.next_move == "DOWN":
            return [down, right, left, down_v, right_v, left_v, dist]
        if self.next_move == "RIGHT":
            return [right, up, down, right_v, up_v, down_v, dist]
        if self.next_move == "LEFT":
            return [left, down, up, left_v, down_v, up_v, dist]
    
    def mainloop(self,graphics_enabled, ticks, bonus_ticks, neural_network, delay, score_mult, gen, screen):
        self.gen = gen
        last_dist = 100000
        if graphics_enabled:
            self.init_screen(screen)
        while ticks:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                        
            self.ticks = ticks
            last_score = self.score
            inp = self.snake_rays(self.normalize)
            out = neural_network.feedforward(inp)
            

            if last_dist > inp[-1]:
                self.fitness_score += 0.5 
            else:
                self.fitness_score -= 1
                
            last_dist = inp[-1]
            x = np.argmax(out)
            if x == 0:
                self.snake_no_turn()
            elif x == 1:
                self.snake_turn_left()
            elif x == 2:
                self.snake_turn_right()
                
            if not self.next_frame(graphics_enabled):
                self.fitness_score -= 20
                break
            if last_score != self.score:
                ticks = ticks + bonus_ticks
            ticks = ticks - 1
            time.sleep(delay)    
        if self.score == 0:
            self.fitness_score -= 10
        if graphics_enabled:
            time.sleep(1)
        
        return self.fitness_score + ((self.score)*score_mult)**1.02
