import glob
import time

import pandas as pd
import tqdm
import sqlalchemy

from spotlight.common import myFileDialog as myfd
from spotlight.txt2db.mod.dbcon import DbCon
from spotlight.txt2db.mod.txt2df import Txt2Df
from spotlight.txt2db.mod.df2db import Df2Db

class Txt2Db():

    path : str
    listFiles : list

    objEngine : sqlalchemy.Engine

    #읽어서 넣기 위한 정보들
    strEncod:str
    strSep:str
    strTableName:str
    bHeader:bool
    intChunksize:int

    def run(self):                
        self.path = myfd.askdirectory() #폴더를 input 받는다.        
        self.checkFiles() #폴더 내 텍스트 배열을 인식한다.
        self.setInfo()
        
        timeStart = time.time()
        self.importAndInsert() #파일을 순환 : import / insert
        print(time.time() - timeStart, "초 소요")

    def checkFiles(self):
        ext = input("확장자(기본값, tsv)>>") or 'tsv'
        self.listFiles = glob.glob(self.path+'/*.'+ext)
        print(self.listFiles)

    def setInfo(self):
        self.strEncod = input("ENCODING(기본 UTF8)>>") or 'utf8'
        self.strSep = input("SEPERATOR(기본 \\t)>>") or '\t'
        self.strTableName = input("Table Name>>")
        self.bHeader = (input("text have header? (Y/N)>>") == 'Y')
        self.intChunksize= int(input("chunksize(기본 500,000)>>") or '500000')
    
    def importAndInsert(self):
        self.objEngine = DbCon().connect() #DB 연결

        pbar = tqdm.tqdm(total=len(self.listFiles))
        objT2D = Txt2Df() #create object to import textfile
        objD2D = Df2Db(self.objEngine)

        i = 0
        for file in self.listFiles: #파일을 순환하면서,
            pbar.set_description(file)

            df = objT2D.run(file, self.strSep, self.strEncod, self.bHeader, self.intChunksize) #IMPORT
            
            objD2D.insert(df, self.strTableName) #and insert
            
            pbar.update(1)          
            # i += 1
            # if i == 1: print("DEBUG END"); break
        
        pbar.close()

def runTxt2Db(): #CALLER
    Txt2Db().run()
