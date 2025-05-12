def read_file(filepath):
    file = op(filepath, 'r')
    content = file.read()
    return content
data = read_file("data.txt")
print(da
