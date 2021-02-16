import time
import threading
import sys
class Semaphore(object):
    def __init__(self, initial):
        self.lock = threading.Condition(threading.Lock())
        self.value = initial

    def up(self):
        with self.lock:
            self.value += 1
            self.lock.notify()

    def down(self):
        with self.lock:
            while self.value == 0:
                self.lock.wait()
            self.value -=1

class ChopStick(object):
    def __init__(self, number):
        self.number = number
        self.user = -1
        self.lock = threading.Condition(threading.Lock())
        self.taken = False

    def take(self, user):
        with self.lock:
            while self.taken == True:
                self.lock.wait()
            self.user = user
            self.taken = True
            sys.stdout.write("Trabajador [%s] toma la silla: %s\n" % (user, self.number))
            self.lock.notifyAll()

    def drop(self, user):
        with self.lock:
            while self.taken == False:
                self.lock.wait()
            self.user = -1
            self.taken = False
            sys.stdout.write("Trabajador [%s] deja la silla: %s\n" % (user, self.number))
            self.lock.notifyAll()

class Philosopher (threading.Thread):
    def __init__(self, number, left, right, butler):
        threading.Thread.__init__(self)
        self.number = number
        self.left = left
        self.right = right
        self.butler = butler

    def run(self):
        for i in range(1):
            self.butler.down()
            print("Trabajador ", self.number, "de pie")
            time.sleep(0.1)
            self.left.take(self.number)
            time.sleep(0.1)
            self.right.take(self.number)
            print("Trabajador ",self.number, "descansando")
            time.sleep(0.1)
            self.right.drop(self.number)
            self.left.drop(self.number)
            self.butler.up()
        sys.stdout.write("Trabajador [%s] termina de descansar" % self.number)

def main():
    n = 4
    butler = Semaphore(n-1)
    c = [ChopStick(i) for i in range(n)]
    p = [Philosopher(i, c[i], c[(i+1) % n], butler) for i in range(n)]
    for i in range(n):
        p[i].start()


if __name__=="__main__":
    main()
