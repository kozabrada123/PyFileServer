import os
import binascii
import random
import json

import keyring
import config



class file:



    def __init__(self, path=f"{config.files_path}dummy.txt"):

        #Parse name
        self.name=path.replace(config.files_path, "")

        #Parse size
        try:
            self.size = os.path.getsize(path)
        except:
            self.size = 404


        #Parse type
        try:
            self.type = self.name.split(".")
            self.type = self.type[len(self.type)-1]

            if self.type == self.name:
                self.type = "None"
        except:
            self.type = "Empty"


        #Parse path
        if path != None:
            self.path = path

        else:
            self.path = f"{config.files_path}dummy.txt"



    def setName(self, name=None):
        #Parse name
        if name != None:
            self.name=name

        else:
            self.name="dummy" + random.randint(0, 1000)



    def setSize(self, size=0):
        #in bytes

        #Parse size
        if size != None:
            #in bytes
            self.size = size

        else:
            #0b
            self.size = 0


    def setType(self, type=None):
        # Parse type
        if type != None:
            self.type = type

        else:
            self.type = "dummy"

    def setPath(self, path=f"{config.files_path}dummy.txt"):
        # Parse type
        if path != None:
            self.path = path

        else:
            self.path = f"{config.files_path}dummy.txt"

def listFromJson(jsonf):
    filelist = json.loads(jsonf)

    list = []

    for afile in filelist:
        list.append(file(name=afile["name"], size=int(afile["size"]), type=afile["type"], path=afile["path"]))


    return list


def jsonFromList(olist):

    list = []

    for file in olist:
        list.append({"name": file.name, "size": str(file.size), "type": file.type, "path": file.path})

    jsonf = json.dumps(list)

    return jsonf


def saveJson(list):
    with open("files.json", "w") as f:

        f.write(jsonFromList(list))

        f.close()


def loadJson():
    f = open("files.json", "r")

    list = listFromJson(f.read())

    return list


def generateFiles():
    list = []
    oslist = os.listdir(config.files_path)

    for afile in oslist:
        list.append(file(f"{config.files_path}" + afile))

    return list


def normalizeSize(sizeb):





    size = sizeb
    append = "b"

    # >= 1k bytes // 1 * 10 ** 3
    if size >= 1000:

        size = size / 1000
        append = "kb"

        # >= 1mb // 1 * 10 ** 6
        if size >= 1000:
        
            size = size / 1000
            append = "mb"

            # >= 1gb // 1 * 10 ** 9
            if size >= 1000:

                size = size / 1000
                append = "gb"

                # >= 1tb // 1 * 10 ** 12
                if size >= 1000:

                    size = size / 1000
                    append = "tb"

    size = "%.2f" % size
    return f"{str(size)}{append}"




def randomizeName(extension):

    random = binascii.b2a_hex(os.urandom(4)).decode("ascii")
    name = f"{random}.{extension}"
    return name


def getType(name):
    try:
        type = name.split(".")
        type = type[len(type)-1]

        if type == name:
            return ""
    except:
        type = ""

    return type

def setLatest(latestfile, latestfilen, key=None):
    
    with open("temp", "w") as f:
        f.write(latestfile + "!-!" + latestfilen + "!-!" + str(key))
        f.close()

def getLatest():
    f = open("temp", "r")
    latestfile, latestfilen, key = f.read().split("!-!")
    return latestfile, latestfilen, key
