from typing import Optional
import tqdm
import pandas as pd
import pymysql
import sqlalchemy
pymysql.install_as_MySQLdb()
# import MySQLdb    
# import pyodbc

import spotlight.common.myFileDialog as myfd
from spotlight.txt2db.mod.dbcon import DbCon

class Df2Db:
    
    objDbCon : DbCon
    strTableName : Optional[str] = None

    def __init__(self, objDbCon:DbCon, tableName:Optional[str] = None):
        self.objDbCon = objDbCon
        print("Engine connected")
        self._setTableName(tableName)     

    def _setTableName(self, tableName:Optional[str]) -> None:
        if tableName is None:
            self.strTableName = input("Table Name? (DBMS)>>")
        else:
            self.strTableName = tableName

    def insert(self, df : pd.DataFrame, chunksize=1000000, bPBar:bool = True) -> None: #insert dataframe to db # chunksize : 1백만. 이거보다 적으면 느려짐
        tgtNo = df.shape[0] #rows to insert        

        if bPBar: #외부루프가 없는 경우
            pbar = tqdm.tqdm(total=tgtNo , desc="작업대상행수")        

        startNo = 0
        endFlag = True
        resultInsertAcc = 0                

        while endFlag:        
            endNo = startNo + chunksize    
            if (endNo > tgtNo):
                endNo = tgtNo
                endFlag = False #이번 루프를 마지막으로 종료시키기
            dfTmp = df.iloc[startNo:endNo,:]   #df1 : 입력할 chunk

            if bPBar: #외부루프가 없는 경우
                pbar.update(endNo-startNo)            

            resultInsert = dfTmp.to_sql(name=self.strTableName, con=self.objDbCon.objEngine, index=False, if_exists="append")

            #print(startNo,"/",endNo,"/ Insert 완료")
            startNo = startNo + chunksize
            resultInsertAcc = resultInsertAcc + resultInsert            

        if bPBar: #외부루프가 없는 경우
            pbar.close()
            print(resultInsertAcc,"행 Inserted")

    def createTable(self, df:pd.DataFrame) -> None:
        df.head(0).to_sql(self.strTableName, con=self.objDbCon.objEngine, if_exists='replace', index=False)
        print(f"Table '{self.strTableName}' created successfully without inserting data!")