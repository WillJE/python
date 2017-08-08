import random
class Sprite(object):
    step = [-2, +2, -3, +3]
    def __init__(self, gm, point = None):
        self.gm = gm
        if point is None:
            self.point = random.randint(0, 20)
        else:
            self.point = point

    def jump(self):
        astep = random.choice(Sprite.step)#随机产生移动的大小
        if 0 <= self.point + astep <= 20:
            self.point += astep


class Ant(Sprite):
    def __init__(self, gm, point = None):
        self.gm = gm
        super(Ant, self).__init__(gm, point)
        self.gm.set_point('Ant', self.point)#显示初始化位置

    def jump(self):
        super(Ant, self).jump()
        self.gm.set_point('Ant', self.point)

class Worm(Sprite):
    def __init__(self, gm, point=None):
        self.gm = gm
        super(Worm, self).__init__(gm, point)
        self.gm.set_point('Worm', self.point)

    def jump(self):
        super(Worm, self).jump()
        self.gm.set_point('Worm', self.point)

class GameOver(object): #地图类，初始化两个参数
    def __init__(self):
        self.ant_point = None
        self.worm_point = None

    def catched(self):
        print("ant:{},worm:{}".format(self.ant_point, self.worm_point))
        if self.ant_point is not None and self.worm_point is not None and self.ant_point == self.worm_point:
            return True

    def set_point(self, tp, point):
        if tp == 'Ant':
            self.ant_point = point
        if tp == 'Worm':
            self.worm_point = point

if __name__ == '__main__':
    gm = GameOver()
    worm = Worm(gm)
    ant = Ant(gm)
    while not gm.catched():
        worm.jump()
        ant.jump()

