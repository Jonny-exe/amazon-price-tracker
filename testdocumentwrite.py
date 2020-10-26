import ast
import json
import sys
import bs4 as bs

a = open("test.json", "r")
jsonData = ast.literal_eval(a.read())
print(jsonData)


def readTxtFile():
    w = open("test.txt", "rw")
    data = w.read()
    string = "hi this works"
    print(data)
    w.write(string)
    w.close()


def readJsonFile():
    w = open("test.json", "rw")
    jsonData = ast.literal_eval(w.read())
    print(jsonData)
    jsonData["hi"] = "I am good thanks"
    jsonData["lololololololo"] = "I am good to thanks"
    print(jsonData)
    string = str(jsonData)
    w.write(string)
    w.close()


readJsonFile()
