import pandas as pd

#from spotlight.main import Spotlight
from spotlight.common.ErrRetry import ErrRetryF
from spotlight.modify.killComma import KillComma
from spotlight.modify.applyDC import ApplyDC
from spotlight.modify.minus import ToMinus
from spotlight.modify.m100 import M100
from spotlight.modify.createUnsigned import CreateUnsigned
from spotlight.modify.fillna import FillNA

class Modifier:

    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame): #의존성 주입
        self.df = df

    def run(self) -> None:
        text =  "#"*10+"\n"
        text += "MODIFY MODE\n"
        text += "전처리_전표금액\n"
        text += "11. Kill Comma (문자열 컬럼 내에서 replace(',',''))\n" #콤마 없애기 : 변경컬럼선택 / 시행        
        text += "12. Apply DC (차변은 +, 대변은 - 처리)\n" #차대구분에 따라 (-)처리 : 변경컬럼선택 / 차대컬럼선택 / 차변구분자 선택 / 시행        
        text += "13. To Minus () or - : 문자열 () 또는 후위-인 경우 마이너스로 변환\n" #마이너스전환 : ()인 경우
        text += "14. Multiple 100  : 곱하기 100\n" #*100 : 변경컬럼선택 / 시행
        text += "15. FROM 전표금액 TO 차대금액  : signed 전표금액에서 unsigned 차변/대변을 생성한다.\n" #전표금액을 차대금액으로 뿌리기 : 전표기능/ 전표표시 선택 / (+)(-)로 자동 뿌림
        text += "16. FILLNA(0)  : N/A를 0으로 채운다.\n" 
        text += "90. DEBUG MODE\n"
        text += "98. df.info()\n"
        text += "99. df.head(10)\n"
        #####
        textMain = "enter '?' to help / 'q' to exit"

        while True:
            print(textMain)
            flag = input(">>")            
            match flag:
                case '?': print(text)
                case 'q': print("MODIFY MODE END"); break
                case '11': #콤마 없애기 : 변경컬럼선택 / 시행
                    cName = self.selectColumn() #컬럼명 추출
                    KillComma(self.df).run(cName) #DF랑 컬럼명을 던진다

                case '12': #콤마 없애기 : 변경컬럼선택 / 시행
                    cName1 = self.selectColumn("변경할 컬럼을 선택하세요") #컬럼명 추출
                    cName2 = self.selectColumn("차대구분자컬럼을 선택하세요(D/C, S/H 등)") #컬럼명 추출
                    ApplyDC(self.df).run(cName1, cName2)                     
                
                case '13':
                    cName = self.selectColumn("변경할 컬럼을 선택하세요") #컬럼명 추출
                    ToMinus(self.df).run(cName)

                case '14':
                    cName = self.selectColumn("변경할 컬럼을 선택하세요") #컬럼명 추출
                    M100(self.df).run(cName)

                case '15':                    
                    cNameSigned = self.selectColumn("select signed amount (From)") #컬럼명 추출
                    cNameUnsignedD = self.selectColumn("select Unsigned Debit (To Create)") #컬럼명 추출
                    cNameUnsignedC = self.selectColumn("select Unsigned Credit (To Create)") #컬럼명 추출
                    CreateUnsigned(self.df).run(cNameSigned, cNameUnsignedD, cNameUnsignedC)

                case '16':
                    cName = self.selectColumn("변경할 컬럼을 선택하세요") #컬럼명 추출
                    FillNA(self.df).run(cName)

                case '90':
                    print("DEBUG NOW") #여기다 BREAKPOINT를 걸면 수기 디버깅가능
                case '98': self.df.info()
                case '99': print(self.df.head(10))

                case _: print("Retry"); continue

    @ErrRetryF
    def selectColumn(self, msg:str = "Select column") -> str:
        print(msg)
        self.df.info()
        num = input(">>")
        num = int(num) 
        cName = self.df.columns[num] #선택한 번호에 해당하는 컬럼명을 반환한다.
        return cName