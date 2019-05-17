#! python
# coding:utf-8
# Author:VChao
# Date:2019/05/14

import copy
import traceback

from snake import *


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


def depth_first_search(state):

    tmp_state = copy.deepcopy(state)

    head_node = StateNode(tmp_state, None, 0)
    node_queue = list()
    explored_cor = set()

    if head_node.state_success():
        return 0

    node_queue.append(head_node)
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
                node_queue.append(one_node)

    return None


def breadth_first_search(state):
    tmp_state = copy.deepcopy(state)
    head_node = StateNode(tmp_state, None, 0)
    node_queue = list()
    explored_cor = set()

    if head_node.state_success():
        return 0

    node_queue.append(head_node)
    explored_cor.add(str(head_node))

    while len(node_queue) > 0:
        tmp_node = node_queue.pop(0)

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
                node_queue.append(one_node)

    return None


def greedy_first_search(state):
    tmp_state = copy.deepcopy(state)

    head_node = StateNode(tmp_state, None, 0)
    node_queue = list()
    explored_cor = set()

    if head_node.state_success():
        return 0

    node_queue.append(head_node)
    explored_cor.add(str(head_node))

    while len(node_queue) > 0:
        tmp_node = node_queue.pop(0)

        for action in tmp_node.get_actions():

            new_state = tmp_node.state_change(action)
            tmp_node.add_child(new_state)

        tmp_node_list = []
        for one_node in tmp_node.children:
            if not one_node.state_normal():
                continue
            if one_node.state_success():
                return one_node.action_list()

            # 我记得，这一块的代码，可能有些不对，书上的代码是考虑了一些函数值，
            # 虽然现在算是工作了，但实际上还是不太对，
            if str(one_node) in explored_cor:
                continue
            else:
                explored_cor.add(str(one_node))
                tmp_node_list.append(one_node)

        distance_node_list = []
        for one_node in tmp_node_list:
            distance_node_list.append(
                (one_node.distance_function(), one_node)
            )

        distance_node_list.sort(key=lambda x: x[0], reverse=True)
        for one_node in distance_node_list:
            node_queue.insert(0, one_node[1])

    return None


def get_move_sequence(snake_state):
    try:
        sol = breadth_first_search(snake_state)
        return sol
    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    one = SnakeState([[4, 10], [4, 11]], 4, [[4, 5]], False)
