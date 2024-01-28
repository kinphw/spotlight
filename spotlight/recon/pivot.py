from spotlight.common.ErrRetry import ErrRetryF
from spotlight.recon.recon import ReconGL

class PivotMonthAcct(ReconGL): #Inherit Modifier to use 'selectColumn'

    @ErrRetryF    
    def run(self):
        print("검증목적의 행렬피벗테이블(전표금액 합산)을 추출하여 파일로 저장합니다. (행/열 Index를 1개씩 지정. ex: 행으로 계정/열으로 월)")
        
        cNameRow = self.selectColumn("Select row(ex. Account Number)")
        cNameColumn = self.selectColumn("Select column (ex. Period)")
        cNameAmt = self.selectColumn("Select Amount LC (to sum)")
        self.test(cNameRow, cNameColumn, cNameAmt)
        self.export()
        print("DONE")

    def test(self, cNameRow:str, cNameColumn:str, cNameAmt:str): #cName1 : 변경할 컬럼, #cName2 : 차대컬럼        
        #먼저 float64로 바꾼다
        self.df[cNameAmt] = self.df[cNameAmt].astype('float64')        
        g = self.df.groupby([cNameRow, cNameColumn])[cNameAmt].sum()
        self.dfResult = g.unstack(cNameColumn)

#240127 : 설명을 수정        

