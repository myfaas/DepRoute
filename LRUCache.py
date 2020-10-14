from collections import OrderedDict


class ContainerCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.length = 0
        self.cache = OrderedDict()

    # return：是否命中，删除了哪个
    def handleNone(self, func):
        # 插入一个元素
        if self.length < self.capacity:
            self.cache[func] = 1
            self.length += 1
            return False, None
        else:
            eldest = list(self.cache.keys())[0]
            self.cache.pop(eldest)
            self.cache[func] = 1
            return False, eldest

    def handleHit(self, func):
        self.cache.pop(func)
        self.cache[func] = 1
        return True, None

    def handleSubInter(self, func):
        eldest = list(self.cache.keys())[0]
        self.cache.pop(eldest)
        self.cache[func] = 1
        return True, eldest

    # def handleSub(self, subs, func):
    #     self.cache.pop(subs)
    #     self.cache[func] = 1
    #     return True, subs
