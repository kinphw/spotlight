#RECON 파일 추출
import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF
from spotlight.modify.modify import Modifier

class ReconGL(Modifier): #Inherit Modifier to use 'selectColumn'

    dfResult:pd.DataFrame
    
    @ErrRetryF    
    def run(self):
        cNameAcct = self.selectColumn("Select Account Number (to group by)")
        cNameAmt = self.selectColumn("Select Amount LC (to sum)")
        self.test(cNameAcct, cNameAmt)
        self.export(self)
        print("DONE")

    #상속 후 오버라이드해서 사용할 메서드
    def test(self, cNameAcct:str, cNameAmt:str): #cName1 : 변경할 컬럼, #cName2 : 차대컬럼
        #먼저 float64로 바꾼다
        self.df[cNameAmt] = self.df[cNameAmt].astype('float64')   
        self.dfResult = self.df.groupby(cNameAcct)[cNameAmt].sum()
    
    #공통 메서드
    def export(self):         
        #Run        
        self.dfResult = self.dfResult.reset_index()

        while True:
            flag = input("Excel(1) or Text(2)>>")
            match(flag):
                case '1':
                    fileName = input("검증결과 추출할 파일명을 입력하세요(기본값 RECON.xlsx)>>") or 'RECON.xlsx'
                    df.to_excel(fileName, index=False); break
                case '2':
                    fileName = input("검증결과 추출할 파일명을 입력하세요(기본값 RECON.tsv)>>") or 'RECON.tsv'
                    df.to_csv(fileName, index=False, encoding='utf8', sep='\t'); break
                case _:
                    print("잘못 입력하셨습니다.")


        
        
        
        

