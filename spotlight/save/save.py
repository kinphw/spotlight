import pandas as pd
import tqdm

class Saver:
    def save(cls, df:pd.DataFrame) -> None:

        path = input("저장할 Text filename을 지정하세요(기본값 result.tsv)>>") or 'result.tsv'        
        encod = input("인코딩? (cp949)>>") or 'utf8'

        pbar = tqdm.tqdm(total=df.shape[0], desc='Save')                

        lineStart = 0
        chunksize = 10000000 #천만으로 변경
        flagFirst = True #처음에만 헤더를 넣기 위한 Flag
        while True: #헤더가 추가되는 오류 디버그 231206
            lineEnd = min(lineStart + chunksize, df.shape[0])
            length = lineEnd - lineStart
            if flagFirst: df.iloc[lineStart:lineEnd, :].to_csv(index=False, sep='\t', encoding=encod, path_or_buf=path, mode='a')            
            else: df.iloc[lineStart:lineEnd, :].to_csv(index=False, sep='\t', encoding=encod, path_or_buf=path, mode='a', header=None)
            pbar.update(length)
            lineStart += length

            if flagFirst: flagFirst = False
            if lineEnd >= df.shape[0]: break       

        print("save done")   
