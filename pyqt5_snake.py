#! python
#coding:utf-8
#Author:VChao
#Date:2019/05/14

import random
import sys
# 为啥这个会显示没用呢，难道是因为我在另一个文件中导入了？？？
import traceback

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from search import *


class SnakeGame(QMainWindow):
    def __init__(self):
        super(SnakeGame, self).__init__()

        self.board = Board(self)
        self.statusbar = self.statusBar()
        self.board.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.setCentralWidget(self.board)
        self.setWindowTitle('PyQt5 Snake game')

        self.resize(320, 340)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

        self.board.start()
        self.show()


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)

    '''
    This speed is mean the timer's interval,
    so the value lower,the speed higher
    '''
    SPEED = 20
    # The nums of blocks
    WIDTH_BLOCKS = X_nums
    HEIGHT_BLOCKS = Y_nums

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.timer = QBasicTimer()
        self.running = False

        self.snake, self.food, self.direction = [[5, 5], [5, 6]], [], 4
        self.last_state = {}
        self.drop_food()

        self.move_solution = []
        self.pong = None
        self.grow_snake = False

        self.setFocusPolicy(Qt.StrongFocus)

    # 尝试着删除过这里两个函数，但最后就是一个非常小的画了，感觉应该是这个东西在实质开始之后就不变了
    # 我感觉应该是他底层的gui的机制
    def square_width(self):
        return int(self.contentsRect().width() / Board.WIDTH_BLOCKS)

    def square_height(self):
        return int(self.contentsRect().height() / Board.HEIGHT_BLOCKS)

    def status_str(self):
        return str(
            "score:%d,head_x:%d,head_y:%d,food_x:%d,food_y:%d" % (
                len(self.snake) - 2,
                self.snake[0][0],
                self.snake[0][1],
                self.food[0][0],
                self.food[0][1]
            )
        )

    def start(self):
        self.msg2statusbar.emit(self.status_str())
        self.timer.start(Board.SPEED, self)
        self.running = True

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        width = self.square_width()
        height = self.square_height()
        board_top = rect.bottom() - Board.HEIGHT_BLOCKS * height

        pos = self.snake[0]
        color = 0x00CD66
        self.draw_square(
                painter, color,
                rect.left() + pos[0] * width,
                board_top + pos[1] * height
            )

        for pos in self.snake[1:]:
            color = 0xCC66CC
            self.draw_square(
                painter, color,
                rect.left() + pos[0] * width,
                board_top + pos[1] * height
            )

        for pos in self.food:
            color = 0x000000
            self.draw_square(
                painter, color,
                rect.left() + pos[0] * width,
                board_top + pos[1] * height
            )

        if self.pong is not None:
            self.draw_myself(self.pong[0], self.pong[1])

    def draw_myself(self,x,y):
        painter = QPainter(self)
        rect = self.contentsRect()
        board_top = rect.bottom() - Board.HEIGHT_BLOCKS * self.square_height()

        color = 0xB22222
        self.draw_square(painter, color, rect.left() + x * self.square_width(),
                         board_top + y * self.square_height())

    def draw_square(self, painter, color, x, y):
        color = QColor(color)
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            if self.direction != key_map['RIGHT']:
                self.direction = key_map['LEFT']
        elif key == Qt.Key_Right:
            if self.direction != key_map['LEFT']:
                self.direction = key_map['RIGHT']
        elif key == Qt.Key_Down:
            if self.direction != key_map['UP']:
                self.direction = key_map['DOWN']
        elif key == Qt.Key_Up:
            if self.direction != key_map['DOWN']:
                self.direction = key_map['UP']

        elif key == Qt.Key_Space:

            if self.running:
                self.running = False
                self.timer.stop()
            else:
                self.running = True
                self.timer.start(Board.SPEED, self)
        elif key == Qt.Key_Q:

            if len(self.last_state) != 0:
                self.snake = copy.deepcopy(self.last_state['snake_state'])
                self.food = copy.deepcopy(self.last_state['food'])
                self.direction = self.last_state['direction']
                self.grow_snake = self.last_state['grow']
                self.move_solution = []
                self.last_state = {}
                self.pong = None

                self.update()
                self.running = True
                self.timer.start(Board.SPEED, self)

    def move_snake(self):

        self.snake = snake_state_change(self.snake,self.direction,self.grow_snake)
        if self.grow_snake:
            self.grow_snake = False
        self.msg2statusbar.emit(self.status_str())

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            try:
                if len(self.move_solution) == 0:
                    self.last_state = {
                        "snake_state": copy.deepcopy(self.snake),
                        "food":        copy.deepcopy(self.food),
                        "direction":   self.direction,
                        "grow":        self.grow_snake
                    }
                    self.move_solution = get_snake_move(
                        self.snake,
                        self.direction,
                        self.food,
                        self.grow_snake
                    )
                    self.direction = self.move_solution.pop(0)
                else:
                    self.direction = self.move_solution.pop(0)

            except Exception as e:
                print(traceback.print_exc())

            self.move_snake()
            self.is_suicide()
            self.is_food_collision()
            self.update()

    # If snake collides with itself, game is over
    def is_suicide(self):
        for i in range(1, len(self.snake)):
            if self.snake[i] == self.snake[0]:
                self.msg2statusbar.emit(self.status_str())
                self.running = False
                self.timer.stop()
                self.pong = self.snake[i]
                return i
        return 0

    def drop_food(self):
        x = random.randint(0, Board.WIDTH_BLOCKS - 1)
        y = random.randint(0, Board.HEIGHT_BLOCKS - 1)
        # Do not drop food on snake
        for pos in self.snake:
            if pos == [x, y]:
                self.drop_food()
                return
        self.food.append([x, y])

    def is_food_collision(self):
        for pos in self.food:
            if pos == self.snake[0]:
                self.food.remove(pos)
                self.drop_food()
                self.grow_snake = True


def main():
    app = QApplication([])
    launch_game = SnakeGame()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()