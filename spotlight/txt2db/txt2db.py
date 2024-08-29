import glob
import time

import pandas as pd
import tqdm
import sqlalchemy
from abc import ABCMeta
from abc import abstractmethod

from spotlight.common import myFileDialog as myfd
from spotlight.txt2db.mod.dbcon import DbCon
from spotlight.txt2db.mod.df2db import Df2Db
from spotlight.common.protoSelector import ProtoABSSelector
from spotlight.import2df import Import2Df

#인터페이스
class ProtoTxt2Db(ProtoABSSelector, metaclass=ABCMeta):   
    
    objDbCon:DbCon
    objDf2Db:Df2Db
    
    #생성자
    @abstractmethod
    def __init__(self): pass #실행

    #데이터프레임 읽기
    @abstractmethod
    def _setDf(self): pass
    
    #DB연결
    @abstractmethod
    def _setDb(self): pass

    #Insert
    @abstractmethod
    def _insertDb(self): pass

class Txt2Db(ProtoTxt2Db): #have self.df

    bRealInsert:bool = True #기본은 직접입력
    
    def __init__(self, df:pd.DataFrame = None):
        if df is not None: 
            print("df가 전달되었습니다.")
            self.df = df

    def run(self) -> None:
        
        self._setBRealInsert()
        self._setDf()
        self._setDb()
        self._insertDb(self.bRealInsert)

    def _setBRealInsert(self) -> None:

        # 실제 데이터를 넣을것인지, 테이블구조만 생성할것인지
        msg = ""
        msg += "1. 실제 데이터 Insert(def) / 2. 테이블구조만 생성 \n"        
        print(msg)

        flag = input(">>") or "1"
        match(flag):
            case("1"): self.bRealInsert = True
            case("2"): self.bRealInsert = False    

    def _setDf(self) -> None:  
        if isinstance(self.df, pd.DataFrame):
            print("전달된 df를 insert합니다.")
        else:
            print("설정된 df가 없으므로 df를 읽어옵니다.")
            self.df = Import2Df().run() #타 모듈 활용        

    def _setDb(self):
        self.objDbCon = DbCon()
        self.objDf2Db = Df2Db(self.objDbCon)

    def _insertDb(self, bRealInsert:bool = True) -> None:
        if bRealInsert:
            self.objDf2Db.insert(self.df)
        elif not bRealInsert:
            self.objDf2Db.createTable(self.df)
