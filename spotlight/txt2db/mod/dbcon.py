from typing import Optional
import pandas as pd
import pymysql
import sqlalchemy
pymysql.install_as_MySQLdb()


import spotlight.common.myFileDialog as myfd

class DbCon:

    objEngine:sqlalchemy.Engine
    
    def __init__(self):
        self._connect()

    def _connect(self, flag:str = 'mysql', dbName : Optional[str] = None) -> bool:

        mySQL_ID:str = input("ID? (DBMS)>>")
        mySQL_PW:str = input("Password? (DBMS)>>")
        if dbName is not None:
            mySQL_DB:str = dbName
        else:
            mySQL_DB:str = input("DB Name? (DBMS)>>")

        if flag=="mysql":
            #MySQL에 연결하는 경우
            engine = sqlalchemy.create_engine("mysql+mysqldb://"+mySQL_ID+":"+mySQL_PW+"@127.0.0.1/"+mySQL_DB+"?charset=utf8")

        elif flag=="mssql":
            #MSSQL에 연결하는 경우
            engine = sqlalchemy.create_engine("mssql+pyodbc://"+mySQL_ID+":"+mySQL_PW+"!@mymssql")
            #engine.connect()
        
        try:
            conn = engine.connect()
            print("DB에 연결되었습니다.")
            self.objEngine = engine
            return True
        except:
            print("DB 연결에 실패했습니다.")
            return False
        

