import glob

import pandas as pd
import tqdm

from spotlight.txt2db import Txt2Db
from spotlight.common import myFileDialog as myfd
from spotlight.import2df import Import2Df

class Txt2DbMulti(Txt2Db):
    
    listFiles : list = []

    #Override
    #여러 파일을 인식. 테이블 구조 분기는 불필요함
    def run(self) -> None:
        #self._setBRealInsert()
        self._setTargetFiles() #추가구현
        self._setDb()
        self._loop() #추가구현
        # self._setDf()
        # self._insertDb(self.bRealInsert) 

    ################################

    def _setTargetFiles(self) -> None:
        strFolder = myfd.askdirectory() #폴더를 input 받는다.    
        self._checkFiles(strFolder)

    def _checkFiles(self, strFolder:str) -> None:
        ext = input("확장자(기본값, tsv)>>") or 'tsv'
        self.listFiles = glob.glob(strFolder+'/*.'+ext)
        print(self.listFiles)

    def _loop(self) -> None:        
        
        objImport2Df = Import2Df(bPBar=False, bPreSet=True) #내부 pbar는 끈다.
        
        pbar = tqdm.tqdm(total=len(self.listFiles))
        i = 0
        for file in self.listFiles:            
            file:str
            
            pbar.set_description(file)
            
            self.df = objImport2Df.run(path = file)
            self.objDf2Db.insert(self.df, bPBar = False) #외부 pbar를 위해 내부 pbar는 끈다.
            
            pbar.update(1)                      
        pbar.close()