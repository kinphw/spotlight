import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF
from spotlight.recon.recon import ReconGL
from spotlight.merge.setkey import SetKey #재활용
from spotlight.common.colors import Colors

class UniqueValidator(ReconGL): #Inherit Modifier to use 'selectColumn'

    #df : pd.DataFrame #상속
    #def __init__(self, df): self.df = df #상속

    # 1. 전표금액 컬럼 설정
    # 2. 분석대상 컬럼 복수설정 => 리스트로 (기존개발기능 활용)
    # 3. groupby => 전표금액 SUM침
    # 4. groupby SUM == 0 인지 확인
    # 5. 에러를 확인하기 위해 reset_index 후에 엑셀로 추출함

    serFalse:pd.Series

    @ErrRetryF    
    def run(self):
        self.help()        
        cNameAmt = self.selectColumn("Select Amount LC (to sum)")
        li_cNameUniq:list = SetKey(self.df).run("set Key(유일성검증 대상)")        
        bPass = self.test(cNameAmt, li_cNameUniq)
        self.exportWrapper(bPass)
        print("DONE")        

    def help(self):
        print(Colors.RED + "#"*30 + Colors.END)
        print("검증목적 전표벌 주요 구분자(column) 유일성 검증을 실시합니다.")
        print("주요 구분자별로 groupby하여 전표금액 합계가 0으로 떨어지는지 확인합니다.")
        print(Colors.RED + "ex) 전표번호별/전기일자별 전표금액 합계(차대)는 일치해야 한다 => 구분자로 전표번호/전기일자 선택 " + Colors.END)
        print("Spotlight / Excel JET 범용으로 사용가능합니다. (구분자 선택에 따라)")
        print("사용법 : ")
        print("1. 전표금액 컬럼을 선택한다. (컬럼별 Groupby Sum 대상객체)")
        print("2. 유일성검증을 실시할 구분자를 선택한다. (복수선택가능. 전표번호부터)")
        print("3. 검증결과 중 이상내역을 화면출력하며, 전체 검증결과를 Text파일로 추출한다.")        
        print(Colors.RED + "#"*30 + Colors.END)

    def test(self, cNameAmt:str, li_cNameUniq:list) -> bool: 
        self.df[cNameAmt] = self.df[cNameAmt].astype('float64') #먼저 float64로 바꾼다
        #실시
        self.dfResult = self.df.groupby(li_cNameUniq)[cNameAmt].sum()    

        print(Colors.RED + "#"*30 + Colors.END)
        print("전체 조합의 수 : ", self.dfResult.shape[0])
        
        self.serFalse = self.dfResult[self.dfResult != 0] #Series #실패한 그룹
        print("유일성 검증결과를 통과하지 못한 조합의 수 : ", self.serFalse.shape[0])
        print(Colors.RED + "#"*30 + Colors.END)

        if self.serFalse.shape[0] == 0: return True
        else: return False

    def exportWrapper(self, bPass:bool):        
        if bPass: #성공시
            if (input("검증결과 전체내역을 추출하겠습니까?(Y) (기본값 N)>>") or 'N') == 'Y': self.export()
            else: print("추출하지 않습니다.")
        else: #실패시
            print("통과하지 못한 내역을 출력합니다.(상위 10개)")
            print(self.serFalse.head(10))    

            if (input("검증결과 오류내역만 추출하겠습니까?(Y) (기본값 N. 전체를 추출)>>") or 'N') == 'Y':
                self.dfResult = self.serFalse.reset_index() #multi index => column
            
            self.export()