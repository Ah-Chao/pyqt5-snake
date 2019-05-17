#! python
# coding:utf-8
# Author:VChao
# Date:2019/05/14

import copy
import traceback

from snake import *


class Queue(object):
    def __init__(self):
        self.data_queue = list()

    def add(self, data):
        self.data_queue.append(data)

    def pop(self, index=0):
        return self.data_queue.pop(index)

    def __len__(self):
        return len(self.data_queue)


class Stack(Queue):
    def pop(self, index=-1):
        return self.data_queue.pop(index)


class PriorityQueue(Queue):

    def add(self, element):
        distance = element.distance_function()
        self.data_queue.append((distance,element))
        self.data_queue.sort(key=lambda x: x[0])

    # 想知道子类怎么调用父类的方法
    def pop(self, index=0):
        return self.data_queue.pop(index)[1]


class StateNode(object):
    """
            This is the class object for node using in search algorithms.
    """
    def __init__(self, state, parent, action):
        self.parent = parent
        self.state = state
        self.children = []
        self.action = action
        self.actions = state.get_actions()

    def __str__(self):
        return self.state.__str__()

    def add_child(self, children):
        self.children.append(children)

    def get_actions(self):
        return self.actions

    def state_normal(self):
        return self.state.is_normal()

    def state_success(self):
        return self.state.is_success()

    def state_change(self, action):
        return StateNode(
            self.state.state_change(action),
            self,
            action
        )

    def distance_function(self):
        return self.state.distance_function()

    def action_list(self):
        path_list = []
        tmp_node = self
        while tmp_node.parent is not None:
            path_list.insert(0, tmp_node.action)
            tmp_node = tmp_node.parent
        return path_list


def first_search(state,queue):
    tmp_state = copy.deepcopy(state)

    head_node = StateNode(tmp_state, None, 0)
    node_queue = queue()
    explored_cor = set()

    if head_node.state_success():
        return 0

    node_queue.add(head_node)
    explored_cor.add(str(head_node))

    while len(node_queue) > 0:
        tmp_node = node_queue.pop()

        for action in tmp_node.get_actions():
            new_state = tmp_node.state_change(action)
            tmp_node.add_child(new_state)

        for one_node in tmp_node.children:
            if not one_node.state_normal():
                continue
            if one_node.state_success():
                return one_node.action_list()

            if str(one_node) in explored_cor:
                continue
            else:
                explored_cor.add(str(one_node))
                node_queue.add(one_node)

    return None


def depth_first_search(state):
    return first_search(state, Stack)


def breadth_first_search(state):
    return first_search(state, Queue)


def greedy_first_search(state):
    return first_search(state, PriorityQueue)


def get_move_sequence(snake_state):
    try:
        sol = greedy_first_search(snake_state)
        return sol
    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    one = SnakeState([[4, 10], [4, 11]], 4, [[4, 5]], False)
