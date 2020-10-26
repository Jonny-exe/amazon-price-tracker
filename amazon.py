#!/usr/bin/python3
import argparse
import ast
import json
import logging
import signal
import sys
import urllib.request
from functools import partial

import bs4 as bs
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

filenameDefault = "products.json"


class MyWindow(QMainWindow):
    def __init__(self, args):
        super(MyWindow, self).__init__()
        self.newVars()
        self.getJsonFileData()
        self.setGeometry(1000, 1600, 900, 900)
        self.setWindowTitle("Track amazon products")
        self.initUI()
        self.checkCurretDataValue()
        self.initLabels()

    def getJsonFileData(self):
        args.file.seek(0)
        self.data = self.savedData = ast.literal_eval(args.file.read())
        logging.debug(f"getJsonFileData:: current data: {self.data}")

    def saveData(self):
        newdata = str(self.data) + "\n"
        args.file.seek(0)
        args.file.truncate(args.file.write(newdata))
        args.file.flush()
        if args.debug:
            logging.debug(f"saveData:: re-reading saved data:")
            self.getJsonFileData()  # just for debugging, re-read it

    def newVars(self):
        self.height = 140
        self.width = 30
        self.widthButton = 600
        self.errorMesagge = "Too many requests, try again in 15 mins"
        self.args = args

    def initUI(self):
        height = 50

        # Create main label
        label = QtWidgets.QLabel(self)
        # self.label[0].setStyleSheet("background-color: red")
        label.setText("Introduce the link of the product you want to track")
        label.setFont(QFont("Ubuntu", 15))
        label.move(self.width, height - 35)
        label.adjustSize()

        # Create main button
        b1 = QtWidgets.QPushButton(self)
        b1.setText("Add product")
        b1.setGeometry(650, height, 100, 30)
        b1.move(650, height)
        b1.clicked.connect(self.mainButtonClicked)

        # Create main input
        self.input = QtWidgets.QLineEdit(self)
        self.input.move(self.width, height)
        self.input.resize(600, 30)

    def mainButtonClicked(self):
        url = self.input.text()
        self.newValue(url)
        self.checkValues()

    def shortenUrl(self, url: str) -> str:
        url = url.split("/")
        return url[3]

    def initLabels(self):
        self.products = []
        self.closeButtons = []
        self.productsIndex = 0
        self.productsSpaceDiference = 50
        logging.debug(f"initLabels:: {self.data}")
        self.addLabel(self.data)

    def addLabel(self, newdata):
        colorGreen = "background-color: lightgreen"
        colorRed = "background-color: red"
        for url in newdata:
            # Check if the current url is deleted
            if newdata[url] == "Deleted":
                continue

            try:
                bigger = self.whichIsMoreExpensive(self.data[url], self.savedData[url])
                logging.debug(f"addLabel:: Which is bigger {bigger}")
                logging.debug(
                    f"addLabel:: price {self.data[url]} vs. {self.savedData[url]}"
                )
            except:  # catch *all* exceptions
                e = sys.exc_info()[0]
                logging.error(f"addLabel:: Caught exception\n{e}\n{url}\n{self.data}.")

            shortUrl = self.shortenUrl(url)

            # Create the label
            newLabel = QtWidgets.QLabel(self)
            newLabel.setText(
                f"Product {(self.productsIndex+1)}: {newdata[url]}€\n{shortUrl}"
            )
            newLabel.move(self.width, self.height)
            newLabel.adjustSize()
            if bigger > 0:
                newLabel.setStyleSheet(colorRed)
            elif bigger < 0:
                newLabel.setStyleSheet(colorGreen)
            elif bigger == 0:
                newLabel.setStyleSheet("background-color: lightblue")
            self.products.append(newLabel)

            # Create the close button
            newButton = QtWidgets.QPushButton(self)
            newButton.setText("⨉")
            removeFunction = partial(
                self.removeProduct, newLabel, newButton, self.productsIndex, False, url
            )
            newButton.setGeometry(self.widthButton, self.height, 30, 25)
            newButton.clicked.connect(removeFunction)
            self.closeButtons.append(newButton)

            logging.debug(f"addLabel:: {newButton}")

            # Show the made items and increase iterators
            newLabel.show()
            newButton.show()
            self.height += self.productsSpaceDiference
            self.productsIndex += 1

    def removeProduct(self, label, button, index, checked, url):
        logging.debug(f"removeProduct:: {self}")
        logging.debug(
            f"self: {self}, button: {type(button)} {button}, index: {index}, checked: {type(checked)}"
        )
        logging.debug(f"winid is {button.winId()}")

        # Hiding and removing the label and the button
        button.hide()
        label.hide()

        # Set url to deleted
        self.data[url] = "Deleted"
        self.saveData()
        self.replaceProducts(index)

    def replaceProducts(self, productIndex: int):
        for index in range(productIndex, len(self.products)):
            label = self.products[index]
            button = self.closeButtons[index]

            yPosLabel = label.y()
            yPosButton = button.y()

            self.height -= self.productsSpaceDiference

            label.move(self.width, yPosLabel - self.productsSpaceDiference)
            button.move(self.widthButton, yPosButton - self.productsSpaceDiference)

    def newValue(self, url: str):
        price = str(getPrice(url))
        newdata = {}
        if url not in self.data:
            newdata[url] = price
            self.addLabel(newdata)
        self.data[url] = price

    def whichIsMoreExpensive(self, price1: str, price2: str) -> int:
        try:
            price1 = price1.replace(",", ".")
            price2 = price2.replace(",", ".")
            price1 = float(price1)
            price2 = float(price2)
            if price1 > price2:
                # If prize1 is bigger return 1
                return 1
            elif price1 < price2:
                # If prize2 is bigger return -1
                return -1
            return 0
            # If they are the same return -1
        except:
            # If the input is a value you cant float
            return 0

    def checkCurretDataValue(self):
        jsonData = self.data.copy()
        for url in jsonData:
            if self.data[url] == "Deleted":
                self.data.pop(url)
                continue
            price = getPrice(url)
            if price != self.data[url]:
                self.data[url] = price
                jsonString = str(self.data)
        self.saveData()


def window(args):
    app = QApplication([])
    win = MyWindow(args)
    win.show()
    sys.exit(app.exec())


def getPrice(url) -> str:
    try:
        sauce = urllib.request.urlopen(url)
        soup = bs.BeautifulSoup(sauce, "lxml")
        search = soup.find("span", {"id": "priceblock_ourprice"})
        tag = search.text
        tag = tag[0 : len(tag) - 2]
        logging.debug(tag)
    except:
        logging.debug("except ocurred")
        tag = "Too many requests, try again in 15 mins"
    return tag


def init() -> argparse.Namespace:
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # Argparse
    parser = argparse.ArgumentParser(description="Track amazon prices")
    parser.add_argument(
        "-d",
        "--debug",
        default=True,
        action="store_true",
        help="Turn debug on",
    )
    parser.add_argument(
        "-f",
        "--file",
        # r...read, w...write, +...update(read and write), t...text mode, b...binary
        # see: https://docs.python.org/3/library/functions.html#open
        type=argparse.FileType("r+"),
        default=filenameDefault,
        const=filenameDefault,
        nargs="?",
        help="file for product listings",
    )
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.debug(f"init:: args is set to: {args}")
    logging.debug(f"init:: debug is set to: {args.debug}")
    logging.debug(f"init:: file is set to: {args.file.name}")

    # get the file content
    jsonData = ast.literal_eval(args.file.read())
    logging.debug(f"init:: Initial state of file is: {jsonData}.")
    return args


try:
    args = init()
    window(args)
    args.file.close()
except KeyboardInterrupt:
    logging.debug(f"Received keyboard interrupt.")
    raise
    sys.exit()
except Exception as e:
    logging.error(f"Caught exception {e}.")
    raise
    sys.exit()
