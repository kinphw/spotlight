import csv
from collections import defaultdict

from typing import TYPE_CHECKING
from typing import Optional
# from spotlight.import2df.import2df import Import2Df

class Import2DfInfo:

    type:int #Text or Excel
    TXT:int = 0
    PARQUET:int = 1
    PICKLE:int = 2
    EXCEL:int = 3

    sep:str = '\t'
    encod:str = 'cp949'
    # bQuote:bool = True
    intQuote:int = 0
    dtype:defaultdict | str = 'string'
    flagModin:bool = False
    intHeader:Optional[int] = True #240825

    bSetInfo:bool = False

    def __init__(self):
        pass
        # 당 객체 생성자에서 직접 호출하지 않고 호출하는 모객체에서 필요에 따라 호출하도록 함
        # self.setType()
        # self.setInfo()

    def setType(self) -> bool: #설정했으면 True, 아니면 False        
        help = "1. import txt\n"
        help += "2. import parquet\n"
        help += "3. import pickle\n"
        help += "4. import Excel\n"
        help += "5. quit\n"      
        print(help)
        flag:str = input(">>")
        
        while True:
            match(flag):
                case '1': self.type = self.TXT
                case '2': self.type = self.PARQUET
                case '3': self.type = self.PICKLE
                case '4': self.type = self.EXCEL
                case '5': return False
                case _: print("Wrong input"); continue
            return True
    
    def setInfo(self):

        if self.bSetInfo: return

        if self.type == self.TXT:
            self.sep = input("Seperator? (기본값 \\t)>>") or '\t'
            
            self.encod = input("인코딩? (cp949)>>") or 'cp949'
            
            flag = input("헤더가 있습니까? (Y/N, 기본값 Y)") or 'Y'
            if flag == 'Y': self.intHeader = 0
            else: self.intHeader = None
            
            #240215
            flag = input("quote(\")를 사용합니까? (Y/N, 기본값 Y)")
            if flag == 'Y': self.intQuote = csv.QUOTE_MINIMAL
            elif flag == 'N': self.bQuote = csv.QUOTE_NONE
            else: print("선택하지 않았습니다. quote를 사용합니다."); self.intQuote = csv.QUOTE_MINIMAL

            #240529
            self.dtype = self._setDType()

        ## MODIN 활용부
        flagTmp:str = input("USE MODIN? MODIN doesn't support chunksize (DEFAUT : N)>>") or 'N'
        if flagTmp == 'Y': self.flagModin = True
        else: self.flagModin = False

        self.bSetInfo = True #한번 세팅하면 True로 flag 변경        
        # return self

    # 선택에 따라 dtype을 반환받아 read_csv메서드의 dtype 인수에 적용하는 함수
    def _setDType(self) -> defaultdict | str :
        flag:str = input("dtype을 사전 지정합니까?(1 지정하지 않음(def : string으로 처리) / 2 지정함(for sy))>>")
        if flag == "": flag='1'
        while True:
            match flag:
                case '1':
                    return 'string'
                case '2':
                    return defaultdict(lambda:'string'
                            , HKONT="int64"
                            , WRBTR="float64"
                            , DMBTR="float64"
                            , BELNR="int64")
                case _:
                    print("잘못 입력하였습니다.")
                    continue        