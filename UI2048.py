# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from random import *
from math import pow
import sys

GRID_LEN = 4

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}

CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}

CELL_TEXT_DICT = {2: "35", 4: "35", 8: "35", 16: "35",
                  32: "35", 64: "35", 128: "33", 256: "33",
                  512: "33", 1024: "28", 2048: "28"}

FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = QtCore.Qt.Key_W
KEY_DOWN_ALT = QtCore.Qt.Key_S
KEY_LEFT_ALT = QtCore.Qt.Key_A
KEY_RIGHT_ALT = QtCore.Qt.Key_D

KEY_UP = QtCore.Qt.Key_Up
KEY_DOWN = QtCore.Qt.Key_Down
KEY_LEFT = QtCore.Qt.Key_Left
KEY_RIGHT = QtCore.Qt.Key_Right


class UiMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.matrix = []
        self.score = 0
        self.bestscore = 10
        for i in range(GRID_LEN):
            self.matrix.append([0]*GRID_LEN)

        self.commands = {KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right,
                         KEY_UP_ALT: up, KEY_DOWN_ALT: down, KEY_LEFT_ALT: left, KEY_RIGHT_ALT: right}
        # Setup Main Window
        self.setGeometry(300, 300, 250, 150)
        self.setFixedSize(550,685)
        self.setWindowTitle("Game 2048")
        self.setStyleSheet("background:rgb(250, 248, 239)")
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        # setup 2048 label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(25, 30, 150, 60))
        self.label.setText("2048")
        self.label.setStyleSheet("color:rgb(119,110,98);"
                                 "font:75 bold 36pt 'Arial';"
                                 "qproperty-alignment:center")
        # 设置当前分数Frame
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(280, 30, 100, 60))
        self.frame.setStyleSheet("background:rgb(187,173,160);\n" "border-radius:10px;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        # 设置Score显示
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(0, 8, 100, 20))
        self.label_2.setText("SCORE")
        self.label_2.setStyleSheet("color:rgb(238,228,218);""font:75 bold 14pt 'Arial';")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        # 设置Score数值显示
        self.scoreLabel = QtWidgets.QLabel(self.frame)
        self.scoreLabel.setGeometry(QtCore.QRect(0, 28, 100, 30))
        self.scoreLabel.setText(str(self.score))
        self.scoreLabel.setStyleSheet("color:rgb(255,255,255);""font:75 bold 20pt 'Arial';")
        self.scoreLabel.setAlignment(QtCore.Qt.AlignCenter)
        # 设置Best Fame
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(425, 30, 100, 60))
        self.frame_3.setStyleSheet("background:rgb(187,173,160);\n" "border-radius:10px;")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(0, 8, 100, 20))
        self.label_3.setText("BEST")
        self.label_3.setStyleSheet("color:rgb(238,228,218);""font:75 bold 14pt 'Arial'")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.bestScore = QtWidgets.QLabel(self.frame_3)
        self.bestScore.setGeometry(QtCore.QRect(0, 28, 100, 30))
        self.bestScore.setText(str(self.bestscore))
        self.bestScore.setStyleSheet("color:rgb(255,255,255);""font:75 bold 20pt 'Arial'")
        self.bestScore.setAlignment(QtCore.Qt.AlignCenter)
        # 设置简要说明
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(25, 115, 291, 30))
        self.label_6.setText("Join the Numbers and get the 2048 tile!")
        self.label_6.setStyleSheet("font: 13pt 'Arial';""color:rgb(119,110,98)")
        # 设置矩阵Frame
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(25, 160, 500, 500))
        self.frame_2.setStyleSheet("background:rgb(187, 173, 160);\n" "border-radius:10px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # 设置矩阵
        self.cellgrid = []
        for i in range(GRID_LEN):
            cellrow = []
            for j in range(GRID_LEN):
                cell = QtWidgets.QLabel(self.frame_2)
                cell.setGeometry(QtCore.QRect(20+120*i, 20+120*j, 100, 100))
                cell.setAlignment(QtCore.Qt.AlignCenter)
                cell.setStyleSheet("background:rgb(205,193,180);" "color:rgb(119,110,101);""font:75 35pt 'Arial'")
                cellrow.append(cell)
            self.cellgrid.append(cellrow)
        # 设置游戏结束
        self.endLabel = QtWidgets.QLabel(self.frame_2)
        self.endLabel.setGeometry(0, 0, 500, 500)
        self.endLabel.setText("Game Over!")
        self.endLabel.setStyleSheet("background:rgb(187, 173, 160, 160);"
                                    "color:rgb(119,110,98,180);font:bold 45pt 'Arial';")
        self.endLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.endLabel.setHidden(True)
        # 设置New Game按钮
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(425, 110, 100, 40))
        self.pushButton.setText("New Game")
        self.pushButton.setStyleSheet("font:75 bold 12pt 'Arial';\n""background:rgb(143,122,102);\n"
                                      "color:rgb(249,246,242);\n""border-radius:10px;")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.button_clicked)

        self.new_game()
        self.update_grid()
        self.setCentralWidget(self.centralwidget)
        self.show()

    def closeEvent(self, *args, **kwargs):
        print("closeCb called")

    def button_clicked(self):
        sender = self.sender()
        if sender == self.pushButton:
            self.new_game()
            self.update_grid()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key_W:
            if self.game_state() == 'not over':
                self.matrix, a, b = up(self.matrix)
                if a:
                    self.score += b
                    self.matrix_addnum()
                    self.update_grid()
                    if self.game_state() == 'lose':
                        self.endLabel.setText("Game Over!")
                        self.endLabel.setStyleSheet("background:rgb(187, 173, 160, 160);"
                                                    "color:rgb(119,110,98,180);font:bold 45pt 'Arial';")
                        self.endLabel.setAlignment(QtCore.Qt.AlignCenter)
                        self.endLabel.setHidden(False)
                    elif self.game_state() == 'win':
                        self.endLabel.setText("You Win!")
                        self.endLabel.setStyleSheet("background:rgb(187, 173, 160, 160);"
                                                    "color:rgb(237,194,46,180);font:bold 45pt 'Arial';")
                        self.endLabel.setAlignment(QtCore.Qt.AlignCenter)
                        self.endLabel.setHidden(False)
        elif e.key() == QtCore.Qt.Key_S:
            if self.game_state() == 'not over':
                self.matrix, a, b = down(self.matrix)
                if a:
                    self.score += b
                    self.matrix_addnum()
                    self.update_grid()
                    if self.game_state() == 'lose':
                        self.endLabel.setText("Game Over!")
                        self.endLabel.setStyleSheet("background:rgb(187, 173, 160, 160);"
                                                    "color:rgb(119,110,98,180);font:bold 45pt 'Arial';")
                        self.endLabel.setAlignment(QtCore.Qt.AlignCenter)
                        self.endLabel.setHidden(False)
                    elif self.game_state() == 'win':
                        self.endLabel.setText("You Win!")
                        self.endLabel.setStyleSheet("background:rgb(187, 173, 160, 160);"
                                                    "color:rgb(237,194,46,180);font:bold 45pt 'Arial';")
                        self.endLabel.setAlignment(QtCore.Qt.AlignCenter)
                        self.endLabel.setHidden(False)
        elif e.key() == QtCore.Qt.Key_A:
            if self.game_state() == 'not over':
                self.matrix, a, b = left(self.matrix)
                if a:
                    self.score += b
                    self.matrix_addnum()
                    self.update_grid()
                    if self.game_state() == 'lose':
                        self.endLabel.setText("Game Over!")
                        self.endLabel.setStyleSheet("background:rgb(187, 173, 160, 160);"
                                                    "color:rgb(119,110,98,180);font:bold 45pt 'Arial';")
                        self.endLabel.setAlignment(QtCore.Qt.AlignCenter)
                        self.endLabel.setHidden(False)
                    elif self.game_state() == 'win':
                        self.endLabel.setText("You Win!")
                        self.endLabel.setStyleSheet("background:rgb(187, 173, 160, 160);"
                                                    "color:rgb(237,194,46,180);font:bold 45pt 'Arial';")
                        self.endLabel.setAlignment(QtCore.Qt.AlignCenter)
                        self.endLabel.setHidden(False)
        elif e.key() == QtCore.Qt.Key_D:
            if self.game_state() == 'not over':
                self.matrix, a, b = right(self.matrix)
                if a:
                    self.score += b
                    self.matrix_addnum()
                    self.update_grid()
                    if self.game_state() == 'lose':
                        self.endLabel.setText("Game Over!")
                        self.endLabel.setStyleSheet("background:rgb(187, 173, 160, 160);"
                                                    "color:rgb(119,110,98,180);font:bold 45pt 'Arial';")
                        self.endLabel.setAlignment(QtCore.Qt.AlignCenter)
                        self.endLabel.setHidden(False)
                    elif self.game_state() == 'win':
                        self.endLabel.setText("You Win!")
                        self.endLabel.setStyleSheet("background:rgb(187, 173, 160, 160);"
                                                    "color:rgb(237,194,46,180);font:bold 45pt 'Arial';")
                        self.endLabel.setAlignment(QtCore.Qt.AlignCenter)
                        self.endLabel.setHidden(False)
        else:
            pass

    # 重新开始游戏
    def new_game(self):
        self.matrix = []
        for i in range(GRID_LEN):
            self.matrix.append([0]*GRID_LEN)
        for i in range(2):
            self.matrix_addnum()
        self.score = 0
        self.endLabel.setHidden(True)

    def update_grid(self):
        self.scoreLabel.setText(str(self.score))
        if self.bestscore < self.score:
            self.bestscore = self.score
            self.bestScore.setText(str(self.bestscore))
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                if self.matrix[i][j] != 0:
                    self.cellgrid[i][j].setText(str(self.matrix[i][j]))
                    self.cellgrid[i][j].setStyleSheet(
                        "background:"+BACKGROUND_COLOR_DICT[self.matrix[i][j]]+";"
                        "color:"+CELL_COLOR_DICT[self.matrix[i][j]]+";"
                        "font:"+CELL_TEXT_DICT[self.matrix[i][j]]+"pt 75 'Arial';")
                else:
                    self.cellgrid[i][j].setText("")
                    self.cellgrid[i][j].setStyleSheet("background:"+BACKGROUND_COLOR_CELL_EMPTY+";")

    def matrix_addnum(self):
        index = (randint(0, GRID_LEN-1), randint(0, GRID_LEN-1))
        while self.matrix[index[0]][index[1]] != 0:
            index = (randint(0, GRID_LEN-1), randint(0, GRID_LEN-1))
        self.matrix[index[0]][index[1]] = int(pow(2, randint(1, 2)))

    def game_state(self):
        for i in range(GRID_LEN):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == 2048:
                    return 'win'
        for i in range(GRID_LEN-1):  # intentionally reduced to check the row on the right and below
            for j in range(GRID_LEN-1):  # more elegant to use exceptions but most likely this will be their solution
                if self.matrix[i][j] == self.matrix[i+1][j] or self.matrix[i][j+1] == self.matrix[i][j]:
                    return 'not over'
        for i in range(GRID_LEN):  # check for any zero entries
            for j in range(GRID_LEN):
                if self.matrix[i][j] == 0:
                    return 'not over'
        for k in range(GRID_LEN-1):  # to check the left/right entries on the last row
            if self.matrix[GRID_LEN-1][k] == self.matrix[GRID_LEN-1][k+1]:
                return 'not over'
        for j in range(GRID_LEN-1):  # check up/down entries on last column
            if self.matrix[j][GRID_LEN-1] == self.matrix[j+1][GRID_LEN-1]:
                return 'not over'
        return 'lose'


def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new


def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new


def cover_up(mat):
    new = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    done = False
    for i in range(4):
        count = 0
        for j in range(4):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done


def merge(mat):
    score = 0
    done = False
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j+1] = 0
                score += mat[i][j]
                done = True
    return mat, done, score


def left(game):
        print("left")
        # return matrix after shifting up
        game = transpose(game)
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        game = transpose(game)
        return game, done, temp[2]


def right(game):
        print("right")
        game = reverse(transpose(game))
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        game = transpose(reverse(game))
        return game, done, temp[2]


def up(game):
        print("up")
        # return matrix after shifting left
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        return game, done, temp[2]


def down(game):
        print("down")
        # return matrix after shifting right
        game = reverse(game)
        game, done = cover_up(game)
        temp = merge(game)
        game = temp[0]
        done = done or temp[1]
        game = cover_up(game)[0]
        game = reverse(game)
        return game, done, temp[2]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UiMainWindow()
    sys.exit(app.exec_())
