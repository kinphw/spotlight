import pandas as pd

class Saver:
    def save(cls, df:pd.DataFrame) -> None:

        path = input("저장할 Text filename을 지정하세요(기본값 result.tsv)>>") or 'result.tsv'        
        encod = input("인코딩? (cp949)>>") or 'utf8'        

        df.to_csv(index=False, sep='\t', encoding=encod, path_or_buf=path)

        print("save done")   
