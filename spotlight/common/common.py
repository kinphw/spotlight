import pandas as pd
import glob
import spotlight.common.myFileDialog as myfd

# 데이터프레임 컬럼을 trim하는 함수. Call by object reference이므로 return 불필요
def stripColumn(df:pd.DataFrame) -> None:
    df.columns = [str.strip(i) for i in df.columns.to_list()]

def obj2str(df:pd.DataFrame) -> None:
    #df를 받아서, object인 columns을 모두 string으로 변경해줌
    for column in df.columns:    
        if df[column].dtype == 'object':
            df[column] = df[column].astype(str) # Call by Object Refenece이므로 Return 불필요    

