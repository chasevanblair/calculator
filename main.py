from functools import partial
import sys


from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QComboBox
)
from datetime import datetime

WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
FORMAT_TYPE = "base 10"

class CalcWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)
        #answer format box
        comboFormats = QComboBox()
        comboFormats.addItem("base 10")
        comboFormats.addItem("hexadecimal")
        comboFormats.addItem("octal")
        comboFormats.addItem("binary")
        

        self.generalLayout.addWidget(comboFormats)
    
    def _createButtons(self):
        buttonsLayout = QGridLayout()
        # probably a better way to do this
        # numbers
        buttonsLayout.addWidget(QPushButton("1"), 0, 0)
        buttonsLayout.addWidget(QPushButton("2"), 0, 1)
        buttonsLayout.addWidget(QPushButton("3"), 0, 2)
        buttonsLayout.addWidget(QPushButton("4"), 1, 0)
        buttonsLayout.addWidget(QPushButton("5"), 1, 1)
        buttonsLayout.addWidget(QPushButton("6"), 1, 2)
        buttonsLayout.addWidget(QPushButton("7"), 2, 0)
        buttonsLayout.addWidget(QPushButton("8"), 2, 1)
        buttonsLayout.addWidget(QPushButton("9"), 2, 2)
        buttonsLayout.addWidget(QPushButton("0"), 3, 0)

        #operators
        #+-*/()
        buttonsLayout.addWidget(QPushButton("+"), 0, 3)
        buttonsLayout.addWidget(QPushButton("-"), 1, 3)
        buttonsLayout.addWidget(QPushButton("*"), 2, 3)
        buttonsLayout.addWidget(QPushButton("/"), 3, 3)
        buttonsLayout.addWidget(QPushButton("("), 3, 1)
        buttonsLayout.addWidget(QPushButton(")"), 3, 2)
        buttonsLayout.addWidget(QPushButton("C"), 4, 0)
        buttonsLayout.addWidget(QPushButton("="), 4, 3)

        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()
    
    def clearDisplay(self):
        self.setDisplayText("")

class Calc:
    def __init__(self, model, view):
        self.eval = model
        self.view = view
        self.connectSignalSlots()

    def calcResult(self):
        result = self.eval(expression=self.view.displayText())
        self.view.setDisplayText(result)
    
    def makeExpression(self, subExp):
        if self.view.displayText() == "error":
            self.view.clearDisplay()
        exp = self.view.displayText() + subExp
        self.view.setDisplayText(exp)

    def connectSignalSlots(self):
        widgets = self.view.children()
        layout = widgets[1]
        for widget in layout.children():
            if type(widget) == QPushButton:
                # print(widget.text())
                text = widget.text()
                if text == "=":
                    widget.clicked.connect(self.calcResult)
                elif text == "C":
                    widget.clicked.connect(self.view.clearDisplay)
                else:
                    widget.clicked.connect(partial(self.makeExpression, text))
            if type(widget) == QComboBox:
                widget.currentTextChanged.connect(self.formatChange)
        
    def formatChange(self, format):
        global FORMAT_TYPE
        FORMAT_TYPE = format
        print(FORMAT_TYPE)



        


def calcAnswer(expression):
    try:
        result = eval(expression)
        #dont need eval if base 10
        print("sdf" + FORMAT_TYPE)
        if FORMAT_TYPE == "octal":
            result = format(result, 'o')
        elif FORMAT_TYPE == "hexadecimal":
            result = format(result, 'x')
        elif FORMAT_TYPE == "binary":
            result = bin(result)
            print( result)
        result = str(result)
    except Exception:
        result = "error"

    with open('output.txt', 'a') as f:
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f.write(dt_string + " " + FORMAT_TYPE + ": " + result + "\n")
    
    return result
    #TODO PRINT TO FILE


def main():
    calcApp = QApplication([])
    calcWindow = CalcWindow()
    calcWindow.show()
    Calc(model=calcAnswer, view=calcWindow)
    sys.exit(calcApp.exec())


if __name__ == "__main__":
    main()
