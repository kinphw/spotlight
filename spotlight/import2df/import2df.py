import pandas as pd
import tqdm

import spotlight.common.myFileDialog as myfd
from spotlight.common.ErrRetry import ErrRetry
from spotlight.common.common import mapcount

class Import2Df:    
    def run(self):
        return self.importTxt()

    @ErrRetry
    def importTxt(self) -> pd.DataFrame:       
        path = myfd.askopenfilename("Text 파일을 선택하세요. ")
        sep = input("Seperator? (기본값 \\t)>>") or '\t'
        encod = input("인코딩? (cp949)>>") or 'cp949'        
        
        cnt = mapcount(path,encod) -1 #Count Check _ Column 때문에 1을 빼야 함
        pbar = tqdm.tqdm(total=cnt, desc='Read')        

        df = pd.DataFrame()
        chunksize = 10000000 #천만
        dfReader = pd.read_csv(path, sep=sep, encoding=encod, low_memory=False, chunksize=chunksize)
        for count, chunk in enumerate(dfReader):
            df = pd.concat([df, chunk])
            pbar.update(chunk.shape[0])
        pbar.close()
        return df

def runImport2Df():
    return Import2Df().run()

if __name__=='__main__':
    runImport2Df()