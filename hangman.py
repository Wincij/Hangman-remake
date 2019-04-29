from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QGridLayout, QLabel,
    QApplication, QDesktopWidget, QGraphicsOpacityEffect)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QKeySequence
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import *
import random


QPushButtonStyle = """
    width: 30px;
    height: 30px;
    color: #73ff38;
    text-align:center;
    padding: 5px;
    margin: 5px;
    float: left;
    border-radius: 15px;
    text-align: justify;
    font-size: 32px;
"""

def random_line():
    afile = open("words/words.txt", "r")
    line = next(afile)
    for num, aline in enumerate(afile, 2):
      if random.randrange(num): continue
      line = aline
    return line.upper()[0:-1]


class Hangman(QWidget):
    def __init__(self):
        super().__init__()
        self.mainBox = QVBoxLayout()
        self.setLayout(self.mainBox)
        self.setUI()

    def fade(self, widget, duration,startValue, endValue):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(duration)
        self.animation.setStartValue(startValue)
        self.animation.setEndValue(endValue)
        self.animation.start()


    def setTextLabel(self):
        """
        Set up and style hidden word
        """
        self.word = QLabel("_" * len(self.secret))
        self.word.setText("_" * len(self.secret))
        font = QFont()
        font.setBold(True)
        font.setLetterSpacing(QFont.AbsoluteSpacing,30)
        self.word.setAlignment(Qt.AlignCenter)
        self.word.setFont(font)
        self.word.setStyleSheet("""color: #FFFFFF;font-family: "Consolas", monospace; font: 44px; font-weight: bold;""")


    def setUI(self):
        """
        Main window interface setter
        """
        self.secret = random_line()
        self.setWindowIcon(QIcon('img/rope.ico'))
        self.lostCount = 0

        self.setStyleSheet("background-color: #000000;")
        self.buttons = []
        self.sounds = {
            'yes': QSound("sound/yes.wav"),
            'no': QSound("sound/no.wav")
        }
        self.hanger = QLabel(self)
        self.hanger.setAlignment(Qt.AlignCenter)


        self.setTextLabel()
        self.setHanger(0)

        self.mainBox.addStretch(5)
        self.mainBox.addWidget(self.hanger)
        self.mainBox.addStretch(5)
        self.mainBox.addWidget(self.word)
        self.mainBox.addStretch(5)

        self.setKeyboard()

        self.resize(800, 800)

        # Some tricky way to center application window on the screen
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowTitle("Hangman")
        self.show()

    def buttonClick(self):
        """
        This method detects which button was clicked.
        If the letter is in secret word (once or more) it disappears (visually, the button instance stays on its place).
        If not button becomes red and inactive. The lost counter increments.
        Whenever whole hanger is drawn it calls gameOver(with result) method.
        """
        letter = self.sender().text()
        if letter in self.secret:
            for i in range(len(self.secret)):
                if self.secret[i] == letter:
                    word = self.updateWord(self.word.text(), i, letter)
                    self.word.setText(word)
                    self.sender().setStyleSheet(QPushButtonStyle + "border: 3px solid #000000; color: #000000;")
                    self.sounds['yes'].play()
                    self.word.setText(word)
                    if self.secret == word:
                        self.emptyLoop(2000)
                        self.gameOver(True)
                        pass
                        #here
        else:
            self.lostCount+=1
            self.setHanger(self.lostCount)
            self.sender().setStyleSheet(QPushButtonStyle + "border: 3px solid #FF1111; color: #FF1111;")
            self.sender().clicked.disconnect()
            self.sounds['no'].play()
            if self.lostCount == 9:
                self.emptyLoop(2000)
                self.word.setText(self.secret)
                self.emptyLoop(2000)
                self.gameOver(False)

    def emptyLoop(self, duration):
        """
        Sets os.sleep method that is more friendly to PyQt5
        """
        loop = QEventLoop()
        QTimer.singleShot(duration, loop.quit)
        loop.exec_()



    def updateWord(self, word, position, letter):
        """
        Inserts letter at word[position]
        """
        return word[:position]+letter+word[position+1:]

    def setHanger(self, elements):
        """
        Sets and updates hanger image each time user hits button with letter that is not contained in hidden word
        """
        pixmap = QPixmap('img/{}.jpg'.format(elements))
        self.hanger.setPixmap(pixmap)
        self.fade(self.hanger, 2500, 1, 0.75)


    def setRow(self, row, letters):
        """
        Sets one "row" of keyboard and assigns its shortcut. Returns row (QHBoxLayout type)
        """
        for letter in letters:
            button = QPushButton(letter)
            self.buttons.append(button)
            button.setStyleSheet(QPushButtonStyle + "border: 3px solid #73ff38;")
            row.addWidget(button)
        return row

    def clearLayout(self, layout):
        """
        Clears whole layout
        """
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())



    def gameOver(self, result):
        """
        Method called by buttonClick() with result:
        True - Win
        False - Defeat
        Clears mainBox (self.layout) and sets up end screen with info.
        """
        self.clearLayout(self.mainBox)
        self.word.deleteLater()
        resultText = QLabel()
        font = QFont()
        font.setBold(True)
        resultText.setAlignment(Qt.AlignCenter)
        resultText.setFont(font)
        self.mainBox.addWidget(resultText)
        if result:
            resultText.setText("Victory")
            resultText.setStyleSheet("""color: #00FF00;font-family: "Consolas", monospace; font: 72px; font-weight: bold;""")
            # self.fade(resultText, 2500, 0, 1)
            # self.setUI()
        else:
            resultText.setText("Defeat")
            resultText.setStyleSheet("""color: #FF0000;font-family: "Consolas", monospace; font: 72px; font-weight: bold;""")

        self.fade(resultText, 2500, 0, 1)
        self.emptyLoop(5000)
        resultText.deleteLater()
        self.emptyLoop(5000)
        self.setUI()

    def setKeyboard(self):
        """
        Creates seperated layout (keyboardBox), fills it with rows of buttons and then places it in mainBox
        At the end connects buttons to 'clicked' event
        """
        keyboardBox = QVBoxLayout()
        row1, row2, row3 = QHBoxLayout(), QHBoxLayout(), QHBoxLayout()
        row1.setAlignment(Qt.AlignCenter)
        letters = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
        self.setRow(row1, letters)

        row2.setAlignment(Qt.AlignCenter)
        letters = ['A','S','D','F','G','H','J','K','L']
        self.setRow(row2, letters)

        row3.setAlignment(Qt.AlignCenter)
        letters = ['Z','X','C','V','B','N','M']
        self.setRow(row3, letters)

        keyboardBox.addLayout(row1)
        keyboardBox.addLayout(row2)
        keyboardBox.addLayout(row3)

        self.mainBox.addLayout(keyboardBox)

        for button in self.buttons:
            button.clicked.connect(self.buttonClick)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    hangman = Hangman()
    sys.exit(app.exec_())
