#!/usr/bin/python3

import sys
import random as rand
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Snake:
    def __init__(self):
        self.body = [[10,10],[10,9],[10,8]]

    def move(self, newhead):
        self.body.insert(0,[newhead[0],newhead[1]])

    def eat(self, eat):
        if(eat is False):
            tail =  self.body.pop()
            return tail


class Box(QWidget):

    pal = QPalette()

    def __init__(self,cx,cy):
        super().__init__()
        self.x = cx
        self.y = cy
        self.pal.setColor(QPalette.Background, QColor(15,15,15,25))
        self.setAutoFillBackground(True)
        self.setPalette(self.pal)
        self.setFixedSize(10,10)

    def changeColor(self, color):
        self.pal.setColor(QPalette.Background, color)
        self.setPalette(self.pal)


class Grid(QWidget):

    gbox = []
    timer = QBasicTimer()
    key_pressed = Qt.Key_Right
    cur_x = 5
    cur_y = 5
    snake = Snake()
    food = [0,0]
    c = 0
    score=0

    def __init__(self):
        super().__init__()
        self.label = QLabel("Score:")
        self.setWindowTitle("Snek")
        self.setFixedSize(350, 350)
        self.lscore = QLabel()

        gridP = QVBoxLayout(self)   
        gridH = QHBoxLayout()
        gridL = QGridLayout() 
        gridL.setSpacing(2.5)

        row = []
        for i in range(0,25):
            for j in range(0,25):
                element = Box(i,j)
                row.append(element)
                gridL.addWidget(row[j],i,j)
            self.gbox.append(list(row))
            row.clear()

        gridP.addLayout(gridL)
        gridH.addWidget(self.label)
        gridH.addWidget(self.lscore)
        gridP.addLayout(gridH)

        self.newFood()
        self.timer.start(100,self)
        self.setLayout(gridP)
        self.show()

    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_Escape):
            self.label.setText("Pause")
            self.lscore.setText("")
            self.timer.stop()
        else :
            if(not self.timer.isActive()):
                self.timer.start(100,self)
                self.label.setText("Score")
                self.lscore.setText(str(self.score))
            if(event.key() in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Down, Qt.Key_Up]):
            	self.key_pressed = event.key()

    def timerEvent(self, event):
        if(self.timer.isActive()):
            self.move()
            self.lscore.setText(str(self.score))

    def newFood(self):
        self.food = [rand.randint(0,24),rand.randint(0,24)]
        self.gbox[self.food[0]][self.food[1]].changeColor(Qt.red)

    def move(self):

        if self.key_pressed == Qt.Key_Up:
            self.cur_x = self.cur_x-1
        elif self.key_pressed == Qt.Key_Down:
            self.cur_x = self.cur_x+1
        elif self.key_pressed == Qt.Key_Left:
            self.cur_y = self.cur_y-1
        elif self.key_pressed == Qt.Key_Right:
            self.cur_y = self.cur_y+1

        eat = False
        
        if([self.cur_x,self.cur_y] in self.snake.body):
            self.timer.stop()
            msg = QMessageBox()
            msg.setText("You Lose")
            msg.exec_()
            app.quit()

        
        self.snake.move([self.cur_x,self.cur_y])
        
        if(self.cur_x == -1 or self.cur_y == -1 or self.cur_x == 25 or self.cur_y ==25):
            self.timer.stop()
            msg = QMessageBox()
            msg.setText("You Lose")
            msg.exec_()
            app.quit()
        else:
            self.gbox[self.cur_x][self.cur_y].changeColor(QColor(0,150,69,127))


        if([self.cur_x,self.cur_y] == self.food):
            eat = True
            self.score = self.score+1
            self.newFood()

        tail = self.snake.eat(eat)
        if(eat is False):
            self.gbox[tail[0]][tail[1]].changeColor(QColor(15,15,15,25))
    


app = QApplication(sys.argv)
griglia = Grid()
sys.exit(app.exec_())