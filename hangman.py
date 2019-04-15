from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout,QGridLayout, QApplication)

style = """
QPushButton {
    width: 30px;
    height: 30px;
    color: #73ff38;
    text-align:center;
    padding: 5px;
    margin: 5px;
    border: 3px solid #73ff38;
    float: left;
    border-radius: 15px;
    text-align: justify;
    font-size: 32px;
    }

    """


class Hangman(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()


    def setUI(self):



        self.mainBox = QVBoxLayout()
        self.setStyleSheet("background-color: #000000;")
        self.buttons = []
        self.mainBox.addStretch(1)



        self.setKeys()

        self.setLayout(self.mainBox)


        self.resize(800, 450)
        # self.setKeyboard()
        self.setWindowTitle("Hangman")
        self.show()


    def setKeys(self):
        keyboardBox = QVBoxLayout()
        row1 = QHBoxLayout()
        row1.addStretch(5)
        letters = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
        for letter in letters:
            button = QPushButton(letter)
            self.buttons.append(button)
            button.setStyleSheet(style)
            row1.addWidget(button)
        row1.addStretch(5)
        keyboardBox.addLayout(row1)


        row2 = QHBoxLayout()
        row2.addStretch(6)
        letters = ['A','S','D','F','G','H','J','K','L']
        for letter in letters:
            button = QPushButton(letter)
            self.buttons.append(button)
            button.setStyleSheet(style)
            row2.addWidget(button)
        row2.addStretch(5)
        keyboardBox.addLayout(row2)


        row3 = QHBoxLayout()
        row3.addStretch(7)
        letters = ['Z','X','C','V','B','N','M']
        for letter in letters:
            button = QPushButton(letter)
            self.buttons.append(button)
            button.setStyleSheet(style)
            row3.addWidget(button)
        row3.addStretch(6)
        keyboardBox.addLayout(row3)
        self.mainBox.addLayout(keyboardBox)





if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    hangman = Hangman()
    sys.exit(app.exec_())
