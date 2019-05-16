#! python
# coding:utf-8
# Author:VChao
# Date:2019/05/14

import copy
import math
X_nums = 24
Y_nums = 24

key_map = {
    'LEFT': 1,
    'RIGHT': 2,
    'DOWN': 3,
    'UP': 4
}
actions = [[1, 3, 4],
           [2, 3, 4],
           [1, 2, 3],
           [1, 2, 4]]


def naive_get_snake_move(head, food):
    ''''
    Using the only head and food
    See the result it can obtain.

    Parameters
    ----------
    head : array_like -> (x,y)
        snake's head cor

    food: array_like -> (x,y)

    '''

    if head[0] < food[0]:
        return key_map['RIGHT']
    elif head[0] > food[0]:
        return key_map['LEFT']

    if head[1] <= food[1]:
        return key_map['DOWN']
    else:
        return key_map['UP']


def snake_state_change(tmp_state, direction, grow):

    snake_state = copy.deepcopy(tmp_state)
    current_x_head = snake_state[0][0]
    current_y_head = snake_state[0][1]

    if direction == key_map['LEFT']:
        current_x_head, current_y_head = current_x_head - 1, current_y_head
        if current_x_head < 0:
            current_x_head = X_nums - 1

    if direction == key_map['RIGHT']:
        current_x_head, current_y_head = current_x_head + 1, current_y_head
        if current_x_head >= X_nums:
            current_x_head = 0

    if direction == key_map['DOWN']:
        current_x_head, current_y_head = current_x_head, current_y_head + 1
        if current_y_head >= Y_nums:
            current_y_head = 0

    if direction == key_map['UP']:
        current_x_head, current_y_head = current_x_head, current_y_head - 1
        if current_y_head < 0:
            current_y_head = Y_nums - 1

    head = [current_x_head, current_y_head]

    snake_state.insert(0, head)
    if not grow:
        snake_state.pop()
    return snake_state


class TreeNode(object):
    def __init__(self, snake_state, parent, action, direction):
        self.snake_state = copy.deepcopy(snake_state)
        self.parent = parent
        self.action = action
        self.direction = direction
        self.children = []

    def get_actions(self):
        return actions[self.direction - 1]

    def add_children(self, children):
        self.children.append(children)

    def node_safe(self):
        # Test if snake collides with itself, game is over
        for i in range(1, len(self.snake_state)):
            if self.snake_state[i] == self.snake_state[0]:
                return False
        return True

    # Test if snake eat the food
    def node_success(self, food):
        for pos in food:
            if pos == self.snake_state[0]:
                return True
        return False


def distance_function(snake_head, food):
    return math.sqrt(pow(snake_head[0] - food[0], 2) +
                     pow(snake_head[1] - food[1], 2))


def get_move_sequence(one_node):
    path_list = []
    tmp_node = one_node
    while tmp_node.parent is not None:
        path_list.insert(0, tmp_node.action)
        tmp_node = tmp_node.parent

    return path_list


def greedy_first_search(snake, direction, food, grow):

    head_node = TreeNode(snake, None, 0, direction)
    node_queue = list()
    explored_cor = set()

    if head_node.node_success(food):
       return direction

    node_queue.append(head_node)
    explored_cor.add(str(head_node.snake_state[0]))

    while len(node_queue) > 0:
        tmp_node = node_queue.pop(0)
        for action in tmp_node.get_actions():
            state = snake_state_change(tmp_node.snake_state, action, grow)
            tmp_node.add_children(TreeNode(state, tmp_node, action, action))

        grow = False
        tmp_node_list = []
        for one_node in tmp_node.children:
            if not one_node.node_safe():
                continue
            if one_node.node_success(food):
                return get_move_sequence(one_node)

            if str(one_node.snake_state[0]) in explored_cor:
                continue
            else:
                explored_cor.add(str(one_node.snake_state[0]))
                tmp_node_list.append(one_node)

        distance_node_list = []
        for one_node in tmp_node_list:
            distance_node_list.append(
                (distance_function(one_node.snake_state[0],food[0]),one_node)
            )

        distance_node_list.sort(key=lambda x: x[0], reverse=True)
        for one_node in distance_node_list:
            node_queue.insert(0,one_node[1])

    return None


def depth_first_search(snake, direction, food, grow):

    head_node = TreeNode(snake, None, 0, direction)
    if head_node.node_success(food):
        return direction

    node_queue = list()
    node_queue.append(head_node)

    explored_cor = set()
    explored_cor.add(str(head_node.snake_state[0]))

    while len(node_queue) > 0:

        tmp_node = node_queue.pop()
        for action in tmp_node.get_actions():
            state = snake_state_change(tmp_node.snake_state, action,grow)
            tmp_node.add_children(TreeNode(state, tmp_node, action, action))
        grow = False
        for one_node in tmp_node.children:
            if one_node.node_success(food):
                return get_move_sequence(one_node)
            if not one_node.node_safe():
                continue
            if str(one_node.snake_state[0]) in explored_cor:
                continue
            else:
                explored_cor.add(str(one_node.snake_state[0]))
                node_queue.append(one_node)
    return None


def breadth_first_search(snake, direction, food, grow):

    head_node = TreeNode(snake, None, 0, direction)

    if head_node.node_success(food):
        return direction

    node_queue = list()
    node_queue.append(head_node)

    explored_cor = set()
    explored_cor.add(str(head_node.snake_state[0]))

    while len(node_queue) > 0:

        tmp_node = node_queue.pop(0)
        for action in tmp_node.get_actions():
            state = snake_state_change(tmp_node.snake_state, action,grow)
            tmp_node.add_children(TreeNode(state, tmp_node, action, action))
        grow = False
        for one_node in tmp_node.children:
            if one_node.node_success(food):
                return get_move_sequence(one_node)
            if not one_node.node_safe():
                continue
            if str(one_node.snake_state[0]) in explored_cor:
                continue
            else:
                explored_cor.add(str(one_node.snake_state[0]))
                node_queue.append(one_node)
    return None

import traceback
def get_snake_move(snake, direction, food, grow):
    """
    :param snake: array_like [[x1,y1],[x2,y2]...]
                all the position a snake take

    :param direction: int

    :param food: array_like  (x,y)
                food cor

    :param grow: bool
                whether the snake will grow

    :return:
        move : int
            the direction you want to move
    """
    try:
        sol = breadth_first_search(snake, direction, food, grow)
        print("Solution:", sol)
        return sol
    except Exception as e:
        print(traceback.print_exc())

if __name__ == "__main__":
    pass