import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF
from spotlight.modify.replace import Replacer

class ExcelNum(Replacer):

    # df:pd.DataFrame
    # bReg:bool
    # def __init__(self, df:pd.DataFrame):
    #     self.df = df

    @ErrRetryF
    def run(self, cName:str): #100을 곱해준다

        strBefore:str
        strAfter:str
        self.df[cName] = self.df[cName].astype('string') #DEBUG : STRING
        print("string type으로 변경함")

        print("1. 공백제거")
        self.bReg = True #240202
        strBefore = '[ ]' ; strAfter = ''
        self._doReplace(cName,strBefore,strAfter)

        print("2. 콤마제거")
        self.bReg = True #240202
        strBefore = '[,]' ; strAfter = ''
        self._doReplace(cName,strBefore,strAfter)

        print("#3. 전체 \"-\" 를 0으로")
        self.bReg = False #240202
        strBefore = '-' ; strAfter = '0'
        self._doReplace(cName,strBefore,strAfter)

        print("#4. ( ) to minus")
        self.bReg = True #240202
        strBefore = '[)]' ; strAfter = '' 
        self._doReplace(cName,strBefore,strAfter)

        self.bReg = True #240202
        strBefore = '[())]' ; strAfter = '-' 
        self._doReplace(cName,strBefore,strAfter)

        print("#5. Change to float64")
        self.df[cName] = self.df[cName].astype('float64')

        print("DONE")        
    