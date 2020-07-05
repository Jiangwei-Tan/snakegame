import random
import sys
import time

import pygame
from pygame.locals import *


#初始化窗口
class window:

    def __init__(self):
        #初始化pygame
        pygame.init()
        #移动速度
        self.fpsClock = pygame.time.Clock()
        #创建pygame显示层
        self.playSurface = pygame.display.set_mode((640,480))
        
    #定义结束窗口
    def gameover(self,color):
        #设置字体
        gameoverPrint = pygame.font.SysFont('Arial',60)
        #设置字体属性
        gameoverSurf = gameoverPrint.render('Game Over',True,color)
        #得到文本图像的rect属性
        gameoverRect = gameoverSurf.get_rect()
        #设置文本图像位置
        gameoverRect.midtop = (320,240)
        #在窗口显示
        self.playSurface.blit(gameoverSurf,gameoverRect)
        #刷新屏幕显示
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()



#定义一个Snake类

class Snake:

    def __init__(self):
        #初始化snake出现的位置
        self.snakeHead = [100,100]
        self.snakeBody = [[100,100],[80,100],[60,100]]
        #移动的方向
        self.direction = 'right'
        self.changeDirection = self.direction

    #定义键盘事件
    def key_Event(self):
        #监听事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                #判断键盘事件
                if event.key == K_RIGHT or event.key == ord('d'):
                    self.changeDirection = 'right'
                if event.key == K_LEFT or event.key == ord('a'):
                    self.changeDirection = 'left'
                if event.key == K_UP or event.key == ord('w'):
                    self.changeDirection = 'up'
                if event.key == K_DOWN or event.key == ord('s'):
                    self.changeDirection = 'down'
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))

    #移动
    def move(self):

        #判断是否输入了当前移动方向的反方向
        if self.changeDirection == 'right' and not self.direction == 'left':
            self.direction = self.changeDirection
        if self.changeDirection == 'left' and not self.direction == 'right':
            self.direction = self.changeDirection
        if self.changeDirection == 'up' and not self.direction == 'down':
            self.direction = self.changeDirection
        if self.changeDirection == 'down' and not self.direction == 'up':
            self.direction = self.changeDirection

        #根据方向移动蛇头坐标
        if self.direction == 'right':
            self.snakeHead[0] += 20
        if self.direction == 'left':
            self.snakeHead[0] -= 20
        if self.direction == 'up':
            self.snakeHead[1] -= 20
        if self.direction == 'down':
            self.snakeHead[1] += 20
        
    #定义吃掉食物
    def eat(self,food):
        self.snakeBody.insert(0,list(self.snakeHead))
        #判断是否吃掉了食物
        if self.snakeHead[0] == food.raspberryposition[0] and \
            self.snakeHead[1] == food.raspberryposition[1]:
            #food随机产生的位置
            x = random.randrange(1,32)
            y = random.randrange(1,24)
            food.raspberryposition = [int(x*20),int(y*20)]
        else:
            self.snakeBody.pop()



#定义Food类

class Food:

    def __init__(self):
        #出现位置
        self.raspberryposition = [300,300]




def main():

    #定义颜色
    redColor = pygame.Color(255,0,0)
    blackColor = pygame.Color(0,0,0)
    whiteColor = pygame.Color(255,255,255)
    greyColor = pygame.Color(150,150,150)

    '''
    定义基本元素
    
    画面
    snake
    food
    '''
    user_Interface = window()
    snake = Snake()
    food = Food()

    while True:

        #设置窗口背景色
        user_Interface.playSurface.fill(blackColor)
        #设置snake和food的位置和颜色
        for position in snake.snakeBody:
            pygame.draw.rect(
                user_Interface.playSurface,whiteColor,Rect(
                    position[0],position[1],20,20
                )
            )
            pygame.draw.rect(
                user_Interface.playSurface,redColor,Rect(
                    food.raspberryposition[0],food.raspberryposition[1],20,20
                )
            )
        
        #键盘事件
        snake.key_Event()
        #移动snake
        snake.move()
        #吃食物
        snake.eat(food)

        #判断是否死亡
        if snake.snakeHead[0] > 620 or snake.snakeHead[0] < 0 and\
            snake.snakeHead[1] > 460 or snake.snakeHead[1] < 0:
            user_Interface.gameover(greyColor)
        else:
            for snakebody in snake.snakeBody[1:]:
                if snake.snakeHead[0] == snakebody[0] and snake.snakeHead[1]\
                    == snakebody[1]:
                    user_Interface.gameover(greyColor)

        #刷新界面
        pygame.display.update()

        user_Interface.fpsClock.tick(5)

if __name__ == '__main__':
    main()