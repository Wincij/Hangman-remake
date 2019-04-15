from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout,QGridLayout, QLabel, QApplication)
from PyQt5.QtGui import QIcon, QPixmap

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

QLabel {
    margin-left:175px;
    color: #FFFFFF;
    font-family: "Consolas", monospace;
    font: 72px;
}

    """

secret = "HANGMAN"


class Hangman(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()


    def setUI(self):

        self.lostCount = 0
        self.word = QLabel("-" * len(secret))
        self.word.setStyleSheet(style)
        self.mainBox = QVBoxLayout()
        self.setStyleSheet("background-color: #000000;")
        self.buttons = []

        self.hanger = QLabel(self)
        self.hanger.setStyleSheet(style)

        self.setHanger(0)

        self.mainBox.addWidget(self.hanger)
        self.mainBox.addStretch(1)
        self.mainBox.addWidget(self.word)
        self.mainBox.addStretch(1)


        self.setKeys()
        self.setLayout(self.mainBox)
        self.resize(800, 450)
        self.setWindowTitle("Hangman")
        self.show()

    def buttonClick(self):
        letter = self.sender().text()
        if letter in secret:
            for i in range(len(secret)):
                if secret[i] == letter:
                    word = self.updateWord(self.word.text(), i, letter)
                    self.word.setText(word)
                    if secret == word:
                        ## TODO: Victory
                        pass

            self.word.setText(word)
        else:
            self.lostCount+=1
            self.setHanger(self.lostCount)
            if self.lostCount == 9:
                self.defeat()

    def defeat(self):
        newbox = QVBoxLayout()
        self.setLayout(newbox)

    def updateWord(self, word, position, letter):
        return word[:position]+letter+word[position+1:]

    def setHanger(self, elements):
        pixmap = QPixmap('img/s{}.jpg'.format(elements))
        self.hanger.setPixmap(pixmap)


    def setRow(self, row, letters):
        for letter in letters:
            button = QPushButton(letter)
            self.buttons.append(button)
            button.setStyleSheet(style)
            row.addWidget(button)
        return row


    def setKeys(self):
        keyboardBox = QVBoxLayout()
        row1, row2, row3 = QHBoxLayout(), QHBoxLayout(), QHBoxLayout()
        row1.addStretch(5)
        letters = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
        self.setRow(row1, letters)
        row1.addStretch(5)


        row2.addStretch(6)
        letters = ['A','S','D','F','G','H','J','K','L']
        self.setRow(row2, letters)
        row2.addStretch(5)


        row3.addStretch(7)
        letters = ['Z','X','C','V','B','N','M']
        self.setRow(row3, letters)
        row3.addStretch(6)

        keyboardBox.addLayout(row1)
        keyboardBox.addLayout(row2)
        keyboardBox.addLayout(row3)

        self.mainBox.addLayout(keyboardBox)

        for button in self.buttons :
            button.clicked.connect(self.buttonClick)





if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    hangman = Hangman()
    sys.exit(app.exec_())
