def read_file(filepath):
    file = open(filepath, 'r')
    content = file.read()
    return content
data = read_file("data.txt")
print(data)
