# SPOTLIGHT
# LSE

# 엑셀로 제공됨. 엑셀 헤더가 불규칙함. (헤더가 있기도 하고 없기도하고 합계가 있는 경우도 잇음)
# 따라서 텍스트 추출 후 전처리 필요

import pandas as pd
import numpy as np

#1개의 df로 만든다
# file1 + ( file2 - 1월) + file3

file1 = r'C:\Work\엘에스일렉트로닉스\02_3_통합GL텍스트\05.txt'.replace('\\','/')
file2 = r'C:\Work\엘에스일렉트로닉스\02_3_통합GL텍스트\other.txt'.replace('\\','/')
file3 = r'C:\Work\엘에스일렉트로닉스\02_3_통합GL텍스트\lse_1월.txt'.replace('\\','/')

df1 = pd.read_csv(file1, sep='\t', encoding='utf8', quotechar='"', low_memory=False)
df2 = pd.read_csv(file2, sep='\t', encoding='utf8', quotechar='"', low_memory=False)
df3 = pd.read_csv(file3, sep='\t', encoding='utf8', quotechar='"', low_memory=False)

from spotlight.common.common import stripColumn
stripColumn(df1)
stripColumn(df2)
stripColumn(df3)

df1['전표금액(기준통화)'].astype(np.float64).sum()
df2['전표금액(기준통화)'].astype(np.float64).sum()
df3['전표금액(기준통화)'].astype(np.float64).sum()

#오류처리
df3['전표금액(기준통화)'] = pd.to_numeric(df3['전표금액(기준통화)'].apply(lambda x:str.strip(x)).replace("-",""))

df1['전표금액(기준통화)'] = df1['전표금액(기준통화)'].astype(np.float64)
df2['전표금액(기준통화)'] = df2['전표금액(기준통화)'].astype(np.float64)

#df2에서 1월을 날림
df2.head()
df2['회계월'].shape[0]
df2 = df2[df2['회계월'] != 1]

dfCon = pd.concat([df1,df2,df3])
df1.shape[0] + df2.shape[0] + df3.shape[0]
dfCon.shape[0]

#차대검증
dfCon.columns
dfCon['전표금액(기준통화)'].sum()

#TB Recon
dfGroup = dfCon.groupby('계정과목')['전표금액(기준통화)'].sum()
dfGroup.to_excel("GL Recon.xlsx")

from spotlight.common.common import obj2str

def obj2str(df:pd.DataFrame) -> None:
    #df를 받아서, object인 columns을 모두 string으로 변경해줌
    for column in df.columns:    
        if df[column].dtype == 'object':
            df[column] = df[column].astype(str) # Call by Object Refenece이므로 Return 불필요    

obj2str(dfCon)

dfCon.to_parquet("lse_tmp.parquet")

#Column 갈아끼우기
#추후 구현

dfCon.columns

#전표번호 별로 차대변금액이 일치하는지 확인
dfTmp1 = dfCon.groupby('전표번호')['전표금액'].sum()
dfTmp1[dfTmp1 != 0].count()
#25567개 전표. pass 중요하지 않음

#전표번호 별로 전기일자는 1개만 존재하는지 확인
dfTmp2 = dfCon.groupby('전표번호')['전기일자'].nunique()
dfTmp2[dfTmp2 != 1]

#전표번호 별로 작성일자는 1개만 존재하는지 확인
dfTmp3 = dfCon.groupby('전표번호')['작성일자'].nunique()
dfTmp3[dfTmp3 != 1]

#전표번호 별 작성자가 동일한지
dfTmp4 = dfCon.groupby('전표번호')['작성자ID'].nunique()
dfTmp4[dfTmp4 != 1].count()
#1876개

#작성자ID 모든 라인에 값이 있는가?
dfCon[dfCon['작성자ID'].isna()]


#대상기간을 벗어나는 날짜가 있는지 확인
dfCon['전기일자'].min()
dfCon['전기일자'].max()

tmp = pd.to_datetime(dfCon['전기일자'], format = "%Y.%m.%d")
tmp[tmp > '2023-09-30'].count()

#COLUMN 교체
from spotlight.common.common import autoMap

dfCon.to_parquet('temp.parquet')