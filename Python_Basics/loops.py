fruits = ['apple','mango','banana']

#for loop will help to go through the list 

for index,fruit in enumerate(fruits, start=1):
    print(f" {index} : {fruit}")

#while loop

name = input("Enter your name: ")

while name == '':
    name = input("Enter your name: ")

print(f"Hello {name}")