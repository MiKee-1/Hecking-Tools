#threading help us to create multiple process to work in parallel
import threading
import time

def print_number():
    for i in range(1,6):
        print(f"number: {i}")
        time.sleep(1)


def print_letters():
    for letter in 'ABCDE':
        print(f"Letter: {letter}")
        time.sleep(1)

# i want my program to print numbers and letters at the same time

thread1 = threading.Thread(target=print_number)
thread2 = threading.Thread(target=print_letters)

thread1.start()
thread2.start()

#the join function let our threads to work in a synchronized way
thread1.join()
thread2.join()

print("both threads have finished executions")