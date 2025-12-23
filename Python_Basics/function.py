#we create a funciton that print hello and a function that do aritmetics

def print_hello(name):
    print(f"Hello {name}")

def sum(x,y,z):
    print(x+y+z)

name = input("Enter your name: ")
print_hello(name)

sum(1,2,3)