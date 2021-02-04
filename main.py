# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtCore import QCoreApplication

import parsing
import configparser
from PyQt5.QtWidgets import (QDesktopWidget, QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QFileDialog,
                             QMessageBox, QPushButton, QRadioButton)

class MyApp(QWidget):
    def __init__(self): 
        super().__init__()
        self.grid = QGridLayout()

        self.xllocation = QLineEdit()
        self.dirlocation = QLineEdit()

        self.pstart = QLineEdit()
        self.pend = QLineEdit()

        self.prow = QLineEdit()
        self.pcol = QLineEdit()
        self.pwidth = QLineEdit()
        self.pheight = QLineEdit()

        self.xllocation.setMaximumWidth(395)
        self.dirlocation.setMaximumWidth(395)
        self.prow.setMaximumWidth(75)
        self.pcol.setMaximumWidth(75)
        self.pwidth.setMaximumWidth(75)
        self.pheight.setMaximumWidth(75)

        #초기 값 지정(config.ini에서 가져옴)
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
        self.pcol.setText(self.config['Settings']['column'])
        self.prow.setText(self.config['Settings']['row'])
        self.pwidth.setText(self.config['Settings']['width'])
        self.pheight.setText(self.config['Settings']['height'])
        self.pstart.setText(self.config['Settings']['start'])
        self.pend.setText(self.config['Settings']['end'])

        self.initUI()
        QMessageBox.information(self, "주의사항",
                                '1. 작업할 엑셀 파일을 반드시 백업해주세요.\r\n' \
                                '2. 엑셀파일이 실행중인 경우 오류가 발생합니다.\r\n' \
                                '3. 입력된 파싱 패턴을 찾지 못하면 내용이 저장되지 않습니다.\r\n'\
                                '4. UTF-8 타입의 텍스트 인코딩만 지원됩니다.\r\n')

    def initUI(self):
        self.setWindowTitle('InfraProject v1.0 by.Elbrown')

        #GridLayOut
        self.setLayout(self.grid)

        xlbtn = QPushButton('엑셀 파일 선택', self)
        dirbtn = QPushButton('텍스트 디렉토리 선택', self)
        self.grid.addWidget(xlbtn, 0, 0)
        self.grid.addWidget(dirbtn, 1, 0)

        # Label
        self.grid.addWidget(QLabel('파싱 시작 문자열 입력'), 2, 0)
        self.grid.addWidget(QLabel('파싱 종료 문자열 입력'), 3, 0)
        self.grid.addWidget(QLabel('셀 위치 열/행'), 2, 2)
        self.grid.addWidget(QLabel('셀 너비/높이'), 3, 2)

        #Edit버튼 붙이기
        self.grid.addWidget(self.xllocation, 0, 1, 1, 4)
        self.grid.addWidget(self.dirlocation, 1, 1, 1, 4)

        self.grid.addWidget(self.pstart, 2, 1)
        self.grid.addWidget(self.pend, 3, 1)

        self.grid.addWidget(self.pcol, 2, 3)
        self.grid.addWidget(self.prow, 2, 4)

        self.grid.addWidget(self.pwidth, 3, 3)
        self.grid.addWidget(self.pheight, 3, 4)

        #Button
        scbtn = QPushButton('설정저장', self)
        psbtn = QPushButton('파싱시작', self)
        oebtn = QPushButton('엑셀열기', self)
        closebtn = QPushButton('종료하기', self)

        self.grid.addWidget(scbtn, 4, 0)
        self.grid.addWidget(psbtn, 4, 1, 1, 2)
        self.grid.addWidget(oebtn, 4, 3)
        self.grid.addWidget(closebtn, 4, 4)

        #이벤트 연결
        scbtn.clicked.connect(self.saveConfig)
        xlbtn.clicked.connect(self.selectXl)
        dirbtn.clicked.connect(self.selectDir)
        psbtn.clicked.connect(self.parsing)
        oebtn.clicked.connect(self.openExcel)
        closebtn.clicked.connect(QCoreApplication.instance().quit)

        self.center()
        self.show()

    def selectXl(self):
        file_name = QFileDialog.getOpenFileName(self, "엑셀 파일 선택", "", "Excel Files (*.xlsx)")
        self.xllocation.setText(file_name[0])

    def selectDir(self):
        dir_name = QFileDialog.getExistingDirectory(self, "텍스트 파일 디렉토리 선택", "")
        self.dirlocation.setText(dir_name)

    def saveConfig(self):
        #현재 지정된 설정으로 옵션 변경
        self.config.set("Settings", "column", self.pcol.text())
        self.config.set("Settings", "row", self.prow.text())
        self.config.set("Settings", "width", self.pwidth.text())
        self.config.set("Settings", "height", self.pheight.text())
        self.config.set("Settings", "start", self.pstart.text())
        self.config.set("Settings", "end", self.pend.text())
        # parser에 내용을 추가 해 중 뒤에는 반드시 write 해줘야 함
        with open('./config.ini', "w") as fp:
            self.config.write(fp)
        QMessageBox.information(self, "메세지", '설정이 저장되었습니다.')

    def parsing(self):
        program=parsing.MyParsing()
        program.getTxt(self.dirlocation.text())
        program.initVal(self.pstart.text(),self.pend.text(), self.pcol.text(), self.prow.text(), self.pwidth.text(), self.pheight.text())
        if program.checkSheet(self.xllocation.text()):
            QMessageBox.critical(self, "메세지", '실행된 엑셀 파일을 종료해주세요.')
            return
        # Return 값에 따른 에러처리 1:텍스트파일에러, 2:파싱문자열에러, 3:인코딩에러
        val=program.writeCell(self.xllocation.text())
        if val==1:
            QMessageBox.warning(self, "에러메세지", '텍스트 파일 오픈 에러, 파일이 존재하는지 확인해주세요.')
            return
        elif val==2:
            QMessageBox.warning(self, "에러메세지", '시작/끝 파싱포인트가 매칭되지 않았습니다. 문자열 또는 정규표현식을 다시 확인해주세요.')
            return
        elif val==3:
            QMessageBox.warning(self, "에러메세지", 'UTF-8 텍스트 파일의 인코딩만 지원합니다.')
            return
        else:
            QMessageBox.information(self, "메세지", '작업이 완료되었습니다. 엑셀열기를 클릭해주세요.')

    def openExcel(self):
        os.system('start excel.exe "%s' %(self.xllocation.text(),))
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