from turtle import Turtle, Screen
import random
import time
import numpy as np




class Board:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.board = np.zeros((x,y))
        self.board[0,:] = 1
        self.board[:,0] = 1
        self.board[x-1,:] = 1
        self.board[:,y-1] = 1
    
    def update(self):
        self.board = np.zeros((self.x,self.y))
        self.board[0,:] = 1
        self.board[:,0] = 1
        self.board[self.x-1,:] = 1
        self.board[:,self.y-1] = 1
        
        
class Snake:
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
    def __init__(self, screen_x, screen_y):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.board = Board(self.screen_x, self.screen_y)
        
        self.snake = Snake(int(screen_x/2), int(screen_y/2))
        self.food = Food(1,1)
        self.place_food()
        
        self.next_move = "RIGHT"
        self.move_selected = True
        self.score = 0
        
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
        if graphics_enabled:
            print(self.board.board)
        
        return True

    def snake_up(self):
        if not self.move_selected and self.next_move != "DOWN":
            self.next_move = "UP"

    def snake_down(self):
        if not self.move_selected and self.next_move != "UP":
            self.next_move = "DOWN"

    def snake_left(self):
        if not self.move_selected and self.next_move != "RIGHT":
            self.next_move = "LEFT"

    def snake_right(self):
        if not self.move_selected and self.next_move != "LEFT":
            self.next_move = "RIGHT"

    def snake_rays(self, normalize):
        c = 1
        while True:
            y, x = self.snake.head
            if self.board.board[y - c, x] != 0:
                if normalize:
                    up = c/self.screen_y
                else:
                    up = c
                    
                if self.board.board[y - c, x] == 2:
                    up_v = 1
                else: 
                    up_v = 0
                break
            c = c + 1
            
        c = 1
        while True:
            y, x = self.snake.head
            if self.board.board[y + c, x] != 0:
                if normalize:
                    down = c/self.screen_y
                else:
                    down = c
                if self.board.board[y + c, x] == 2:
                    down_v = 1
                else:
                    down_v = 0
                break
            c = c + 1
            
        c = 1
        while True:
            y, x = self.snake.head
            if self.board.board[y, x - c] != 0:
                if normalize:
                    left = c/self.screen_x
                else:
                    left = c
                if self.board.board[y, x - c] == 2:
                    left_v = 1
                else:
                    left_v = 0
                break
            c = c + 1
            
        c = 1
        while True:
            y, x = self.snake.head
            if self.board.board[y, x + c] != 0:
                if normalize:
                    right = c/self.screen_x
                else:
                    right = c
                if self.board.board[y, x + c] == 2:
                    right_v = 1
                else:
                    right_v = 0
                break
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
            
        if self.next_move == "UP":
            return [up, left, right, up_v, left_v, right_v, sy, sx, fy, fx]
        if self.next_move == "DOWN":
            return [down, right, left, down_v, right_v, left_v, sy, sx, fy, fx]
        if self.next_move == "RIGHT":
            return [right, up, down, right_v, up_v, down_v, sy, sx, fy, fx]
        if self.next_move == "LEFT":
            return [left, down, up, left_v, down_v, up_v, sy, sx, fy, fx]
        
    def mainloop(self,graphics_enabled, normalization):
        while True:
            x = input()
            if x == "w":
                game.snake_up()
            elif x == "a":
                game.snake_left()
            elif x == "d":
                game.snake_right()
            elif x == "s":
                game.snake_down()
            if not game.next_frame(graphics_enabled):
                break
        return game.score
    
game = Game(8,8)
game.mainloop(True,True)