def read_file(filepath):
    file = open(filepath, 'r')
    content = file.read()
    return content 
    file.close()
         print("Hi")
data = read_file("data.txt")
print(data)
