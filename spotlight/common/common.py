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

def autoMap(df:pd.DataFrame)->pd.DataFrame :

    print("Auto Mapping. Read ImportMAP.xlsx")
    #filenameImportMap = "ImportMAP.xlsx"
    #filenameImportMap = glob.glob(tgtdir+"/"+filenameImportMap)
    filenameImportMap = myfd.askopenfilename("MAP파일 선택")    
    dfMap = pd.read_excel(filenameImportMap, sheet_name='MAP_GL')

    ## a. MAP 대상 먼저 전처리
    dfMapMap = dfMap[dfMap['방법'] == 'MAP']
    dfTB = pd.DataFrame()
    for i in range(0, dfMapMap.shape[0]):    
        try:
            dfTB[dfMapMap.iloc[i]["tobe"]] = df[dfMapMap.iloc[i]["asis"]]
        except:
            dfTB[dfMapMap.iloc[i]["tobe"]] = df[str(dfMapMap.iloc[i]["asis"])]

    ## b. KEYIN 대상 추가 전처리
    dfMapKeyin = dfMap[dfMap['방법'] == 'KEYIN']

    for i in range(0, dfMapKeyin.shape[0]):        
        dfTB[dfMapKeyin.iloc[i]["tobe"]] = dfMapKeyin.iloc[i]["asis"]


    print("AUTO-MAP Done")
    return dfTB            