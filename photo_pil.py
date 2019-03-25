#encoding:utf-8

import sys
from PIL import Image
import matplotlib.pyplot as plt

class TailRecurseException(Exception):
    def __init__(self, args, kwargs):
        super().__init__(self)
        self.args = args
        self.kwargs = kwargs

def tail_call_optimized(g):
    """
    This function decorates a function with tail call
    optimization. It does this by throwing an exception
    if it is it's own grandparent, and catching such
    exceptions to fake the tail call optimization.

    This function fails if the decorated
    function recurses in a non-tail context.
    """
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs
    func.__doc__ = g.__doc__
    return func

class PhotoData(object):
    im_path = r'D:\pythonVscode\test.bmp'
    out_path = r'D:\pythonVscode\test_out.bmp'
    check_rgb = 255
    dir = [[-1, 0], [0, -1], [1, 0], [ 0, 1]]

    class DataItem(object):
        def __init__(self):
            self.pixData = [0,0,0]
            self.check = 0 # 1 :白色区域
    
    class PosDataItem(object):
        def __init__(self, dataItem, pos):
            self.dataItem = dataItem
            self.posData = pos

    def __init__(self):
        self.src_img = Image.open(PhotoData.im_path)
        self.out_img = Image.new('RGB', self.src_img.size, (255, 255, 255))
        self.w = self.src_img.size[0]
        self.h = self.src_img.size[1]
        self.src_data = [([0] * self.h) for i in range(self.w)]
        for i in range(0, self.w):
            for j in range(0, self.h):
                data = self.DataItem()
                data.pixData = self.src_img.getpixel((i,j))
                data.check = 0
                self.src_data[i][j] = data
        self.data_list = list() # 矩阵存储
        self.src_list = list() # list存储

    def IsValid(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= self.w or y >= self.h:
            return False
        return True

    def getBorderRect(self, curve):
        ret = [0,self.w,0,self.h] # min_x,max_x,min_y,max_y
        for x in range(self.w):
            for y in range(self.h):
                if curve[x][y] != None:
                    if x < ret[0]:
                        ret[0] = x
                    if x > ret[1]:
                        ret[1] = x
                    if y < ret[2]:
                        ret[2] = y
                    if y > ret[3]:
                        ret[3] = y
        return ret

    def doImage(self):
        for index in range(len(self.data_list)):
            curve = self.data_list[index]
            curve_list = self.src_list[index]
            rec = self.getBorderRect(curve)
            for x in range(rec[0], rec[1]):
                for y in range(rec[2], rec[3]):
                    '''
                    交点为0:出现一个交点为零，在曲线外；
                    交点为单数：多数交点为单数，在曲线内；多数交点为双数，在曲线外
                    '''
                    intersect0 = [0]
                    intersectSing = [0]
                    intersectDual = [0]
                    for borderPos in range(rec[0], rec[1]):
                        self.checkLinePos(curve_list, [x,y], [borderPos, 0], intersect0, intersectSing, intersectDual)
                        self.checkLinePos(curve_list, [x,y], [borderPos, rec[3]-1], intersect0, intersectSing, intersectSing)
                    for borderPos in range(rec[2], rec[3]):
                        self.checkLinePos(curve_list, [x,y], [rec[1]-1, borderPos], intersect0, intersectSing, intersectDual)
                        self.checkLinePos(curve_list, [x,y], [0, borderPos], intersect0, intersectSing, intersectDual)
                    if intersect0[0] == 0 and intersectSing[0] == 0 and intersectDual[0] == 0:
                        continue
                    elif intersect0[0] > 10:# 超过十个点没有误差
                        continue
                    elif intersectSing[0] > intersectDual[0]:
                        continue
                    else:
                        self.out_img.putpixel((x,y), curve[x][y].pixData)
        self.out_img.save(self.out_path)
        plt.figure(self.out_path)
        plt.imshow(self.out_img)
        plt.show()

    def isAdjacent(self, posl, posr):
        if abs(posl[0]-posr[0]) <= 1 and abs(posl[1]-posr[1]) <= 1:
            return True
        return False

    # (y - y1) / (y2 - y1) = (x - x1) / (x2 - x1)
    # y = kx + b
    def getLineAllPos(self, posl, posr):
        ret = list()
        if (posl[0] == posr[0] and posl[1] == posr[1]):
            return ret
        elif posl[0] == posr[0]:
            for y in range(posl[1], posr[1]+1):
                ret.append((posl[0],y))
        else:
            for x in range(posl[0], posr[0]+1):
                if posl[1] == posr[1]:
                    ret.append((x,posl[1]))
                else:
                    y = (x - posl[0]) / (posr[0] - posl[0]) * (posr[1] - posl[1]) + posl[1]
                    ret.append((x,y))
        return ret

    def checkOnLine(self, curve_list, pos):
        for index in range(len(curve_list)):
            if pos[0] == curve_list[index].posData[0] and pos[1] == curve_list[index].posData[1]:
                return True
        return False

    # 根据交点的个数判断和曲线关系，相邻交点只算一个
    def checkLinePos(self, curve_list, posl, posr, intersect0, intersectSing, intersectDual):
        if (posl[0] == posr[0] and posl[1] == posr[1]):
            return
        ret = self.getLineAllPos(posl, posr)
        intersect = list()
        last_pos = None
        for index in range(len(ret)):
            if True == self.checkOnLine(curve_list, ret[index]):
                last_pos = ret[index]
                if False == self.isAdjacent(last_pos, ret[index]):
                    intersect.append(ret[index])
        if len(intersect) == 0:
            intersect0[0] += 1
        elif len % 2 != 0:
            intersectSing[0] += 1
        else:
            intersectDual[0] += 1
        return

    #@tail_call_optimized
    def getCurve(self, x, y, curve, curve_list):
        if False == self.IsValid(x, y):
            return False
        elif self.src_data[x][y].check == 1:
            return False
        self.src_data[x][y].check = 1
        if False == self.checkRGB(self.src_data[x][y].pixData):
            return False
        else:
            for index in range(0, len(self.dir)):
                next_x = x + self.dir[index][0]
                next_y = y + self.dir[index][1]
                self.getCurve(next_x, next_y, curve, curve_list)
            #if curve is None:
            #    curve = [([0] * self.h) for i in range(self.w)]
            #if curve_list is None:
            #    curve_list = list()
            curve[x][y] = self.src_data[x][y]
            curve_list.append(self.PosDataItem(self.src_data[x][y], [x,y]))
        return True

    def getCurveBegin(self):
        for i in range(0, self.w):
            for j in range(0, self.h):
                curve = [([0] * self.h) for i in range(self.w)]
                curve_list = list()
                if (True == self.getCurve(i, j, curve, curve_list)):
                    self.data_list.append(curve)
                    self.src_list.append(curve_list)

    def checkRGB(self, data):
        if (data[0] >= PhotoData.check_rgb and data[1] >= PhotoData.check_rgb and data[2] >= PhotoData.check_rgb):
            return True
        return False

def main():
    sys.setrecursionlimit(1000000) # modify the value of the recursion depth
#    try:
    photo = PhotoData()
    photo.getCurveBegin()
    photo.doImage()
#    except Exception as err:
#        print(err, err.)
#        pass

if __name__ == '__main__':
    main()
    