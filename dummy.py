def read_file(filepath):
    file = open(filepath, 'r')
    content = file.read()
    return content
    file.close()  # ❌ Unreachable code; file is never closed properly

data = read_file("data.txt")
print(data)
