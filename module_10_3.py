import threading
from random import randint
from  time import sleep

class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for _ in range(100):
            amount = randint(50, 500)  # Случайная сумма пополнения
            with self.lock:  # Блокируем доступ к балансу
                self.balance += amount
                print(f"Пополнение: {amount}. Баланс: {self.balance}")
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
        # Имитация времени выполнения пополнения
            sleep(0.001)

    def take(self):
        for _ in range(100):
            amount = randint(50, 500)  # Случайная сумма снятия
            print(f"Запрос на {amount}")
            with self.lock:  # Блокируем доступ к балансу
                if amount <= self.balance:
                    self.balance -= amount
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                else:
                    print("Запрос отклонён, недостаточно средств")
                    self.lock.acquire()  # Блокируем поток, если недостаточно средств

            sleep(0.001)

bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()

th1.join()
th2.join()

print(f'Итоговый баланс:{bk.balance}')