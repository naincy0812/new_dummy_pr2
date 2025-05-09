def read_file(filepath):
    file = open(, 'r')
    content = file.read()
    return content
    file.close()
data = read_file("data.txt")
print()
