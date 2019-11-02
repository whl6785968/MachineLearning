class Queue:
    def __init__(self):
        self.first = None
        self.last = None
        self.N = 0

    def enqueue(self,item):
        oldLast = self.last
        self.last = Node(item)
        self.last.next = None
        if self.isEmpty():
            self.first = self.last
        else:
            oldLast.next = self.last

        self.N += 1

    def unqueue(self):
        if self.isEmpty():
            raise QueueIsEmptyException('队列已经没有元素')
        item = self.first
        self.first = self.first.next
        if self.isEmpty():
            self.last = None

        self.N -= 1
        return item

    def isEmpty(self):
        if self.N == 0:
            return True


class Node:
    def __init__(self,item):
        self.item = item
        self.next = None

class QueueIsEmptyException(Exception):
    def __init__(self,errInfo):
        super.__init__(self)
        self.errorinfo = errInfo
    def __str__(self):
        return self.errorinfo

if __name__ == '__main__':
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    # print(queue)
    print(queue.N)
    item = queue.unqueue()
    print(item.item)
    print(queue.N)
    queue.unqueue()
    queue.unqueue()
