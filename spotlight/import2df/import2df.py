import csv

import pandas as pd
import modin.pandas as mpd #240117
import tqdm
import ray

import spotlight.common.myFileDialog as myfd
from spotlight.common.ErrRetry import ErrRetry
from spotlight.common.common import mapcount

class Import2Df:    

    def run(self, msg:str = "") -> pd.DataFrame | None:
        
        help = "1. import txt\n"
        help += "2. import parquet\n"
        help += "3. import pickle\n"
        help += "4. import Excel\n"
        help += "5. quit\n"      
        print(help)
        flag = input(">>")
        match(flag):
            case '1': return self._importTxt(msg)
            case '2': return self._importParquet(msg)
            case '3': return self._importPickle(msg)
            case '4': return self._importExcel(msg)            
            case '5': return None
            case _: print("Wrong"); return None

    @ErrRetry
    def _importTxt(self, msg:str = "Text 파일을 선택하세요.") -> pd.DataFrame:       
        path = myfd.askopenfilename(msg)
        print(": ",path)
        sep = input("Seperator? (기본값 \\t)>>") or '\t'
        encod = input("인코딩? (cp949)>>") or 'cp949'
        
        #240215
        flag = input("quote(\")를 사용합니까? (Y/N, 기본값 Y)")
        if flag == 'Y': bQuote = True
        elif flag == 'Y': bQuote = False
        else: print("선택하지 않았습니다. quote를 사용합니다."); bQuote = True

        ## MODIN 활용부
        flagModin = input("USE MODIN? MODIN doesn't support chunksize (DEFAUT : N)>>") or 'N'
        
        if flagModin =='Y': #MODIN을 쓸 때
            #df = mpd.DataFrame()
            #chunksize = 10000000 #천만
            if not ray.is_initialized(): ray.init()
            
            if bQuote: df = mpd.read_csv(path, sep=sep, encoding=encod, dtype='string') #, low_memory=False)#, chunksize=chunksize) #240119 
            else: df = mpd.read_csv(path, sep=sep, encoding=encod, quoting=csv.QUOTE_NONE, dtype='string') #, low_memory=False)#, chunksize=chunksize) #240119 
            # for count, chunk in enumerate(dfReader):
            #     df = mpd.concat([df, chunk])
            #     pbar.update(chunk.shape[0])
            df = df._to_pandas() #다시 pd.DataFrame으로 변경
        else:
            cnt = mapcount(path,encod) -1 #Count Check _ Column 때문에 1을 빼야 함
            pbar = tqdm.tqdm(total=cnt, desc='Read')        
            df = pd.DataFrame()        
            chunksize = 10000000 #천만
            
            if bQuote: dfReader = pd.read_csv(path, sep=sep, encoding=encod, low_memory=False, chunksize=chunksize, dtype='string')  #240131 #240214
            else: dfReader = pd.read_csv(path, sep=sep, encoding=encod, low_memory=False, chunksize=chunksize, quoting=csv.QUOTE_NONE, dtype='string')  #240131 #240214
            for count, chunk in enumerate(dfReader):
                df = pd.concat([df, chunk])
                pbar.update(chunk.shape[0])        
            pbar.close()
            if cnt != df.shape[0]: print("raw text rows와 dataframe records count가 상이합니다. 주의하세요.(QUOTE때문일 수 있음)") #240131
        
        return df

    def _importParquet(self, msg:str = "Select parquet") -> pd.DataFrame:
        path = myfd.askopenfilename(msg)
        return pd.read_parquet(path)

    def _importPickle(self, msg:str = "Select pickle") -> pd.DataFrame:
        path = myfd.askopenfilename(msg)
        return pd.read_pickle(path)

    def _importExcel(self, msg:str = "Select Excel") -> pd.DataFrame:
        path = myfd.askopenfilename(msg)

        flagModin = input("USE MODIN? (DEFAUT : N)>>") or 'N'
        if flagModin == 'Y':
            df:mpd.DataFrame = mpd.read_excel(path)
            return df._to_pandas()
        else:
            return pd.read_excel(path)

# def runImport2Df(msg:str = "") -> pd.DataFrame:
#     return Import2Df().run(msg)

if __name__=='__main__':
    Import2Df().run()