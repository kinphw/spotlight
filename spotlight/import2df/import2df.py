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
from spotlight.import2df.importBody import ImportBody

#단일책임원칙을 구현하기 위해 정보설정은 import2dfinfo로 분리
#실제로 파일을 읽는 부분은 importBody로 분리
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
        
        return ImportBody(self).run() #단일책임원칙을 위반하지 않기 위해 별도의 클래스로 분리

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

    # def _importWrapper(self) -> pd.DataFrame:        
    #     return ImportBody(self).run() #단일책임원칙을 위반하지 않기 위해 별도의 클래스로 분리

if __name__=='__main__':
    Import2Df().run()