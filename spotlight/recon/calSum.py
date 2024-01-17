from spotlight.common.ErrRetry import ErrRetryF
from spotlight.recon.recon import ReconGL

class CalSum(ReconGL): #기능이 비슷한 recon을 상속  #Inherit Modifier to use 'selectColumn'

    #이하 Override
    @ErrRetryF    
    def run(self):
        #cNameAcct = self.selectColumn("Select Account Number (to group by)")
        cNameAmt = self.selectColumn("Select Column to sum")
        self.export(cNameAmt)
    
    def export(self, cNameAmt:str): 

        #먼저 float64로 바꾼다
        self.df[cNameAmt] = self.df[cNameAmt].astype('float64')

        #Run
        #fileName = input("검증결과 추출할 파일명을 입력하세요(기본값 GL_RECON.xlsx)>>") or 'GL_RECON.xlsx'        
        print("합계 :", self.df[cNameAmt].sum())        
        #print("DONE")
        

