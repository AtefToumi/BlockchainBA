import random
import time
from threading import Thread

def generate_transactions():
    while True:
        print(random.randrange(1,20))
        time.sleep(1)


def generate_transactions_2():
    while True:
        print(random.randrange(20,40))
        time.sleep(1)

thread_1 = Thread(target = generate_transactions)
thread_2 = Thread(target = generate_transactions_2)

thread_1.start()
thread_2.start()


