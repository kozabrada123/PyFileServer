from file import *

class filemanager:

    def __init__(self):
        self.files = []

    # Generate files
    def refreshFiles(self):
        self.files = generateFiles()
        saveJson(self.files)

        print("Refreshed Files..")