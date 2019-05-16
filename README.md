
PyQt5 Snake Games

forked from https://github.com/borisuvarov/pyqt5-snake
- - -

This Game will test some algorithms.
利用贪吃蛇游戏实现一些搜索算法，自动运行
当前测试三种算法：
    深度优先搜索算法
    广度优先搜索算法
    启发式贪婪算法（大概能用这个名字，但算法实现上跟书上有些出入）
    
当前看来深度优先能达到最好的效果，因为贪吃蛇是没有墙的，他会一直往下
但速度上，或者感觉上最快的，还是启发式算法，利用蛇头和食物的距离来做启发函数
广度优先可以理解为式最直观的，每次都是直线过去，但还是说不好

下面这个图片是启发式算法运作的过程

![Snake](https://github.com/Ah-Chao/pyqt5-snake/blob/master/snake.gif)
- - -
This is my first attempt to use github.