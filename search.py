#! python
#coding:utf-8
#Author:VChao
#Date:2019/05/14


key_map = {
    'LEFT': 1,
    'RIGHT': 2,
    'DOWN': 3,
    'UP': 4
}

'''
This is the alghrithm used for move snake
'''

'''
测试结果，该函数只会进行坐标的比较，然后就进行动作的发生了， 
丝毫不考虑这个东西会不会导致游戏的结束，所以下一步应该考虑，
如何保证这个游戏不会发生这种情况
'''
def naive_get_snake_move(head,food):
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


# Test if snake collides with itself, game is over
def is_suicide(snake):
    for i in range(1, len(snake)):
        if snake[i] == snake[0]:
            return True
    else:
        return False

'''
开始的时候，我是想利用游戏的知识，我要去考虑很多细节，
但这种算法，就是我最开始想的，我根据他们之间的位置，
然后考虑不碰撞的情况，来弄相应的数据
更像是我那种决定性编程的思路
- - -
我需要对这个部分进行建模，
利用图形的搜索算法，保证后续的最短路径
同时不会导致游戏的结束
- - -
那么我这个搜索空间应该怎么定义，这个是个问题
不仅仅是我的头在动，同时蛇的身体也在动，所以说这个空间的定义感觉是个动态的
'''

def get_snake_move(snake,food):

    """
    :param snake: array_like [(x1,y1),(x2,y2)...]
                all the position a snake take
    :param food: array_like  (x,y)
                food cor

    :return:
        move : int
            the direction you want to move
    """

    return 1