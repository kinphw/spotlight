import pandas as pd
import modin.pandas as mpd #240117
import tqdm
import ray
import typing

from spotlight.common.ErrRetry import ErrRetryF
from spotlight.common.common import mapcount
if typing.TYPE_CHECKING:    
    from spotlight.import2df.import2df import Import2Df
from spotlight.import2df.import2dfInfo import Import2DfInfo
from spotlight.common.protoSelector import ProtoRun

# Import2df가 호출하는 본체
class ImportBody():

    def __init__(self, objMain:Import2Df):
        self.objInfo = objMain.objInfo
        self.path = objMain.path
        self.bPBar = objMain.bPBar

    def run(self) -> pd.DataFrame:        
        match(self.objInfo.type):
            case Import2DfInfo.TXT: return self._importTxt(self.path)
            case Import2DfInfo.PARQUET: return self._importParquet(self.path)
            case Import2DfInfo.PICKLE: return self._importPickle(self.path)
            case Import2DfInfo.EXCEL: return self._importExcel(self.path)            

    ############################            

    @ErrRetryF
    def _importTxt(self, path:str, chunksize:int = 10000000) -> pd.DataFrame:    
        
        if self.objInfo.flagModin: #MODIN을 쓸 때
            if not ray.is_initialized(): ray.init()
            # if self.objInfo.bQuote:
            #     df = mpd.read_csv(path, sep=self.objInfo.sep, encoding=self.objInfo.encod, dtype=self.objInfo.dtype, header=self.objInfo.intHeader) #, low_memory=False)#, chunksize=chunksize) #240119 
            # else: 
            df = mpd.read_csv(path, 
                              sep=self.objInfo.sep, 
                              encoding=self.objInfo.encod, 
                              quoting=self.objInfo.intQuote, 
                              dtype=self.objInfo.dtype, 
                              header=self.objInfo.intHeader) #, low_memory=False)#, chunksize=chunksize) #240119
            df = df._to_pandas() #다시 pd.DataFrame으로 변경
        else:
            cnt = mapcount(path,self.objInfo.encod) -1 #Count Check _ Column 때문에 1을 빼야 함
            if self.bPBar: pbar = tqdm.tqdm(total=cnt, desc='Read')        
            df = pd.DataFrame()        
            
            # if self.objInfo.bQuote: 
            #     dfReader = pd.read_csv(path, sep=self.objInfo.sep, encoding=self.objInfo.encod, low_memory=False, chunksize=chunksize, dtype=self.objInfo.dtype, header=self.objInfo.intHeader)            
            # else: 
            dfReader = pd.read_csv(path, 
                                   sep=self.objInfo.sep, 
                                   encoding=self.objInfo.encod, 
                                   low_memory=False, 
                                   chunksize=chunksize, 
                                   quoting=self.objInfo.intQuote, 
                                   dtype=self.objInfo.dtype, 
                                   header=self.objInfo.intHeader)  #240131 #240214
            for count, chunk in enumerate(dfReader):
                df = pd.concat([df, chunk])
                if self.bPBar: pbar.update(chunk.shape[0])        
            if self.bPBar: pbar.close()
            if cnt != df.shape[0]: print("raw text rows와 dataframe records count가 상이합니다. 주의하세요.(QUOTE때문일 수 있음)") #240131
        return df

    def _importParquet(self, path:str) -> pd.DataFrame:       
        return pd.read_parquet(path)

    def _importPickle(self, path:str) -> pd.DataFrame:        
        return pd.read_pickle(path)

    def _importExcel(self, path:str) -> pd.DataFrame:

        if self.objInfo.flagModin:
            df:mpd.DataFrame = mpd.read_excel(path)
            return df._to_pandas()
        else:
            return pd.read_excel(path)


if __name__ == "__main__":
    ImportBody().run()


