import time
import threading
import sys

class Semaforo(object):
    def __init__(self, inicial):
        self.lock = threading.Condition(threading.Lock())  # Variable de condición
        self.valor = inicial  # Valor inicial va a ser n-1 (en este caso 4) para que no se produzca el interbloqueo.

    def up(self):
        with self.lock:
            self.valor += 1  # Aumenta el valor en 1.
            self.lock.notify()  # Despierta el hilo de down.

    def down(self):
        with self.lock:
            while self.valor == 0:  # Evita que la cuenta disminuya a -1 para que no se produzca el interbloqueo.
                self.lock.wait()  # Bloquea el hilo hasta que up lo despierte.
            self.valor -=1  # Disminuye el valor en 1.

class Sillas(object):
    def __init__(self, id):
        self.id = id
        self.lock = threading.Condition(threading.Lock())
        self.tomado = False  # Variable booleana para verificar si la silla está tomada.

    def tomar(self, persona):
        with self.lock:
            while self.tomado == True:
                self.lock.wait()  # Mientras esté tomada bloquea el hilo hasta que lo llamen.
            self.persona = persona
            self.tomado = True  # Si no está tomada, toma la silla.
            sys.stdout.write("Trabajador [%s] toma la silla: %s\n" % (persona, self.id))
            self.lock.notifyAll()  # Despierta todos los hilos que esperan en esta condición.

    def dejar(self, persona):
        with self.lock:
            while self.tomado == False:  # Mientras no esté tomada bloquea el hilo hasta que lo llamen.
                self.lock.wait()
            self.tomado = False  # Si está tomada, deja la silla.
            sys.stdout.write("Trabajador [%s] deja la silla: %s\n" % (persona, self.id))
            self.lock.notifyAll()  # Despierta todos los hilos que esperan en esta condición.

class Trabajador (threading.Thread):
    def __init__(self, id, silla, silla_ady, control):
        threading.Thread.__init__(self)
        self.id = id
        self.silla = silla
        self.silla_ady = silla_ady
        self.control = control

    def run(self):
        for i in range(1):  # Está en rango (1) porque en el main se inicia dentro de un for.
            self.control.down()  # Llama el método down (representa a los trabajadores que están de pie).
            print("Trabajador ", self.id, "de pie")  # Presenta el mensaje que están de pie.
            time.sleep(0.1)
            self.silla.tomar(self.id)  # Llama a la función tomar.
            time.sleep(0.1)
            self.silla_ady.tomar(self.id)  # Toma la silla adyacente en caso de que no esté bloqueada.
            print("Trabajador ", self.id, "descansando")  # Si tiene las 2 sillas, presenta este mensaje.
            time.sleep(0.1)
            self.silla_ady.dejar(self.id)  # Deja la silla adyacente.
            self.silla.dejar(self.id)  # Deja su suya.
            self.control.up()  # Llama al método up (representa a los trabajadores que ya terminaron de descansar).
        sys.stdout.write("Trabajador [%s] termina de descansar" % self.id)  # Presenta el mensaje que terminaron de descansar.

def main():
    n = 5  # Número de trabajadores en base al problema.
    control = Semaforo(n-1)  # Si fuera (n) se produce el interbloqueo porque cada trabajador tomaría 1 silla.
    s = [Sillas(i) for i in range(n)]  # Lista de sillas.
    t = [Trabajador(i, s[i], s[(i+1) % n], control) for i in range(n)]  # Lista de trabajadores.
    for i in range(n):
        t[i].start()  #Inicio los procesos definidos en el run.


if __name__=="__main__":
    main()
