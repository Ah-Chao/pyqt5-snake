#! python
#coding:utf-8
#Author:VChao
#Date:2019/05/14

import random
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


from search import *

class SnakeGame(QMainWindow):
    def __init__(self):
        super(SnakeGame, self).__init__()
        self.sboard = Board(self)

        self.statusbar = self.statusBar()
        self.sboard.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.setCentralWidget(self.sboard)
        self.setWindowTitle('PyQt5 Snake game')
        self.resize(320, 340)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

        self.sboard.start()
        self.show()


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)

    '''
    This speed is mean the timer's interval,
    so the value lower,the speed higher
    '''
    SPEED = 150

    WIDTHINBLOCKS = X_nums
    HEIGHTINBLOCKS = Y_nums

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.timer = QBasicTimer()
        self.running = False
        self.snake = [[5, 5], [5, 6]]
        self.current_x_head = self.snake[0][0]
        self.current_y_head = self.snake[0][1]
        self.key_map = {
                    'LEFT': 1,
                    'RIGHT': 2,
                    'DOWN': 3,
                    'UP': 4
                }
        self.food = []
        self.grow_snake = False
        self.board = []
        self.direction = 4
        self.drop_food()
        self.move_solution = []
        self.setFocusPolicy(Qt.StrongFocus)

    def square_width(self):
        return int(self.contentsRect().width() / Board.WIDTHINBLOCKS)

    def square_height(self):
        return int(self.contentsRect().height() / Board.HEIGHTINBLOCKS)

    def status_str(self):
        return str("score:%d,head_x:%d,head_y:%d,food_x:%d,food_y:%d , x :%d,y:%d" % (
                     len(self.snake) - 2,
                     self.current_x_head,
                     self.current_y_head,
                     self.food[0][0],
                     self.food[0][1],
                     self.snake[1][0],
                     self.snake[1][1]
                    ))

    def start(self):
        self.msg2statusbar.emit(self.status_str())
        self.timer.start(Board.SPEED, self)
        self.running = True

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height()
        '''
        #绘制网格线，有些密集
        for x in range(self.WIDTHINBLOCKS):
            painter.drawLine(x * self.square_width(),0,
                             x * self.square_width(),
                             (self.HEIGHTINBLOCKS + 1)*  self.square_height())

        for y in range(0,self.HEIGHTINBLOCKS + 1):
            painter.drawLine(0,y * self.square_height(),
                             (self.WIDTHINBLOCKS + 1) * self.square_width(),
                             y * self.square_height())
        '''
        for pos in self.snake:
            color = 0xCC66CC
            self.draw_square(painter, color,rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())

        for pos in self.food:
            color = 0x000000
            self.draw_square(painter, color,rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())

    def draw_square(self, painter, color, x, y):
        color = QColor(color)
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            if self.direction != self.key_map['RIGHT']:
                self.direction = self.key_map['LEFT']
        elif key == Qt.Key_Right:
            if self.direction != self.key_map['LEFT']:
                self.direction = self.key_map['RIGHT']
        elif key == Qt.Key_Down:
            if self.direction != self.key_map['UP']:
                self.direction = self.key_map['DOWN']
        elif key == Qt.Key_Up:
            if self.direction != self.key_map['DOWN']:
                self.direction = self.key_map['UP']

        elif key == Qt.Key_Space:

            if self.running == True:
                self.running = False
                self.timer.stop()
            else:
                self.running = True
                self.timer.start(Board.SPEED, self)


    def move_snake(self):
        if self.direction == self.key_map['LEFT']:
            self.current_x_head, self.current_y_head = self.current_x_head - 1, self.current_y_head
            if self.current_x_head < 0:
                self.current_x_head = Board.WIDTHINBLOCKS - 1

        if self.direction == self.key_map['RIGHT']:
            self.current_x_head, self.current_y_head = self.current_x_head + 1, self.current_y_head
            if self.current_x_head >= Board.WIDTHINBLOCKS:
                self.current_x_head = 0

        if self.direction == self.key_map['DOWN']:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head + 1
            #这里跟其地方不太一样，是因为Y轴最下面那一块，有时候会被状态栏挡住
            if self.current_y_head >= Board.HEIGHTINBLOCKS:
                self.current_y_head = 0

        if self.direction == self.key_map['UP']:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head - 1
            if self.current_y_head < 0:
                self.current_y_head = Board.HEIGHTINBLOCKS - 1

        head = [self.current_x_head, self.current_y_head]
        self.snake.insert(0, head)
        self.msg2statusbar.emit(self.status_str())
        if not self.grow_snake:
            self.snake.pop()
        else:
            self.grow_snake = False

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():

            food = self.food
            try:
                if len(self.move_solution) == 0:
                    self.move_solution = get_snake_move(self.snake, self.direction, food)
                    self.direction = self.move_solution.pop(0)
                else:
                    self.direction = self.move_solution.pop(0)
            except Exception as e:
                print(e)

            self.move_snake()
            self.is_food_collision()
            self.is_suicide()
            self.update()

    def is_suicide(self):  # If snake collides with itself, game is over
        for i in range(1, len(self.snake)):
            if self.snake[i] == self.snake[0]:
                self.msg2statusbar.emit(str("TRUP"))
                self.snake = [[x, y] for x in range(0, 61) for y in range(0, 41)]
                self.food = []
                self.timer.stop()
                self.update()

    def is_food_collision(self):
        for pos in self.food:
            if pos == self.snake[0]:
                self.food.remove(pos)
                self.drop_food()
                self.grow_snake = True

    def drop_food(self):

        x = random.randint(0, self.WIDTHINBLOCKS - 1)
        y = random.randint(0, self.HEIGHTINBLOCKS - 1)
        for pos in self.snake:  # Do not drop food on snake
            if pos == [x, y]:
                self.drop_food()
                return
        self.food.append([x, y])

def main():
    app = QApplication([])
    launch_game = SnakeGame()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()