#!/usr/bin/python3
"""Sample Python program."""
import ast


def readTxtFile():
    """Read text file."""
    w = open("test.txt", "rw")
    data = w.read()
    string = "hi this works"
    print(data)
    w.write(string)
    w.close()


def readJsonFile():
    """Read JSON file."""
    w = open("products.json", "r")
    jsonData = ast.literal_eval(w.read())
    print(jsonData)
    w.close()


a = open("test.json", "r")
jsonData = ast.literal_eval(a.read())
print(jsonData)

readJsonFile()
