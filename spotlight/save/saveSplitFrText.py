import tqdm
import pathlib

from spotlight.common.ErrRetry import ErrRetryF
#from spotlight.save.saveSplit import SaverSplit
import spotlight.common.myFileDialog as myfd
from spotlight.common.common import mapcount

@ErrRetryF
class SaverSplitFrText(): #직접 읽어서 분할해서 저장 (왜? Pandas로 인한 데이터 변환효과를 배제하기 위해)

    _filename:str    
    _interval:int

    _txtEncod:str
    _txtSep:str
    _txtHeader:str    

    _flagHeader:bool


    def __init__(self): #OVERIDE
        self._filename = myfd.askopenfilename("text file to split:")
        self._txtEncod = input("인코딩? (cp949 등, 기본값 utf8)>>") or 'utf8'
        self._totalSize = mapcount(self._filename, self._txtEncod) # 전체 행수이므로 -1하지 않는다.

    def run(self):
        self._setInfo() #기본정보 설정  
        self._splitter()

    def _setInfo(self): # OVERIDE    

        #Set Interval
        while True:
            flag = input("추출할 크기를 지정하세요(기본값 1,000,000) >>") or '1000000'
            if not flag.isdigit(): print("숫자를 입력하세요."); continue
            else: self._interval = int(flag); break
        flag = input("HEADER가 존재합니까? >>")
        match flag:
            case 'Y':
                self._getHeader()
                self._flagHeader = True
            case _: self._flagHeader = False

    def _splitter(self): #OVERIDE

        pbar = tqdm.tqdm(total=self._totalSize, desc='Save')
        
        fIn = open(self._filename, mode="rt", encoding=self._txtEncod)
        
        cntLine = 0 #line numbering        
        cntFile = 0 #save file numbering
        cntData = 0 #line(data) numbering

        filenameOut = pathlib.Path(self._filename).stem

        fOut = open(filenameOut + "_" + str(cntFile) + ".txt", mode="at", encoding=self._txtEncod) #일단 처음에 연다
        
        while True:
            txtLine = fIn.readline()

            if not txtLine: fOut.close();break #없으면 순환을 끝낸다
            
            # 파일교체부
            if cntLine == 0 or cntLine == 1: pass #처음엔 파일교체 pass
            elif cntData % self._interval == 0:
                fOut.close()
                cntFile += 1
                fOut = open(filenameOut + "_" + str(cntFile) + ".txt", mode="at", encoding=self._txtEncod)
                if self._flagHeader: fOut.write(self._txtHeader)                        

            fOut.write(txtLine)
            if not(cntLine == 0 and self._flagHeader): cntData += 1 #첫째줄이고 헤더가 있는경우가 아니라면            
            cntLine += 1            
            pbar.update(1)

        fIn.close()
        pbar.close()

    def _getHeader(self):
        f = open(self._filename, mode="rt", encoding=self._txtEncod)
        self._txtHeader = f.readline()
        print("HEADER:", self._txtHeader)
        f.close()

if __name__=='__main__':
    SaverSplitFrText().run()