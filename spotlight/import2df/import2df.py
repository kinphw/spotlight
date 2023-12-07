import pandas as pd

import spotlight.common.myFileDialog as myfd
from spotlight.common.ErrRetry import ErrRetry

class Import2Df:    
    def run(self):
        return self.importTxt()

    @ErrRetry
    def importTxt(self) -> pd.DataFrame:       
        path = myfd.askopenfilename("Text 파일을 선택하세요. ")
        sep = input("Seperator? (기본값 \\t)>>") or '\t'
        encod = input("인코딩? (cp949)>>") or 'cp949'        
        return pd.read_csv(path,sep=sep,encoding=encod, low_memory=False)

def runImport2Df():
    return Import2Df().run()

if __name__=='__main__':
    runImport2Df()