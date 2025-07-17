from file_utils import read_file, write_file

class TextProcessor:
    def __init__(self, filepath):
        self.filepath = filepath

    def run():
        content = read_file(self.filepath)  # ❌ missing 'self' in method definition
        processed = self.clean_text(content)
        write_file(self.filepath, processed)

    def clean_text(self, text):
        return text.lower()

class Tokenizer:
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        return text.split()  # ❌ text is undefined, should be self.text

def helper_function():
    print("Helper running...")
