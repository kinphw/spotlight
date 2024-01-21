import tqdm

import pandas as pd
import modin.pandas as mpd

from spotlight.common.protoSelector import ProtoABSSelector
from spotlight.common.ErrRetry import ErrRetryF

@ErrRetryF
class SaverSplit(ProtoABSSelector): #분할해서 저장

    # df:pd.DataFrame
    mdf:mpd.DataFrame

    # def __init__(self, df:pd.DataFrame):
    #     self.df = df

    _filename:str
    _flagOutput:bool #True : Excel, False : Text
    _interval:int
    _flagModin:bool

    _txtEncod:str
    _txtSep:str

    _USETEXT:bool = True
    _USEEXCEL:bool = False

    def run(self):
        self._setInfo() #기본정보 설정  
        self._splitter()

    def _setInfo(self):
        
        self._filename = input("저장할 filename을 지정하세요(기본값 result)>>") or 'result'
        
        #추출형식 지정부
        msg = "1. Save to Text\n"
        msg += "2. Save to excel\n"   
        print(msg)
        flag = input(">>")
        match(flag):
            case '1':
                self._txtEncod = input("인코딩? (cp949 등, 기본값 utf8)>>") or 'utf8'
                self._txtSep = input("Seperator? (기본값 \\t)") or '\t'

                self._killLFT()
                self._flagOutput = self._USETEXT
            case '2': self._flagOutput = self._USEEXCEL
            case _: print("Wrong enter")

        #Set Modin
        flag = input("Use Modin? (기본값 N)>>") or 'N'  
        while True:
            match(flag):
                case 'Y': 
                    self.mdf = mpd.DataFrame(self.df)
                    self._flagModin = True ; break
                case 'N': self._flagModin = False ; break
                case _: print("Wrong enter")

        #Set Interval
        while True:
            flag = input("추출할 크기를 지정하세요(기본값 1,000,000) >>") or '1000000'
            if not flag.isdigit(): print("숫자를 입력하세요."); continue
            else: self._interval = int(flag); break

    def _splitter(self): #분할

        pbar = tqdm.tqdm(total=self.df.shape[0], desc='Save')
        
        lineStart = 0
        chunksize = self._interval
        i = 0 #for filename
        while True:
            lineEnd = min(lineStart + chunksize, self.df.shape[0]) #마지막 줄. 데이터프레임보다 크면 안되니 검증식 구현
            length = lineEnd - lineStart #size of one chunk

            if self._flagModin: df = self.mdf.iloc[lineStart:lineEnd, :]
            else: df = self.df.iloc[lineStart:lineEnd, :]

            if self._flagOutput == self._USETEXT:
                filename = self._filename + "_" + str(i) + ".txt"
                self._saveText(df, filename)

            elif self._flagOutput == self._USEEXCEL:
                filename = self._filename + "_" + str(i) + ".xlsx"
                self._saveExcel(df, filename)

            pbar.update(length)
            lineStart += length
            i += 1 # for filename
            
            if lineEnd >= self.df.shape[0]: break

    def _saveText(self, df:pd.DataFrame|mpd.DataFrame, filename:str):        
        df.to_csv(index=False, sep=self._txtSep, encoding=self._txtEncod, path_or_buf=filename)

    def _saveExcel(self, df:pd.DataFrame, filename:str):
        if self._flagModin:            
            df._to_pandas().to_excel(filename, index=None)
        else: df.to_excel(filename, index=None)    

    def _killLFT(self):
        print("text 추출시 오류를 피하기 위해 모든 개행문자와 탭문자를 제거합니다.")
        self.df.replace('[\n]', '', regex=True)
        self.df.replace('[\t]', '', regex=True)
        print("제거완료")

if __name__=='__main__':
    SaverSplit(pd.read_csv("test.txt", encoding='utf8', sep=',')).run()