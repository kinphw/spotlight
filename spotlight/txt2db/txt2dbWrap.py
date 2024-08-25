import pandas as pd

from spotlight.common.protoSelector import ProtoABSSelector
from spotlight.txt2db.txt2db import Txt2Db
from spotlight.txt2db.txt2dbMulti import Txt2DbMulti

# Simple factory pattern
class Txt2DbWrapper(ProtoABSSelector):
    def __init__(self, df:pd.DataFrame = None):
        self.df = df

    def run(self):
        # 단일파일 or 폴더내파일일괄
        msg = ""
        msg += "1. 단일 파일 읽기(def, 테이블구조만 생성하는 경우 포함) / 2. 폴더 내 파일 일괄읽기 >>"
        print(msg)
        flag = input(">>") or "1"
        
        while True:
            match(flag):
                case "1":
                    Txt2Db(self.df).run()
                    return
                case "2":
                    Txt2DbMulti(self.df).run()
                    return
                case _:
                    print("잘못된 입력입니다.")
                    continue