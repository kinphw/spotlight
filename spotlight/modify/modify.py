import pandas as pd

#from spotlight.main import Spotlight
from spotlight.common.ErrRetry import ErrRetryF
from spotlight.common.protoSelector import ProtoSelector, ProtoABSSelector
from spotlight.modify.replace import Replacer
from spotlight.modify.applyDC import ApplyDC
from spotlight.modify.minus import ToMinus
from spotlight.modify.m100 import M100
from spotlight.modify.createUnsigned import CreateUnsigned
from spotlight.modify.createSigned import CreateSigned
from spotlight.modify.fillna import FillNA
from spotlight.modify.automanual import AutoManual
from spotlight.modify.dropColumn import DropColumn
from spotlight.modify.dropDuplicate import DropDuplicate
from spotlight.common.colors import Colors
from spotlight.modify.removeD import RemoveDecimal
from spotlight.modify.excelNum import ExcelNum

class Modifier(ProtoABSSelector):

    #df:pd.DataFrame

    # def __init__(self, df:pd.DataFrame = None): #의존성 주입
    #     self.df = df

    def run(self) -> pd.DataFrame:
        text =  "#"*10+"\n"
        text += Colors.RED + "MODIFY MODE\n" + Colors.END
        text += Colors.RED + "전처리_전표금액\n" + Colors.END
        text += "11. replace string (Kill comma, space, regex etc.)\n" #
        text += "12. Apply DC (차변은 +, 대변은 - 처리)\n" #차대구분에 따라 (-)처리 : 변경컬럼선택 / 차대컬럼선택 / 차변구분자 선택 / 시행        
        text += "13. To Minus () or - : 문자열 () 또는 후위-인 경우 마이너스로 변환\n" #마이너스전환 : ()인 경우
        text += "14. Multiple 100  : 곱하기 100\n" #*100 : 변경컬럼선택 / 시행
        text += "15. FROM 전표금액 TO 차대금액  : signed 전표금액에서 unsigned 차변/대변을 생성한다.\n" #전표금액을 차대금액으로 뿌리기 : 전표기능/ 전표표시 선택 / (+)(-)로 자동 뿌림
        text += "16. FROM 차대금액 TO 전표금액  : unsigned 차변/대변에서 signed 전표금액을 생성한다.\n"
        text += "17. FILLNA(0)  : N/A를 0으로 채운다.\n" 
        text += "18. 자동수동 : 특정 컬럼값(전표성격, 사용자 등)이 특정 문자열(복수 가능)을 포함하는 행을 A로 지정\n"
        text += "19. 전표번호에서 소수점 제거(특히, 문자/숫자 mixed dtype에 대하여) => 벡터연산이 아니므로 느릴 수 있음\n"
        text += "110. (Excel을 TSV로 변환한 경우) 숫자형식 일괄 전처리 : 공백제거+콤마제거+\"-\"0으로+()음수화\n"
        text += "\n"
        text += Colors.RED + "기타 전처리\n" + Colors.END
        text += "21. drop a column\n"
        text += "22. drop duplicate\n"
        text += "23. Change column name\n"
        text += "24. Change column datatype\n"
        text += "25. Change column datatype : All Object to String\n"
        text += "26. Add new column(to do something) : NA로 채워짐\n"
        text += "\n"
        text += Colors.RED + "General\n" + Colors.END
        text += "90. DEBUG MODE (USE Self.df)\n"
        text += "98. df.info()\n"
        text += "99. df.head(10)\n"
        #####
        textMain = Colors.RED + "MODIFY MODE : enter '?' to help / 'q' to exit" + Colors.END

        while True:
            print(textMain)
            flag = input(">>")            
            match flag:
                case '?': print(text)
                case 'q': print("MODIFY MODE END"); return self.df #240120. 직접 수정하는 경우 call by obj.ref가 풀리기 때문에 반환해줘야 함
                case '11': #콤마 없애기 : 변경컬럼선택 / 시행
                    cName = self.selectColumn() #컬럼명 추출
                    Replacer(self.df).run(cName) #DF랑 컬럼명을 던진다

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

                case '15': self._createUnsigned()          
                case '16': self._createSigned()

                case '17':
                    cName = self.selectColumn("변경할 컬럼을 선택하세요") #컬럼명 추출
                    FillNA(self.df).run(cName)

                case '18':
                    cNameBase = self.selectColumn("자동수동 구분 기준값을 포함하는 컬럼을 선택하세요(성격 또는 사용자 등)") #컬럼명 추출
                    cNameAM = self.selectColumn("자동수동 컬럼을 선택하세요") #컬럼명 추출
                    AutoManual(self.df).run(cNameBase, cNameAM)

                case '19':
                    RemoveDecimal(self.df).run(self.selectColumn("소수점을 제거할 (즉 .0을 삭제할 컬럼을 선택하세요"))

                case '110':
                    ExcelNum(self.df).run(self.selectColumn("엑셀변환 텍스트에서 숫자로 변경할 컬럼을 선택하세요"))

                case '21':
                    cName = self.selectColumn("Drop할 Column을 선택하세요") #컬럼명 추출
                    DropColumn(self.df).run(cName)
                case '22': DropDuplicate(self.df).run()
                case '23': self._changeColumn()
                case '24': self._changeColumnDtype()
                case '25': self._changeColumnDtypeAllObj2Str()
                case '26': self._addEmptyColumn()

                case '90': breakpoint() #240119
                case '98': self.df.info()
                case '99': print(self.df.head(10))

                case _: print("Retry"); continue

    # @ErrRetryF
    # def selectColumn(self, msg:str = "Select column", df:pd.DataFrame = None) -> str: #DF Injection은 선택. 기본값은 self.df 사용
    #     print('\n'+msg+'\n')
    #     if not isinstance(df,pd.DataFrame): df = self.df # USE Self.df when no injected df
    #     df.info()
    #     num = input(">>")
    #     num = int(num) 
    #     cName = df.columns[num] #선택한 번호에 해당하는 컬럼명을 반환한다.
    #     return cName

    @ErrRetryF
    def _changeColumn(self) -> None: 
        cNameBefore = self.selectColumn("변경하고자 하는 컬럼을 선택하세요")        
        cNameAfter = input("변경 후 컬럼명을 입력>>")
        self.df.rename(columns={cNameBefore:cNameAfter}, inplace=True)
        print("DONE")

    @ErrRetryF
    def _changeColumnDtype(self) -> None: 
        cName = self.selectColumn("변경하고자 하는 컬럼을 선택하세요")        
        cDtype = input("변경하고자 하는 자료형을 입력(i.e. string, float64, int64 등)>>")        
        self.df[cName] = self.df[cName].astype(cDtype)
        print("DONE")
    
    #240120
    @ErrRetryF
    def _changeColumnDtypeAllObj2Str(self) -> None:
        print("모든 Object column을 String으로 일괄변환")
        for i in self.df.columns.to_list():
            if self.df.dtypes[i] == 'O': print(i,"변환합니다."); self.df[i] = self.df[i].astype('string')
        print("DONE")

    @ErrRetryF
    def _addEmptyColumn(self) -> None:         
        cNameAfter = input("새로 만들 컬럼명을 입력>>")
        self.df[cNameAfter] = pd.NA
        print("DONE")        

    @ErrRetryF
    def _createUnsigned(self):
        cNameSigned = self.selectColumn("select signed amount (From)") #컬럼명 추출
        cNameUnsignedD = self.selectColumn("select Unsigned Debit (To Create)") #컬럼명 추출
        cNameUnsignedC = self.selectColumn("select Unsigned Credit (To Create)") #컬럼명 추출
        CreateUnsigned(self.df).run(cNameSigned, cNameUnsignedD, cNameUnsignedC)

    @ErrRetryF
    def _createSigned(self):        
        cNameUnsignedD = self.selectColumn("select Unsigned Debit (To Create)") #컬럼명 추출
        cNameUnsignedC = self.selectColumn("select Unsigned Credit (To Create)") #컬럼명 추출
        flag = input("Signed Amount 컬럼을 새로 생성합니까? Y / N")
        if flag == 'Y': self._addEmptyColumn()
        cNameSigned = self.selectColumn("select signed amount (From)") #컬럼명 추출       
        CreateSigned(self.df).run(cNameSigned, cNameUnsignedD, cNameUnsignedC)        