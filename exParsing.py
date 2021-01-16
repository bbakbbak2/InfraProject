# -*- coding: utf-8 -*-
import codecs
import os
import sys

import xlsxwriter
import glob

from xlsxwriter.exceptions import FileCreateError


class MyParsing:
    def __init__(self):
        super().__init__()
        self.wrkshtList = []  # 워크시트 배열
        self.contentList = []  # 파싱포인트 배열
        self.workbook = xlsxwriter.Workbook('result.xlsx')
        self.wrap_format1 = None
        self.start = ""
        self.end = ""
        self.start2 = ""
        self.end2 = ""
        self.col = 100
        self.row = 50

    def initCell(self, start, end, row, col, start2=None, end2=None):
        self.wrap_format1 = self.workbook.add_format({'text_wrap': True})
        self.wrap_format1.set_align('vcenter')
        self.start = start
        self.end = end
        self.row = row
        self.col = col
        print("초기화:"+ start + " " + end) #디버그코드

        if start2 != None and end2 != None:
            self.wrap_format2 = self.workbook.add_format({'text_wrap': True})
            self.wrap_format2.set_align('vcenter')
            self.start = start
            self.end = end
            self.start2 = start2
            self.end2 = end2

    # FH는 파일핸들러
    def makeCell(self, FH, worksheet):
        row=0
        # 파일의 내용을 라인 단위로 리스트에 저장
        #Standard_START, Standard_END
        findPoint=False
        for line in FH:
            if line.find(self.start) >= 0:
                findPoint=True
            if findPoint:
                self.contentList.append(line)

            # End문구를 찾았을 때, 리스트에 기록된 내용을 시트에 저장
            if line.find(self.end) >= 0:
                # 첫번째, 마지막에 기록된 파싱문구를 지워서 최적화한다.
                try:
                    self.contentList.pop(0)
                    self.contentList.pop(-1)
                    # 저장한 리스트를 실제로 셀에 기록 앞에 첫 두 값은 기록되는 위치
                    worksheet.write(row, 0, ' '.join(self.contentList), self.wrap_format1)
                except FileCreateError:
                    print("엑셀 파일이 열려있음")
                except IndexError:
                    pass

                # 리스트 초기화, 다음 엑셀 행 반복
                self.contentList = []
                findPoint = False
                row+=1
        print("시트 완성")



    def makeSheet(self):
        print("워크시트 생성")
        #텍스트에 따른 워크시트 생성
        for sheetName in self.wrkshtList:
            # 시트 이름에서 .txt는 제거 후 생성
            worksheet = self.workbook.add_worksheet(sheetName.rstrip('.txt'))
            # worksheet.set_default_row(130)
            worksheet.set_column(0, 0, self.col)
            try:
                # 텍스트 파일을 연다. UTF-8로 인코딩 된 텍스트 파일만 불러올 수 있다.
                FH = codecs.open(sheetName, 'r', 'utf-8')
                # 생성된 워크시트에 데이터 저장함수 호출
                self.makeCell(FH, worksheet)

            except IOError:
                print("can't open file")
        #모든 시트 기록 후 close.
        self.workbook.close()
        FH.close()
        #결과 엑셀 자동실행
        os.system('start excel.exe "%s\\result.xlsx"' % (sys.path[0],))


    def getTxt(self):
        # 현재 디렉토리 파일 목록 획득, 텍스트 파일만 추출하기
        txtList = []
        fileList = glob.glob('*')
        for fl in fileList:
            if fl.find('.txt') > 0:
                txtList.append(fl)
        self.wrkshtList = txtList
        print("존재하는 텍스트 리스트: "+ str(self.wrkshtList))

