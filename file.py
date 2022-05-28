import os
import random
import json


basicpath = "./files"

class file:



    def __init__(self, path="./files/dummy.txt"):

        #Parse name
        self.name=path.replace("./files/", "")

        #Parse size
        try:
            self.size = os.path.getsize(path)
        except:
            self.size = 404


        #Parse type
        try:
            self.type = self.name.split(".")[1]
        except:
            self.type = "Empty"


        #Parse path
        if path != None:
            self.path = path

        else:
            self.path = "./files/dummy.txt"



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

    def setPath(self, path="./files/dummy.txt"):
        # Parse type
        if path != None:
            self.path = path

        else:
            self.path = "./files/dummy.txt"

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
    oslist = os.listdir(basicpath)

    for afile in oslist:
        list.append(file("./files/" + afile))

    return list