#to create and write something in the file
with open('./data.txt','w') as file:
    file.write('hello there \n')
    file.write('I am loser . . .')

#to open this file in a readable format and read information from this file
with open('./data.txt','r') as file:
    data = file.read()
    print(data)

