def read_file(filepath):
    file = open(filepath, 'r')  # ❌ file not closed
    content = file.read()
    return content

def write_file(filepath, content):
file = open(filepath, 'w')  # ❌ IndentationError
    file.write(content)
    file.close()

class FileReader:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        return read_file(self.filename)

class FileWriter:
    def __init__(self, file):
        file = file  # ❌ should be self.file = file

    def save(self, content):
        write_file(self.file, content)  # ❌ self.file doesn't exist
