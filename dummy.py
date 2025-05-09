def read_file(filepath):
    file = open(filepath, 'r')
    content = file.read()
    file.close()
return content)
data = read_file("data.txt")
print(data)
