#! python
# coding:utf-8
# Author:VChao
# Date:2019/05/14

import sys
import random
# 为啥这个会显示没用呢，难道是因为我在另一个文件中导入了？？？
import traceback

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from search import *
from snake import *


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
    SPEED = 60
    # The nums of blocks
    WIDTH_BLOCKS = X_nums
    HEIGHT_BLOCKS = Y_nums

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.timer = QBasicTimer()
        self.running = False

        self.state = SnakeState()
        self.state.init_by_game()
        self.next_action = 0

        self.last_state = copy.deepcopy(self.state)
        self.move_solution = []

        # 如果不设置这个选项，无法获取键盘击键时间
        self.setFocusPolicy(Qt.StrongFocus)

    # 尝试着删除过这里两个函数，但最后就是一个非常小的画了
    # 我感觉应该是他底层的gui的机制
    # 即使在上层类调用start后，他的实际数值仍然不是大的（已测试）
    def square_width(self):
        return int(self.contentsRect().width() / Board.WIDTH_BLOCKS)

    def square_height(self):
        return int(self.contentsRect().height() / Board.HEIGHT_BLOCKS)

    def start(self):
        self.msg2statusbar.emit(self.state.status_str())
        self.timer.start(Board.SPEED, self)
        self.running = True

    def board_info(self):
        rect = self.contentsRect()
        width = self.square_width()
        height = self.square_height()
        board_top = rect.bottom() - Board.HEIGHT_BLOCKS * height
        return rect, width, height, board_top

    def paintEvent(self, event):
        painter = QPainter(self)
        rect, width, height, board_top = self.board_info()
        snake, food, pong = self.state.get_state_by_game()

        draw_variable = [
            [0x00CD66, [snake[0]]],
            [0xCC66CC, snake[1:]],
            [0x000000, food],
            [0xB22222, [pong]]
        ]

        for one_var in draw_variable:
            color = one_var[0]
            for pos in one_var[1]:
                self.draw_square(
                    painter, color,
                    width, height,
                    rect.left() + pos[0] * width,
                    board_top + pos[1] * height
                )

    @staticmethod
    def draw_square(painter, color, width, height, x, y):
        color = QColor(color)
        painter.fillRect(
            x + 1,
            y + 1,
            width - 2,
            height - 2,
            color
        )

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            if self.state.direction != key_map['RIGHT']:
                self.state.direction = key_map['LEFT']
        elif key == Qt.Key_Right:
            if self.state.direction != key_map['LEFT']:
                self.state.direction = key_map['RIGHT']
        elif key == Qt.Key_Down:
            if self.state.direction != key_map['UP']:
                self.state.direction = key_map['DOWN']
        elif key == Qt.Key_Up:
            if self.state.direction != key_map['DOWN']:
                self.state.direction = key_map['UP']

        elif key == Qt.Key_Space:
            if self.running:
                self.running = False
                self.timer.stop()
            else:
                self.running = True
                self.timer.start(Board.SPEED, self)

        elif key == Qt.Key_Q:
            self.state = copy.deepcopy(self.last_state)
            self.move_solution = []
            self.update()
            self.running = True
            self.timer.start(Board.SPEED, self)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            try:
                if len(self.move_solution) == 0:
                    self.last_state = copy.deepcopy(self.state)
                    self.move_solution = get_move_sequence(self.state)
                self.next_action = self.move_solution.pop(0)

            except Exception as e:
                traceback.print_exc()

            self.state.next_state_for_game(self.next_action)
            self.msg2statusbar.emit(self.state.status_str())
            if not self.state.is_normal():
                self.running = False
                self.timer.stop()

            self.state.is_success_for_game()
            self.update()


def main():
    app = QApplication([])
    launch_game = SnakeGame()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
