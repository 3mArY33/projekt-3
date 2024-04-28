import time
import random
from threading import Thread, Lock

class Filizofowie:
    def __init__(self, liczba_filozofow = 5, roz_posilki = 7):
        self.posilki = [roz_posilki for _ in range(liczba_filozofow)]
        self.widelce = [Lock() for _ in range(liczba_filozofow)]
        self.status = ['  M  ' for _ in range(liczba_filozofow)]
        self.trzymanie = ['    ' for _ in range(liczba_filozofow)]

    def filozof(self, i):
        j = (i + 1) % 5
        while self.posilki[i] > 0:
            self.status[i] = '  M  '
            time.sleep(random.random())
            self.status[i] = '  C  '
            if not self.widelce[i].locked():
                self.widelce[i].acquire()
                self.trzymanie[i] = '/    '
                time.sleep(random.random())
                if not self.widelce[j].locked():
                    self.widelce[j].acquire()
                    self.trzymanie[i] = '/   \\'
                    self.status[i] = '  J  '
                    time.sleep(random.random())
                    self.posilki[i] -= 1
                    self.widelce[j].release()
                    self.trzymanie[i] = '/    '
                    self.widelce[i].release()
                    self.trzymanie[i] = '     '
                    self.status[i] = '  M  '
                else:
                    self.widelce[i].release()
                    self.trzymanie[i] = '     '

def main():
    n = 5
    m = 4
    dining_philosophers = Filizofowie(n, m)
    philosophers = [Thread(target = dining_philosophers.filozof, args = (i, )) for i in range(n)]
    for filozof in philosophers:
        filozof.start()
    while sum(dining_philosophers.posilki) > 0:
        print("-" * (n * 5))
        print("".join(map(str, dining_philosophers.status)), " : ", str(dining_philosophers.status.count('  J  ')), " <--  Ilość aktualnie jedzących filozofów")
        print("".join(map(str, dining_philosophers.trzymanie)))
        print("".join("{:3d}  ".format(m) for m in dining_philosophers.posilki), " <--", str("Ilość posiłków"))
        print('  F1   F2   F3   F4   F5')
        time.sleep(1)
    for filozof in philosophers:
        filozof.join()

if __name__ == "__main__":
    main()



