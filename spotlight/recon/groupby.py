import pandas as pd 
from spotlight.common.ErrRetry import ErrRetryF
from spotlight.recon.recon import ReconGL
from spotlight.merge.setkey import SetKey

class GroupbyUserDefine(ReconGL): #Inherit Modifier to use 'selectColumn'

    #df
    #dfResult
    strType : str = 'sum' #SUM인지 COUNT인지
    #bStop : bool = False #중단

    @ErrRetryF
    def run(self):
        print("특정 컬럼(들)을 지정하여 groupby(피벗)한 후 합계(Sum) 또는 갯수(Count)를 추출합니다.")        
        while True:
            flag = input("1. 합계(sum) / 2. 전체갯수(size) / 3. 그룹별갯수(nunique)")
            match flag:
                case '1':
                    self.strType = 'sum'
                    cName = self.selectColumn("Select Column to sum")
                    self.__toFloat64(cName)
                    liCNameGroupby:list = SetKey(self.df).run("set Key to groupby")
                    self.__test(liCNameGroupby, cName)
                    break

                case '2':
                    self.strType = 'size'
                    liCNameGroupby:list = SetKey(self.df).run("set Key to groupby")                    
                    self.__test(liCNameGroupby)
                    break

                case '3':
                    self.strType = 'nunique'
                    cName = self.selectColumn("Select Column to count")
                    liCNameGroupby:list = SetKey(self.df).run("set Key to groupby")
                    self.__test(liCNameGroupby, cName)
                    break

                case _:
                    print("다시 입력하세요")        

        print("결과 : (상위 5줄만 화면에 표시함)")
        print(self.dfResult.head())
        print("DONE")

        self.export()

    def __test(self, liCnameGroupby, cName = None): #cName1 : 변경할 컬럼, #cName2 : 차대컬럼  

        if self.strType == 'sum': #합계인 경우
            g = self.df.groupby(liCnameGroupby)[cName].sum()
        elif self.strType == 'size':
            g = self.df.groupby(liCnameGroupby).size()
        elif self.strType == 'nunique':
            g = self.df.groupby(liCnameGroupby)[cName].nunique()

        self.dfResult:pd.DataFrame = g.reset_index()    

    def __toFloat64(self, cName:str):        
        print("SUM Column을 먼저 float64로 바꿉니다.")
        self.df[cName] = self.df[cName].astype('float64')                
        print("데이터타입 변경완료")

#240127 : 설명을 수정        

