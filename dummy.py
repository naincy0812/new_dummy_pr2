def read_file(filepath):
    file = open(filepath, 'r')
    content = file.read()
    return content

def write_file(filepath, content):
file = open(filepath, 'w')  # ❌ IndentationError
file.write(content)
file.close()

class FileProcessor:
    def __init__(self, path):
        path = path  # ❌ should be self.path = path

    def process_file():
        data = read_file(self.path)  # ❌ missing 'self' in function definition
        modified = self.modify_content(data)
        write_file(self.path, modified)

    def modify_content(self, content):
        return content.upper()

data = read_file("data.txt")
print(data)

processor = FileProcessor("data.txt")
processor.process_file()  # ❌ This will raise AttributeError due to self.path not being set
