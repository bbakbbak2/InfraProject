# -*- coding: utf-8 -*-
import os
import sys
import exParsing
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDesktopWidget, QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit,
                             QPushButton, QCheckBox)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.cb = QCheckBox('Extend Parsing', self)
        self.pstart1 = QLineEdit()
        self.pend1 = QLineEdit()
        self.pstart2 = QLineEdit()
        self.pend2 = QLineEdit()

        self.pcolumn1 = QLineEdit()
        self.pwidth1 = QLineEdit()
        self.pcolumn2 = QLineEdit()
        self.pwidth2 = QLineEdit()

        self.pcolumn1.setText("0")
        self.pwidth1.setText("50")
        self.pcolumn2.setText("1")
        self.pwidth2.setText("50")

        self.pstart1.setText("TEST_START")
        self.pend1.setText("TEST_END")
        self.pstart2.setText("TEST_START")
        self.pend2.setText("TEST_END")

        self.initUI()
        self.pcount=1

    def initUI(self):
        #GridLayOut
        self.setLayout(self.grid)
        self.cb.stateChanged.connect(self.extend)
        self.grid.addWidget(self.cb, 0, 0)
        #Label
        self.grid.addWidget(QLabel('Parsing START-1:'), 1, 0)
        self.grid.addWidget(QLabel('Parsing END-1:'), 2, 0)
        self.grid.addWidget(QLabel('열 위치:'), 1, 2)
        self.grid.addWidget(QLabel('열 너비:'), 2, 2)

        #Edit버튼 붙이기
        self.grid.addWidget(self.pstart1, 1, 1)
        self.grid.addWidget(self.pend1, 2, 1)
        self.grid.addWidget(self.pcolumn1, 1, 3)
        self.grid.addWidget(self.pwidth1, 2, 3)

        #Button
        btn1 = QPushButton('상태저장', self)
        btn2 = QPushButton('파싱시작', self)
        btn3 = QPushButton('종료', self)

        self.grid.addWidget(btn1, 5, 0)
        self.grid.addWidget(btn2, 5, 1)
        self.grid.addWidget(btn3, 5, 2)

        btn2.clicked.connect(self.parsing)

        self.center()
        self.show()

    def extend(self, state):
        if state == Qt.Checked:
            print("체크됨")
            self.pcount=2 #두개를 파싱함
            self.grid.addWidget(QLabel('Parsing START-2:'), 3, 0)
            self.grid.addWidget(QLabel('Parsing END-2:'), 4, 0)
            self.grid.addWidget(QLabel('열 위치:'), 3, 2)
            self.grid.addWidget(QLabel('열 너비:'), 4, 2)
            self.grid.addWidget(self.pstart2, 3, 1)
            self.grid.addWidget(self.pend2, 4, 1)
            self.grid.addWidget(self.pcolumn2, 3, 3)
            self.grid.addWidget(self.pwidth2, 4, 3)
            self.show()
        else:
            print("체크해지됨")
            self.pcount=1

    def saving(self):
        return

    def parsing(self):
        print("값 전달")
        program=exParsing.MyParsing()
        program.getTxt()
        program.makeSheet()

        program.initCell(self.pstart1.text(), self.pend1.text(), int(self.pcolumn1.text()), int(self.pwidth1.text()))
        program.writeCell()

        if self.pcount == 2:
            # 두개일 떄, 진행
            program.initCell(self.pstart2.text(), self.pend2.text(), int(self.pcolumn2.text()),
                             int(self.pwidth2.text()))
            return
        #결과 엑셀 자동실행
        os.system('start excel.exe "%s\\result.xlsx"' % (sys.path[0],))


    def exiting(self):
        return

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())