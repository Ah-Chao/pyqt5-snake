#! python
# coding:utf-8
# Author:VChao
# Date: 2019/05/16

import random
import copy
import math
import traceback

X_nums = 12
Y_nums = 12

key_map = {
    'LEFT': 1,
    'RIGHT': 2,
    'DOWN': 3,
    'UP': 4
}

actions = [
    [1, 3, 4],
    [2, 3, 4],
    [1, 2, 3],
    [1, 2, 4]
]


class SnakeState(object):
    def __init__(self, snake=[], direction=0, food=[], grow=False):
        self.snake = copy.deepcopy(snake)
        self.food = copy.deepcopy(food)
        self.direction = direction
        self.grow = grow
        self.pong = [-1,-1]

    def init_by_game(self):
        # direction = random.randint(1,4)
        x = random.randint(0, X_nums - 1)
        y = random.randint(0, Y_nums - 1)

        self.snake = [[x, y], [x, 11]]
        self.direction = 1
        self.drop_food()

    def status_str(self):
        return str("score:%d,head_x:%d,head_y:%d,food_x:%d,food_y:%d" % (
                len(self.snake) - 2,
                self.snake[0][0],
                self.snake[0][1],
                self.food[0][0],
                self.food[0][1]
                )
        )

    def __str__(self):
        return str(self.snake[0])

    def get_state_by_game(self):
        return self.snake, self.food, self.pong

    def get_actions(self):
        return actions[self.direction - 1]

    @staticmethod
    def head_change(current_x_head, current_y_head, action):

        if action == key_map['LEFT']:
            current_x_head, current_y_head = current_x_head - 1, current_y_head
            if current_x_head < 0:
                current_x_head = X_nums - 1

        if action == key_map['RIGHT']:
            current_x_head, current_y_head = current_x_head + 1, current_y_head
            if current_x_head >= X_nums:
                current_x_head = 0

        if action == key_map['DOWN']:
            current_x_head, current_y_head = current_x_head, current_y_head + 1
            if current_y_head >= Y_nums:
                current_y_head = 0

        if action == key_map['UP']:
            current_x_head, current_y_head = current_x_head, current_y_head - 1
            if current_y_head < 0:
                current_y_head = Y_nums - 1

        head = [current_x_head, current_y_head]
        return head

    def drop_food(self):
        x = random.randint(0, X_nums - 1)
        y = random.randint(0, Y_nums - 1)
        # Do not drop food on snake
        for pos in self.snake:
            if pos == [x, y]:
                self.drop_food()
                return
        self.food.append([x, y])

    def is_success(self):
        for pos in self.food:
            if pos == self.snake[0]:
                return True
        return False

    def is_success_for_game(self):
        if self.is_success():
            self.food.pop()
            self.drop_food()
            self.grow = True

    def next_state_for_game(self, action):

        head = self.head_change(self.snake[0][0], self.snake[0][1], action)
        self.snake.insert(0, head)
        if not self.grow:
            self.snake.pop()
        else:
            self.grow = False

    def state_change(self, action):

        snake = copy.deepcopy(self.snake)
        food = copy.deepcopy(self.food)

        head = self.head_change(snake[0][0], snake[0][1], action)

        snake.insert(0, head)
        if not self.grow:
            snake.pop()

        return SnakeState(snake, action, food)

    def is_normal(self):
        for i in range(1, len(self.snake)):
            if self.snake[i] == self.snake[0]:
                self.pong = self.snake[i]
                return False
        return True

    def distance_function(self):
        return math.sqrt(
            (self.snake[0][0] - self.food[0][0]) ** 2 +
            (self.snake[0][1] - self.food[0][1]) ** 2
        )
