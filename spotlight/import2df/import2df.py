import csv

import pandas as pd
import modin.pandas as mpd #240117
import tqdm
import ray
from collections import defaultdict
from typing import Optional

import spotlight.common.myFileDialog as myfd
from spotlight.common.ErrRetry import ErrRetryF
from spotlight.common.common import mapcount
from spotlight.import2df.import2dfInfo import Import2DfInfo

class Import2Df:    

    objInfo:Import2DfInfo
    msg:Optional[str]
    path:str
    bPBar:bool = True
    bPreSet:bool = False #1회용이 아니라 객체를 사전설정할 경우 사용하는 bool변수. 만약 True인 경우에는 생성자에서 _setInfo()를 설정함

    def __init__(self, bPBar:bool = True, bPreSet:bool = False):
        self.objInfo = Import2DfInfo() #최초 인스턴스 생성할때 세팅. 재활용할때는 설정이 불필요
        self.bPBar = bPBar
        if bPreSet: 
            self.bPreSet = True
            if not self._setType(): return #사전설정이 필요한 경우
            self._setInfo() #사전설정이 필요한 경우

    def run(self, msg:str = None, path:Optional[str] = None) -> pd.DataFrame | None:
        if not self.bPreSet:
            if not self._setType(): return #생성자에서 설정했으므로 run()에서는 호출하지 않음

        self._setMsg(msg)
        self._setPath(path)
        if self.path == '': return None #파일선택이 없으면 None 반환하여 종료       

        if not self.bPreSet:            
            self._setInfo() #생성자에서 설정했으므로 run()에서는 호출하지 않음
        
        return self._importWrapper() #실제 호출부

    def _setMsg(self, msg:Optional[str]) -> None:
        #msg 세팅부        
        if msg is None: #msg가 없으면 생성
            msg = " 파일을 선택하세요."
            match(self.objInfo.type):
                case Import2DfInfo.TXT: msg = "Text" + msg                
                case Import2DfInfo.PARQUET: msg = "Parquet" + msg                
                case Import2DfInfo.PICKLE: msg = "Pickle" + msg                
                case Import2DfInfo.EXCEL: msg = "Excel" + msg           
        self.msg = msg

    #@ErrRetryF
    def _setPath(self, path:Optional[str]) -> None:  #이 부분은 무조건 호출하면 다시 작동함     
        if path is None:
            self.path = myfd.askopenfilename(self.msg)
        else:
            self.path = path

    def _setInfo(self):
        self.objInfo.setInfo()

    def _setType(self) -> bool: #나가기를 누르면 False, 아니면 True
        return self.objInfo.setType()

    def _importWrapper(self) -> pd.DataFrame:        
        match(self.objInfo.type):
            case Import2DfInfo.TXT: return self._importTxt(self.path)
            case Import2DfInfo.PARQUET: return self._importParquet(self.path)
            case Import2DfInfo.PICKLE: return self._importPickle(self.path)
            case Import2DfInfo.EXCEL: return self._importExcel(self.path)            

    ############################            

    @ErrRetryF
    def _importTxt(self, path:str, chunksize:int = 10000000) -> pd.DataFrame:    
        
        if self.objInfo.flagModin: #MODIN을 쓸 때
            if not ray.is_initialized(): ray.init()
            # if self.objInfo.bQuote:
            #     df = mpd.read_csv(path, sep=self.objInfo.sep, encoding=self.objInfo.encod, dtype=self.objInfo.dtype, header=self.objInfo.intHeader) #, low_memory=False)#, chunksize=chunksize) #240119 
            # else: 
            df = mpd.read_csv(path, 
                              sep=self.objInfo.sep, 
                              encoding=self.objInfo.encod, 
                              quoting=self.objInfo.intQuote, 
                              dtype=self.objInfo.dtype, 
                              header=self.objInfo.intHeader) #, low_memory=False)#, chunksize=chunksize) #240119
            df = df._to_pandas() #다시 pd.DataFrame으로 변경
        else:
            cnt = mapcount(path,self.objInfo.encod) -1 #Count Check _ Column 때문에 1을 빼야 함
            if self.bPBar: pbar = tqdm.tqdm(total=cnt, desc='Read')        
            df = pd.DataFrame()        
            
            # if self.objInfo.bQuote: 
            #     dfReader = pd.read_csv(path, sep=self.objInfo.sep, encoding=self.objInfo.encod, low_memory=False, chunksize=chunksize, dtype=self.objInfo.dtype, header=self.objInfo.intHeader)            
            # else: 
            dfReader = pd.read_csv(path, 
                                   sep=self.objInfo.sep, 
                                   encoding=self.objInfo.encod, 
                                   low_memory=False, 
                                   chunksize=chunksize, 
                                   quoting=self.objInfo.intQuote, 
                                   dtype=self.objInfo.dtype, 
                                   header=self.objInfo.intHeader)  #240131 #240214
            for count, chunk in enumerate(dfReader):
                df = pd.concat([df, chunk])
                if self.bPBar: pbar.update(chunk.shape[0])        
            if self.bPBar: pbar.close()
            if cnt != df.shape[0]: print("raw text rows와 dataframe records count가 상이합니다. 주의하세요.(QUOTE때문일 수 있음)") #240131
        return df

    def _importParquet(self, path:str) -> pd.DataFrame:       
        return pd.read_parquet(path)

    def _importPickle(self, path:str) -> pd.DataFrame:        
        return pd.read_pickle(path)

    def _importExcel(self, path:str) -> pd.DataFrame:

        if self.objInfo.flagModin:
            df:mpd.DataFrame = mpd.read_excel(path)
            return df._to_pandas()
        else:
            return pd.read_excel(path)

if __name__=='__main__':
    Import2Df().run()