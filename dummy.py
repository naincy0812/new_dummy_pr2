def read_file(filepath):
    file = open(filepath, 'r')
    content = file.read()
    return content 
    # file.close() is removed from this position
        # print("HI") is removed from this position
data = read_file("data.txt")
print(data)
