from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from gui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    operation = 1  # 1 - минус, 2 - плюс
    operation_start = 1
    # 0 и 1 в массивах означают наличие спичек в определенных местах. v - вертикальное расположение,
    # h - горизонтальное/ массивы start хранят данные об изначальном положении
    v = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    h = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    v_start = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    h_start = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    win = False
    hint = False
    selection = ['', -1, -1]  # хранит индексы для массива v и h, означающие выделенный элемент
    num = [0, 0, 0, 0, 0, 0]
    level = 1

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
        self.pushButton_plus.pressed.connect(lambda select=['+', -1, -1]: self.move(select))

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

        if self.operation == 1:
            self.plus.hide()
            self.pushButton_plus.setStyleSheet('background: rgba(200,0,0,0.1);')
            self.label_plus.hide()
        elif self.operation == 2:
            self.plus.show()
            self.pushButton_plus.setStyleSheet('background: rgba(200,0,0,0);')
            self.label_plus.hide()

        # win alert
        if self.win:
            self.label_game.show()
        else:
            self.label_game.hide()

        # hint show
        if self.hint:
            self.label_hint.show()
            if self.level == 1:
                self.label_hint.setText('65+09=74')
            elif self.level == 2:
                self.label_hint.setText('10+24=34')
            elif self.level == 3:
                self.label_hint.setText('37+16=53')
            elif self.level == 4:
                self.label_hint.setText('98-88=10')
            elif self.level == 5:
                self.label_hint.setText('91-11=80')
            elif self.level == 6:
                self.label_hint.setText('71-30=41')
            elif self.level == 7:
                self.label_hint.setText('32-13=19')
            elif self.level == 8:
                self.label_hint.setText('13+28=41')
            elif self.level == 9:
                self.label_hint.setText('25-13=12')
            elif self.level == 10:
                self.label_hint.setText('99-81=18')
        else:
            self.label_hint.hide()

        # selection label
        if (self.selection[1] != -1) and (self.selection[2] != -1) and (self.selection[0] == 'v'):
            getattr(self, 'label_v%s' % int(str(self.selection[1] + 1) + str(self.selection[2] + 1))).show()
        elif (self.selection[1] != -1) and (self.selection[2] != -1) and (self.selection[0] == 'h'):
            getattr(self, 'label_h%s' % int(str(self.selection[1] + 1) + str(self.selection[2] + 1))).show()
        elif self.selection[0] == '+':
            self.label_plus.show()

    def equals(self):
        # перевод массивов 0 и 1 в цифры. Далее - проверка равенства
        for i in range(6):
            if (self.v[i * 2][0] == 1) and (self.v[i * 2][1] == 1) and (self.v[i * 2 + 1][0] == 1) and (
                    self.v[i * 2 + 1][1] == 1) and (
                    self.h[i][0] == 1) and (self.h[i][1] == 0) and (self.h[i][2] == 1):
                self.num[i] = 0
            elif (self.v[i * 2][0] == 0) and (self.v[i * 2][1] == 0) and (self.v[i * 2 + 1][0] == 1) and (
                    self.v[i * 2 + 1][1] == 1) and (self.h[i][0] == 0) and (self.h[i][1] == 0) and (self.h[i][2] == 0):
                self.num[i] = 1
            elif (self.v[i * 2][0] == 0) and (self.v[i * 2][1] == 1) and (self.v[i * 2 + 1][0] == 1) and (
                    self.v[i * 2 + 1][1] == 0) and (self.h[i][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 2
            elif (self.v[i * 2][0] == 0) and (self.v[i * 2][1] == 0) and (self.v[i * 2 + 1][0] == 1) and (
                    self.v[i * 2 + 1][1] == 1) and (self.h[i][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 3
            elif (self.v[i * 2][0] == 1) and (self.v[i * 2][1] == 0) and (self.v[i * 2 + 1][0] == 1) and (
                    self.v[i * 2 + 1][1] == 1) and (self.h[i][0] == 0) and (self.h[i][1] == 1) and (self.h[i][2] == 0):
                self.num[i] = 4
            elif (self.v[i * 2][0] == 1) and (self.v[i * 2][1] == 0) and (self.v[i * 2 + 1][0] == 0) and (
                    self.v[i * 2 + 1][1] == 1) and (self.h[2][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 5
            elif (self.v[i * 2][0] == 1) and (self.v[i * 2][1] == 1) and (self.v[i * 2 + 1][0] == 0) and (
                    self.v[i * 2 + 1][1] == 1) and (self.h[i][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 6
            elif (self.v[i * 2][0] == 0) and (self.v[i * 2][1] == 0) and (self.v[i * 2 + 1][0] == 1) and (
                    self.v[i * 2 + 1][1] == 1) and (self.h[i][0] == 1) and (self.h[i][1] == 0) and (self.h[i][2] == 0):
                self.num[i] = 7
            elif (self.v[i * 2][0] == 1) and (self.v[i * 2][1] == 1) and (self.v[i * 2 + 1][0] == 1) and (
                    self.v[i * 2 + 1][1] == 1) and (self.h[i][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 8
            elif (self.v[i * 2][0] == 1) and (self.v[i * 2][1] == 0) and (self.v[i * 2 + 1][0] == 1) and (
                    self.v[i * 2 + 1][1] == 1) and (self.h[i][0] == 1) and (self.h[i][1] == 1) and (self.h[i][2] == 1):
                self.num[i] = 9
            else:
                return False
        if self.operation == 1:
            return self.num[0] * 10 + self.num[1] - (self.num[2] * 10 + self.num[3]) == self.num[4] * 10 + self.num[5]
        elif self.operation == 2:
            return self.num[0] * 10 + self.num[1] + (self.num[2] * 10 + self.num[3]) == self.num[4] * 10 + self.num[5]

    def compare(self):
        dif = 0  # данные о разнице между массивами h,v и h_start,v_start
        for i in range(0, 6):
            if self.h_start[i][0] != self.h[i][0]: dif += 1
            if self.h_start[i][1] != self.h[i][1]: dif += 1
            if self.h_start[i][2] != self.h[i][2]: dif += 1
        for i in range(0, 12):
            if self.v_start[i][0] != self.v[i][0]: dif += 1
            if self.v_start[i][1] != self.v[i][1]: dif += 1

        if self.operation != self.operation_start:
            if max(self.operation, self.operation_start) - 1 == min(self.operation, self.operation_start):
                dif += 1
        print(dif)
        if dif <= 4:
            return True

    def move(self, select):
        # selection - последняя позиция, select - новая позиция

        # первое нажатие
        if (self.selection[1] == -1) and (self.selection[2] == -1) and (self.selection[0] == ''):
            self.selection = select
            self.draw()
            return

        # отмена выделения
        if self.selection == select:
            self.selection = ['', -1, -1]
            self.draw()
            return

        # перемещение
        if self.selection != select:
            if self.selection[0] == '+':
                self.operation = 1
                getattr(self, str(select[0]))[select[1]][select[2]] = 1
                self.selection = ['', -1, -1]
            elif (select[0] == '+') and (self.operation == 1):
                self.operation = 2
                getattr(self, str(self.selection[0]))[self.selection[1]][self.selection[2]] = 0
                self.selection = ['', -1, -1]

            elif (self.selection[1] != -1) and (self.selection[2] != -1) and (select[0] != '+'):
                # если старая позиция = 1 и новая = 0, то в h или v старая позиция = 0, а новая = 1. затем обнуление выделения
                if (getattr(self, str(self.selection[0]))[self.selection[1]][self.selection[2]] == 1) and (
                        getattr(self, str(select[0]))[select[1]][select[2]] == 0):
                    getattr(self, str(self.selection[0]))[self.selection[1]][self.selection[2]] = 0
                    getattr(self, str(select[0]))[select[1]][select[2]] = 1
                    self.selection = ['', -1, -1]

        if self.equals() and self.compare():
            self.win = True

        self.draw()

    def hint_f(self):
        self.hint = True
        self.draw()

    def start(self, start_level):
        self.reset()
        self.level = start_level
        # выбор уровня
        if start_level == 1:
            self.v = [[1, 1], [0, 1], [1, 0], [0, 1], [1, 0], [1, 1], [1, 1], [1, 1], [0, 0], [1, 1], [1, 0], [1, 1]]
            self.h = [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [0, 0, 0], [0, 1, 0]]
            self.v_start = [[1, 1], [0, 1], [1, 0], [0, 1], [1, 0], [1, 1], [1, 1], [1, 1], [0, 0], [1, 1], [1, 0], [1, 1]]
            self.h_start = [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [0, 0, 0], [0, 1, 0]]
            self.operation = 2
        elif start_level == 2:
            self.v = [[0, 0], [1, 1], [0, 0], [1, 1], [0, 1], [1, 0], [1, 0], [1, 1], [1, 0], [1, 1], [1, 0], [1, 1]]
            self.h = [[0, 0, 0], [1, 1, 1], [1, 1, 1], [0, 1, 0], [1, 1, 1], [0, 1, 0]]
            self.v_start = [[0, 0], [1, 1], [0, 0], [1, 1], [0, 1], [1, 0], [1, 0], [1, 1], [1, 0], [1, 1], [1, 0], [1, 1]]
            self.h_start = [[0, 0, 0], [1, 1, 1], [1, 1, 1], [0, 1, 0], [1, 1, 1], [0, 1, 0]]
            self.operation = 2
        elif start_level == 3:
            self.v = [[0, 0], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [1, 1], [0, 1], [1, 1], [1, 1], [0, 0], [1, 1]]
            self.h = [[1, 1, 1], [1, 0, 0], [0, 0, 0], [1, 1, 1], [1, 1, 1], [1, 0, 0]]
            self.v_start = [[0, 0], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [1, 1], [0, 1], [1, 1], [1, 1], [0, 0], [1, 1]]
            self.h_start = [[1, 1, 1], [1, 0, 0], [0, 0, 0], [1, 1, 1], [1, 1, 1], [1, 0, 0]]
            self.operation = 2
        elif start_level == 4:
            self.v = [[1, 0], [1, 1], [1, 1], [1, 1], [1, 1], [0, 1], [1, 1], [1, 1], [0, 0], [1, 1], [1, 1], [1, 1]]
            self.h = [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 0, 0], [1, 0, 1]]
            self.v_start = [[1, 0], [1, 1], [1, 1], [1, 1], [1, 1], [0, 1], [1, 1], [1, 1], [0, 0], [1, 1], [1, 1], [1, 1]]
            self.h_start = [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 0, 0], [1, 0, 1]]
            self.operation = 1
        elif start_level == 5:
            self.v = [[0, 0], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [1, 1], [1, 1], [1, 1], [0, 1]]
            self.h = [[1, 1, 1], [1, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 1], [1, 1, 1]]
            self.v_start = [[0, 0], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [1, 1], [1, 1], [1, 1], [0, 1]]
            self.h_start = [[1, 1, 1], [1, 0, 0], [0, 0, 0], [0, 0, 0], [1, 1, 1], [1, 1, 1]]
            self.operation = 1
        elif start_level == 6:
            self.v = [[0, 0], [1, 1], [0, 0], [1, 1], [1, 0], [0, 1], [1, 1], [1, 1], [1, 0], [1, 1], [0, 0], [1, 1]]
            self.h = [[1, 0, 0], [0, 0, 0], [1, 1, 1], [1, 0, 1], [0, 1, 0], [0, 0, 0]]
            self.v_start = [[0, 0], [1, 1], [0, 0], [1, 1], [1, 0], [0, 1], [1, 1], [1, 1], [1, 0], [1, 1], [0, 0], [1, 1]]
            self.h_start = [[1, 0, 0], [0, 0, 0], [1, 1, 1], [1, 0, 1], [0, 1, 0], [0, 0, 0]]
            self.operation = 1
        elif start_level == 7:
            self.v = [[0, 1], [1, 0], [0, 1], [1, 0], [0, 0], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [1, 0], [0, 1]]
            self.h = [[1, 1, 1], [1, 1, 1], [0, 0, 0], [1, 1, 1], [0, 0, 0], [1, 1, 1]]
            self.v_start = [[0, 1], [1, 0], [0, 1], [1, 0], [0, 0], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [1, 0], [0, 1]]
            self.h_start = [[1, 1, 1], [1, 1, 1], [0, 0, 0], [1, 1, 1], [0, 0, 0], [1, 1, 1]]
            self.operation = 2
        elif start_level == 8:
            self.v = [[0, 0], [1, 1], [0, 0], [1, 1], [0, 1], [1, 0], [1, 1], [0, 1], [0, 0], [1, 1], [0, 0], [1, 1]]
            self.h = [[0, 0, 0], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [0, 0, 0]]
            self.v_start = [[0, 0], [1, 1], [0, 0], [1, 1], [0, 1], [1, 0], [1, 1], [0, 1], [0, 0], [1, 1], [0, 0], [1, 1]]
            self.h_start = [[0, 0, 0], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [0, 0, 0]]
            self.operation = 2
        elif start_level == 9:
            self.v = [[0, 1], [1, 0], [1, 0], [0, 1], [0, 0], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [1, 0], [0, 1]]
            self.h = [[1, 1, 1], [1, 1, 1], [0, 0, 0], [1, 1, 1], [0, 0, 0], [1, 1, 1]]
            self.v_start = [[0, 1], [1, 0], [1, 0], [0, 1], [0, 0], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [1, 0], [0, 1]]
            self.h_start = [[1, 1, 1], [1, 1, 1], [0, 0, 0], [1, 1, 1], [0, 0, 0], [1, 1, 1]]
            self.operation = 1
        elif start_level == 10:
            self.v = [[1, 0], [0, 1], [1, 0], [1, 1], [1, 1], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [1, 1], [1, 1]]
            self.h = [[1, 1, 1], [1, 1, 1], [1, 0, 1], [1, 0, 0], [1, 0, 0], [1, 1, 1]]
            self.v_start = [[1, 0], [0, 1], [1, 0], [1, 1], [1, 1], [1, 1], [0, 0], [1, 1], [0, 0], [1, 1], [1, 1], [1, 1]]
            self.h_start = [[1, 1, 1], [1, 1, 1], [1, 0, 1], [1, 0, 0], [1, 0, 0], [1, 1, 1]]
            self.operation = 1

        self.operation_start = self.operation
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
