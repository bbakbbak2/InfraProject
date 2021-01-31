# -*- coding: utf-8 -*-
import os
import openpyxl
from openpyxl.styles import Alignment
import re

class MyParsing:
    def __init__(self):
        super().__init__()
        self.txtList = []  # 텍스트 배열
        self.wsList = []  # 워크시트명 배열
        self.start = ""
        self.end = ""
        self.col = 0
        self.row = 0
        self.dir = ""

    def initVal(self, start, end, col, row, width, height):
        self.start = start
        self.end = end
        self.col = col
        self.row = row
        self.width = width
        self.height = height

    # FH는 파일핸들러
    def writeCell(self, filename):
        stcol = self.col
        strow = self.row

        wb = openpyxl.load_workbook(filename)
        FH = None
        # 워크시트 별로 작업 진행
        for wsname in self.txtList:
            try:
                # 텍스트 파일을 연다. UTF-8로 인코딩 된 텍스트 파일만 불러올 수 있다.
                FH = open(self.dir+"/"+wsname, 'r', encoding='utf-8')
            except IOError:
                print("텍스트 오픈 에러")

            # 워크시트 선택, 세부설정
            # ws = wb.active active는 첫번째 워크시트를 선택하는 코드임
            ws = wb.get_sheet_by_name(os.path.splitext(wsname)[0])
            ws.column_dimensions[stcol].width = self.width

            # 정규표현식 셋팅
            pstart = re.compile(self.start)
            pend = re.compile(self.end)

            #텍스트 내용 가져오기
            contentList = []        #파싱포인트 배열
            nextcell = int(strow)   #셀 행 구분
            # 파일의 내용을 라인 단위로 리스트에 저장  Standard_START, Standard_END
            findPoint = False
            for line in FH:
                if pstart.search(line) != None:
                    findPoint = True
                #시작 포인트 찾았을때, 엔드포인트 진행
                if findPoint:
                    #print("파싱 포인트를 찾았습니다.")
                    #print("일치하는 라인: %s" %line)
                    contentList.append(line)
                     # End 문구를 찾았을 때, 리스트에 기록된 내용을 시트에 저장
                    if pend.search(line) != None:
                        # 첫번째, 마지막에 기록된 파싱문구를 지워서 최적화한다.
                        contentList.pop(0)
                        contentList.pop(-1)

                        # 셀에 데이터 기록
                        ws.row_dimensions[nextcell].height = self.height
                        ws[stcol + str(nextcell)].alignment = Alignment(vertical='top', wrap_text=True)
                        try:
                            ws[stcol+str(nextcell)] = "".join(contentList)
                        # badcharacters 에러 이슈가 있었음
                        except openpyxl.utils.exceptions.IllegalCharacterError:
                            pass

                        # 리스트 초기화, 다음 엑셀 행 반복
                        contentList = []
                        findPoint = False
                        nextcell += 1
        # 모든 시트 기록 후 자원 반납
        wb.save(filename)
        FH.close()

    def checkSheet(self, filename):
        wb = openpyxl.load_workbook(filename)
        # wb.get_sheet_names() 모든 워크시트 이름 가져오기
        for wsname in self.wsList:
            try:
                ws = wb[wsname]         # 워크시트가 존재함
            except KeyError:            # 존재하지 않을 경우 새로 생성
                ws = wb.create_sheet()
                ws.title = wsname
            finally:
                wb.save(filename)

    def getTxt(self, dir):
        # 현재 디렉토리 파일 목록 획득, 텍스트 파일만 추출하기
        self.dir = dir
        fileList = os.listdir(dir)
        for file in fileList:
            if file.find('.txt') > 0:
                self.txtList.append(file)
                # 확장자 제거
                self.wsList.append(os.path.splitext(file)[0])