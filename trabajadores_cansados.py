import time
import threading
import sys

class Semaforo(object):
    def __init__(self, inicial):
        self.lock = threading.Condition(threading.Lock())
        self.valor = inicial

    def up(self):
        with self.lock:
            self.valor += 1
            self.lock.notify()

    def down(self):
        with self.lock:
            while self.valor == 0:
                self.lock.wait()
            self.valor -=1

class Sillas(object):
    def __init__(self, id):
        self.id = id
        self.lock = threading.Condition(threading.Lock())
        self.tomado = False

    def tomar(self, persona):
        with self.lock:
            while self.tomado == True:
                self.lock.wait()
            self.persona = persona
            self.tomado = True
            sys.stdout.write("Trabajador [%s] toma la silla: %s\n" % (persona, self.id))
            self.lock.notifyAll()

    def dejar(self, persona):
        with self.lock:
            while self.tomado == False:
                self.lock.wait()
            self.tomado = False
            sys.stdout.write("Trabajador [%s] deja la silla: %s\n" % (persona, self.id))
            self.lock.notifyAll()

class Trabajador (threading.Thread):
    def __init__(self, id, silla, silla_ady, butler):
        threading.Thread.__init__(self)
        self.id = id
        self.silla = silla
        self.silla_ady = silla_ady
        self.butler = butler

    def run(self):
        for i in range(1):
            self.butler.down()
            print("Trabajador ", self.id, "de pie")
            time.sleep(0.1)
            self.silla.tomar(self.id)
            time.sleep(0.1)
            self.silla_ady.tomar(self.id)
            print("Trabajador ", self.id, "descansando")
            time.sleep(0.1)
            self.silla_ady.dejar(self.id)
            self.silla.dejar(self.id)
            self.butler.up()
        sys.stdout.write("Trabajador [%s] termina de descansar" % self.id)

def main():
    n = 5
    butler = Semaforo(n-1)
    s = [Sillas(i) for i in range(n)]
    t = [Trabajador(i, s[i], s[(i+1) % n], butler) for i in range(n)]
    for i in range(n):
        t[i].start()


if __name__=="__main__":
    main()
