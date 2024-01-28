from spotlight.common.ErrRetry import ErrRetryF
from spotlight.recon.recon import ReconGL

class CalSum(ReconGL): #기능이 비슷한 recon을 상속  #Inherit Modifier to use 'selectColumn'

    #이하 Override
    @ErrRetryF    
    def run(self):
        #cNameAcct = self.selectColumn("Select Account Number (to group by)")
        cNameAmt = self.selectColumn("Select Column to sum")
        self.export(cNameAmt)

    def test(self, cNameAmt:str): 
        #먼저 float64로 바꾼다
        self.df[cNameAmt] = self.df[cNameAmt].astype('float64')
        print("합계 :", self.df[cNameAmt].sum())
        



        

