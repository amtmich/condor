import os

class FileManager:
    def __init__(self, folder_name, file_name):
        self.folder_name = folder_name
        self.file_name = file_name
        self.full_path = os.path.join(self.folder_name, self.file_name)
        
        self.ensure_folder_exists()

    def ensure_folder_exists(self):
        """Check if the folder exists, if not, create it."""
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
            print(f"Directory '{self.folder_name}' created.")
        else:
            print(f"Directory '{self.folder_name}' already exists.")

    def file_exists(self):
        """Check if the file exists."""
        return os.path.exists(self.full_path)

    def set_content(self, content, overwrite=False):
        """Set the content of the file based on the overwrite flag."""
        if overwrite:
            self.write_file(content)
        else:
            if not self.file_exists():
                self.write_file(content)
            else:
                raise FileExistsError(f"File '{self.full_path}' already exists and overwrite is set to False.")

    def write_file(self, content):
        """Write content to the file."""
        with open(self.full_path, 'w') as file:
            file.write(content)
        print(f"File '{self.full_path}' written with content.")

# Example usage:
# file_manager = FileManager('my_folder', 'my_file.txt')
# file_manager.set_content('Hello, World!', overwrite=True)
# print(file_manager.file_exists())  # Should print True
