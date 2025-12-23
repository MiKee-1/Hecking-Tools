names = []

try:    
    name = input("Enter your name: ")
    names.append(name)
    print(names)

except KeyboardInterrupt:
    print("Keyboard interrupt, goodbye")
