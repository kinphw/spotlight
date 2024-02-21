import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF
from spotlight.common.protoSelector import ProtoSelector

#정규식 추가할 수 있도록 변경 (정규식 before, after 받음)
'''
콤마 없애기 : '[,]',''
공백 없애기 : '[ ]',''
마지막 - 없애기 : '[-]$',''
'''
class Replacer(ProtoSelector):

    # df:pd.DataFrame
    bReg:bool

    # def __init__(self, df:pd.DataFrame):
    #     self.df = df

    @ErrRetryF
    def run(self, cName:str) -> None: #콤마 없애기

        self.df[cName] = self.df[cName].astype('string') #DEBUG : STRING
        print("string type으로 변경함")

        msg = "1. Kill Comma\n"
        msg += "2. Kill Space\n"        
        msg += "11. User-defined Regular expression\n"
        msg += "12. User-defined Replace (NOT Regular expression)\n" #240202
        msg += "21. Kill \\t and \\n (전체 dataframe 대상)\n" #240117        
        print(msg)
        flag = input(">>")
        
        strBefore:str;strAfter:str
        self.bReg = True #240202
        
        match(flag):
            case '1': strBefore = '[,]' ; strAfter = ''
            case '2': strBefore = '[ ]' ; strAfter = ''
            case '11':
                strBefore = input("변경전 정규식을 직접 입력하세요. (i.e. [-]$) (기본값 : '[ ]')>>") or '[ ]'
                strAfter = input("변경후 문자열(NOT 정규식)을 직접 입력하세요. (기본값 : '')>>") or '' #240202 오타수정
            case '12':
                strBefore = input("변경전 문자열을 직접 입력하세요. 전체가 일치하는 Record만 변경됩니다. (not 부분) (i.e. -) (기본값 : '')>>") or ''
                strAfter = input("변경후 문자열을 직접 입력하세요. (기본값 : '')>>") or ''
                self.bReg = False
            case '21':
                print("전체 데이터프레임 대상으로 탭과 개행문자를 제거합니다 : 엑셀로 읽는 경우 개행도 있을 수 있음")
                self.df.replace(['\t'], [''], regex=True, inplace=True)
                self.df.replace(['\n'], [''], regex=True, inplace=True)
                print("완료")
                return
            case _:
                print("잘못 입력하였습니다."); return

        self._doReplace(cName,strBefore,strAfter)
        print("DONE")

    def _doReplace(self, cName:str, strBefore:str, strAfter:str) -> None:
        if self.bReg: self.df[cName] = self.df[cName].replace(strBefore,strAfter,regex=True)
        else: self.df[cName] = self.df[cName].replace(strBefore,strAfter)        
