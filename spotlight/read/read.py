import os
import pandas as pd

import spotlight.common.myFileDialog as myfd
from spotlight.common.protoSelector import ProtoABSSelector
from spotlight.common.view import DfViewer
from spotlight.import2df.import2df import Import2Df

class ReadColumnLength(ProtoABSSelector):    

    def run(self) -> None:
        # path = myfd.askopenfilename("Select a sample GL file")
        # encoding = input("encoding, 기본값 cp949>>") or 'cp949'
        # sep = input("sep, 기본값 tsv>>") or '\t'
        # df = pd.read_csv(path, encoding=encoding, sep=sep, low_memory=False, dtype='string') #DEBUG.: 240211

        if not isinstance(self.df, pd.DataFrame):
            print("df가 설정되지 않았습니다. df를 설정합니다.")
            self.df = Import2Df().run()
        
        if self.df is None:
            print("df가 설정되지 않았습니다. 종료합니다.")
            return
        
        df = self.df        
        dfTmp = pd.DataFrame()
        for column in df:
            print(column,"->", df[column].astype(str).str.len().max())
            #di[column] = df[column].astype(str).str.len().max()

            di = {'ColumnName':column,
                  'Length':df[column].astype(str).str.len().max()
                }   

            dfDi = pd.DataFrame(di, index=[0])
            dfTmp = pd.concat([dfTmp, dfDi])
        
        flag:str = input("1. View() (def)/ 2. Excel추출>>")
        if str =='2':
            dfTmp.to_excel("ColumnLength.xlsx", index=False)
            print("ColumnLength.xlsx 추출완료. Table 설계하세요")     
        else:
            DfViewer(dfTmp).run()

# def runReadColumnLength():
#     ReadColumnLength().run()

# if __name__=='__main__':
#     runReadColumnLength()
    
    



