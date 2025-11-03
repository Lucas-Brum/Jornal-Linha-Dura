class ReadFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = None

    def read_file(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
                return self.content
        except FileNotFoundError:
            print("Error: file not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
