import threading
from matplotlib import pyplot as plt

lock = threading.Lock()
current_number = 2
count = 0
phi_list = []
running = True


def is_prime(x):
    for i in range(2, x // 2 + 1):
        if x % i == 0:
            return False
    return True

def find_primes():
    global current_number
    global count 
    global running
    global lock
    global phi_list

    while running:
        with lock:
            if is_prime(current_number):
                count += 1
            phi_list.append(count)
            current_number += 1

def user_interact():
    global current_number
    global count 
    global running
    global lock
    global phi_list

    while True:
        cmd = input("> ")
        if cmd == 'count':
            with lock:
                print(current_number, count)
        elif cmd == 'exit':
            running = False
            break
        elif cmd == 'plot':
            with lock:
                n = list(range(2, len(phi_list) + 2))
                plt.figure(figsize=(5,5))
                plt.plot(n, phi_list)
                plt.show()
                
    

thread1 = threading.Thread(target=find_primes)
thread2 = threading.Thread(target=user_interact)
thread1.start()
thread2.start()