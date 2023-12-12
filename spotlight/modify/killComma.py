import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF


class KillComma:

    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame):
        self.df = df

    @ErrRetryF
    def run(self, cName:str): #콤마 없애기
        self.df[cName] = self.df[cName].astype('str')
        print("str type으로 변경함")
        self.df[cName] = self.df[cName].replace('[,]','',regex=True)
        print("DONE")
        
