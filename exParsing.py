# -*- coding: utf-8 -*-
import codecs
import xlsxwriter
import glob
import openpyxl
# xlsxwriter는 읽기,수정 기능이 없는 라이브러리라서 openpyxl라는 다른 라이브러리를 사용해야함 ㅠㅠㅠ

from xlsxwriter.exceptions import FileCreateError


class MyParsing:
    def __init__(self):
        super().__init__()
        self.wrkshtList = []  # 워크시트 배열
        self.workbook = xlsxwriter.Workbook('result.xlsx')
        self.wrap_format = self.workbook.add_format({'text_wrap': True})
        self.wrap_format.set_align('vcenter')
        self.start = ""
        self.end = ""
        self.column = 0
        self.width = 0

    def initCell(self, start, end, column, width):
        self.start = start
        self.end = end
        self.column = column
        self.width = width
        print("초기화:"+ start + " " + end + " " + str(column) + " " + str(width)) #디버그코드

    # FH는 파일핸들러
    def writeCell(self, extend=False):
        FH = None
        for worksheet in self.wrkshtList:
            try:
                # 텍스트 파일을 연다. UTF-8로 인코딩 된 텍스트 파일만 불러올 수 있다.
                FH = codecs.open(worksheet, 'r', 'utf-8')
                objSheet = self.workbook.add_worksheet(worksheet.rstrip('.txt'))
            except IOError:
                print("can't open file")

            contentList = []  # 파싱포인트 배열
            rows=0
            # 파일의 내용을 라인 단위로 리스트에 저장
            #Standard_START, Standard_END
            findPoint=False
            for line in FH:
                print(line+"\r\n")
                if line.find(self.start) >= 0:
                    findPoint=True
                if findPoint:
                    contentList.append(line)

                # End문구를 찾았을 때, 리스트에 기록된 내용을 시트에 저장
                if line.find(self.end) >= 0:
                    # 첫번째, 마지막에 기록된 파싱문구를 지워서 최적화한다.
                    try:
                        contentList.pop(0)
                        contentList.pop(-1)
                        # 저장한 리스트를 실제로 셀에 기록 앞에 첫 두 값은 기록되는 위치를 정의
                        objSheet.write(rows, 0, ' '.join(contentList), self.wrap_format)
                    except FileCreateError:
                        print("엑셀 파일이 열려있음")
                    except IndexError:
                        pass
                    # 리스트 초기화, 다음 엑셀 행 반복
                    contentList = []
                    findPoint = False
                    rows+=1
        #모든 시트 기록 후 자원 반납
        self.workbook.close()
        FH.close()
        print("시트 완성")


    def makeSheet(self):
        print("워크시트 생성")
        #텍스트에 따른 워크시트 생성
        for sheetName in self.wrkshtList:
            # 시트 이름에서 .txt는 제거 후 생성
            worksheet = self.workbook.add_worksheet(sheetName.rstrip('.txt'))
            #worksheet.set_column(1, 0, self.width)#width
            worksheet.write(0, 0, '', self.wrap_format)     # 시트만 생성, 반납은 셀 생성과정에서 진행
        self.workbook.close()                               #종료코드가 있어야 생성됨

    def getTxt(self):
        # 현재 디렉토리 파일 목록 획득, 텍스트 파일만 추출하기
        txtList = []
        fileList = glob.glob('*')
        for fl in fileList:
            if fl.find('.txt') > 0:
                txtList.append(fl)
        self.wrkshtList = txtList
        print("존재하는 텍스트 리스트: "+ str(self.wrkshtList))

