from spotlight.common.ErrRetry import ErrRetryF
from spotlight.recon.recon import ReconGL

class PivotMonthAcct(ReconGL): #Inherit Modifier to use 'selectColumn'

    @ErrRetryF    
    def run(self):
        print("검증목적 계정별/월별 피벗테이블을 추출하여 파일로 저장합니다.")
        
        cNameAcct = self.selectColumn("Select Account Number (to row)")
        cNameMonth = self.selectColumn("Select Period (to column)")
        cNameAmt = self.selectColumn("Select Amount LC (to sum)")
        self.export(cNameAcct, cNameMonth, cNameAmt)
    
    def export(self, cNameAcct:str, cNameMonth:str, cNameAmt:str): #cName1 : 변경할 컬럼, #cName2 : 차대컬럼

        #먼저 float64로 바꾼다
        self.df[cNameAmt] = self.df[cNameAmt].astype('float64')

        #Run
        fileName = input("검증결과 추출할 파일명을 입력하세요(기본값 GL_RECON_MONTH.xlsx)>>") or 'GL_RECON_MONTH.xlsx'
        
        g = self.df.groupby([cNameAcct, cNameMonth])[cNameAmt].sum()
        g.unstack(cNameMonth).to_excel(fileName)
        
        print("DONE")
        

