from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from gui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    # operation = 'minus'
    v = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    h = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    win = False
    hint = False
    selection = ['', -1, -1]
    num = [0, 0, 0, 0, 0, 0]

    def reset(self):
        self.v = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        self.h = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.win = False
        self.hint = False
        self.selection = ['', -1, -1]
        self.num = [0, 0, 0, 0, 0, 0]

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # buttons
        for n in range(1, 11):
            getattr(self, 'pushButton_%s' % n).pressed.connect(lambda start_level=n: self.start(start_level))
        self.pushButton_back.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_hint.clicked.connect(self.hint_f)
        for i in range(12):
            for o in range(2):
                getattr(self, 'pushButton_v%s' % int(str(i + 1) + str(o + 1))).pressed.connect(
                    lambda select=['v', i, o]: self.move(select))
        for i in range(6):
            for o in range(3):
                getattr(self, 'pushButton_h%s' % int(str(i + 1) + str(o + 1))).pressed.connect(
                    lambda select=['h', i, o]: self.move(select))
        # self.pushButton_plus.pressed.connect(lambda select=['+', -1, -1]: self.move(select))

    def draw(self):
        for i in range(12):
            for o in range(2):
                if self.v[i][o] == 0:
                    getattr(self, 'v%s' % int(str(i + 1) + str(o + 1))).hide()
                    getattr(self, 'pushButton_v%s' % int(str(i + 1) + str(o + 1))).setStyleSheet(
                        'background: rgba(200,0,0,0.1);')
                elif self.v[i][o] == 1:
                    getattr(self, 'v%s' % int(str(i + 1) + str(o + 1))).show()
                    getattr(self, 'pushButton_v%s' % int(str(i + 1) + str(o + 1))).setStyleSheet(
                        'background: rgba(200,0,0,0);')
                getattr(self, 'label_v%s' % int(str(i + 1) + str(o + 1))).hide()

        for i in range(6):
            for o in range(3):
                if self.h[i][o] == 0:
                    getattr(self, 'h%s' % int(str(i + 1) + str(o + 1))).hide()
                    getattr(self, 'pushButton_h%s' % int(str(i + 1) + str(o + 1))).setStyleSheet(
                        'background: rgba(200,0,0,0.1);')
                elif self.h[i][o] == 1:
                    getattr(self, 'h%s' % int(str(i + 1) + str(o + 1))).show()
                    getattr(self, 'pushButton_h%s' % int(str(i + 1) + str(o + 1))).setStyleSheet(
                        'background: rgba(200,0,0,0);')
                getattr(self, 'label_h%s' % int(str(i + 1) + str(o + 1))).hide()

        # show only plus
        self.pushButton_plus.hide()
        self.label_plus.hide()
        """        if self.operation == 'minus':
            self.plus.hide()
            self.pushButton_plus.setStyleSheet('background: rgba(200,0,0,0.1);')
            self.label_plus.hide()
        elif self.operation == 'plus':
            self.plus.show()
            self.pushButton_plus.setStyleSheet('background: rgba(200,0,0,0);')
            self.label_plus.hide()
        elif self.operation == 'plus_selected':
            self.plus.show()
            self.pushButton_plus.setStyleSheet('background: rgba(200,0,0,0);')
            self.label_plus.show()"""

        # win alert
        if self.win:
            self.label_game.show()
        else:
            self.label_game.hide()

        # hint show
        if self.hint:
            self.label_hint.show()
            self.label_hint.setText('')
        else:
            self.label_hint.hide()

        # selection label
        if (self.selection[1] != -1) and (self.selection[2] != -1) and (self.selection[0] == 'v'):
            getattr(self, 'label_v%s' % int(str(self.selection[1] + 1) + str(self.selection[2] + 1))).show()
        elif (self.selection[1] != -1) and (self.selection[2] != -1) and (self.selection[0] == 'h'):
            getattr(self, 'label_h%s' % int(str(self.selection[1] + 1) + str(self.selection[2] + 1))).show()

    def equals(self):
        # 01 matrix to numbers
        for i in range(6):
            if (self.v[i][0] == 1) and (self.v[i][1] == 1) and (self.v[i + 1][0] == 1) and (self.v[i + 1][1] == 1) and (
                    self.h[i][0] == 1) and (self.h[i][1] == 0) and (self.h[i][2] == 1):
                self.num[i] = 0
            elif (self.v[i][0] == 0) and (self.v[i][1] == 0) and (self.v[i + 1][0] == 1) and (
                    self.v[i + 1][1] == 1) and (self.h[i][0] == 0) and (self.h[i][1] == 0) and (self.h[i][2] == 0):
                self.num[i] = 1
            elif (self.v[i][0] == 0) and (self.v[i][1] == 1) and (self.v[i + 1][0] == 1) and (
                    self.v[i + 1][1] == 0) and (self.h[i][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 2
            elif (self.v[i][0] == 0) and (self.v[i][1] == 0) and (self.v[i + 1][0] == 1) and (
                    self.v[i + 1][1] == 1) and (self.h[i][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 3
            elif (self.v[i][0] == 1) and (self.v[i][1] == 0) and (self.v[i + 1][0] == 1) and (
                    self.v[i + 1][1] == 1) and (self.h[i][0] == 0) and (self.h[i][1] == 1) and (self.h[i][2] == 0):
                self.num[i] = 4
            elif (self.v[i][0] == 1) and (self.v[i][1] == 0) and (self.v[i + 1][0] == 0) and (
                    self.v[i + 1][1] == 1) and (self.h[i][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 5
            elif (self.v[i][0] == 1) and (self.v[i][1] == 1) and (self.v[i + 1][0] == 0) and (
                    self.v[i + 1][1] == 1) and (self.h[i][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 6
            elif (self.v[i][0] == 0) and (self.v[i][1] == 0) and (self.v[i + 1][0] == 1) and (
                    self.v[i + 1][1] == 1) and (self.h[i][0] == 1) and (self.h[i][1] == 0) and (self.h[i][2] == 0):
                self.num[i] = 7
            elif (self.v[i][0] == 1) and (self.v[i][1] == 1) and (self.v[i + 1][0] == 1) and (
                    self.v[i + 1][1] == 1) and (self.h[i][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 8
            elif (self.v[i][0] == 1) and (self.v[i][1] == 0) and (self.v[i + 1][0] == 1) and (
                    self.v[i + 1][1] == 1) and (self.h[i][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 9
            else:
                return False
        return self.num[0] * 10 + self.num[1] + self.num[2] * 10 + self.num[3] == self.num[4] * 10 + self.num[5]

    def move(self, select):
        # selection
        if (self.selection[1] == -1) and (self.selection[2] == -1):
            self.selection = select
            self.draw()
            return

        if self.selection == select:
            self.selection = ['', -1, -1]
            self.draw()
            return

        # moving
        if (self.selection != select) and (self.selection[1] != -1) and (self.selection[2] != -1):
            if (getattr(self, str(self.selection[0]))[self.selection[1]][self.selection[2]] == 1) and (
                    getattr(self, str(select[0]))[select[1]][select[2]] == 0):
                getattr(self, str(self.selection[0]))[self.selection[1]][self.selection[2]] = 0
                getattr(self, str(select[0]))[select[1]][select[2]] = 1
                self.selection = ['', -1, -1]

        self.draw()
        if self.equals():
            self.win = True

    def hint_f(self):
        self.hint = True
        self.draw()

    def start(self, start_level):
        if start_level == 1:
            self.reset()
            self.v = [[1, 1], [0, 1], [1, 0], [0, 1], [1, 0], [1, 1], [1, 1], [1, 1], [0, 0], [1, 1], [1, 0], [1, 1]]
            self.h = [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [0, 0, 0], [0, 1, 0]]
            #self.operation = 'plus'
        """elif start_level == 2:

        elif start_level == 3:

        elif start_level == 4:

        elif start_level == 5:

        elif start_level == 6:

        elif start_level == 7:

        elif start_level == 8:

        elif start_level == 9:

        elif start_level == 10:"""

        self.draw()
        self.stackedWidget.setCurrentIndex(0)


def application():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setWindowTitle('Головоломки со спичками')
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
