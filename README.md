# SPOTLIGHT

## Ver

v0.0.76

## 목적

정형화된 전처리 반자동화

## 작동방법

pip install spotlighter  
import spotlight as sl  
sl.run()  

## 주요기능

1. 전처리

* Excel to Text  
* concatenate text  
* check text header (TEST)    
* Merge Text (i.e. BSEG+BKPF) (if already set df, automatically transferred to dfA)    

2. DF to SQL(IMPORT)

* Import file and Insert to DB (a single file or multiple files in the specific folder)
* To Insert to SQL, Read columns'length  

3. MAIN RUN 

* Read text to dataframe  
* Auto_MAP : MAP_GL.xlsx 파일을 활용하여 columns 자동 매핑 + 추가  
* Modify mode(After Auto_MAP)  
* To recon G/L and T/B, export SUM(AMT LC)groupby Acct  

3-1. MODIFY MOD

3-1-1. 전처리-전표금액

* replace string (Kill comma, space, regex etc.)  
* Apply DC (차변은 +, 대변은 - 처리)  
* To Minus () or - : 문자열 () 또는 후위-인 경우 마이너스로 변환  
* Multiple 100  : 곱하기 100  
* FROM 전표금액 TO 차대금액  : signed 전표금액에서 unsigned 차변/대변을 생성한다.  
* FILLNA(0)  : N/A를 0으로 채운다.  
* 자동수동 : 특정 컬럼값(전표성격, 사용자 등)이 특정 문자열(복수 가능)을 포함하는 행을 A로 지정  

3-1-2. 전처리-기타

* drop a column  
* drop duplicate  
* Change column name  
* Change column datatype  
 
4. SAVE TO..

* Save text  
* Save a part of df(특정 계정과목 추출 등)  

5. 일반기능

* MANUAL HANDLING - DEBUG  
* df.info()  
* df.head(30) (like R's View())

## Help
박형원

## History

v0.0.1 DD 231218  
v0.0.2 DD 240117 : 추가 : 탭/개행 삭제기능, sum기능, head to excel 추출, 계정별/월별 금액 추출, Modin사용 import/export  
v0.0.3 DD 240119 : breakpoint 추가  
v0.0.4 DD 240120 : minor patch  
v0.0.5 DD 240121 : save split (text or excel) 기능추가 / DF에서 추출하거나 아니면 직접 텍스트에서 추출함  
v0.0.6 240125 : FROM 전표금액 TO 차대금액 추가 / 차대처리시 숫자 자료형 처리가능하게 변경  
v0.0.7 : 유일성검증기능 추가  
v0.0.71 : read_csv debug (quote)  
v0.0.72 : AUTO_MAP 취소시 loaded df 사라지는 버그 해결 / 정규식 수정 오타수정 / 비정규식 replace 기능 추가  
v0.0.73 : user-define groupby  
v0.0.732 : dtype을 기본적으로 string으로 읽는다. (데이터 손실 방지)  
v0.0.733 : data import시 quote 선택받도록 변경  
v0.0.74 : excel to tsv 연계 형변환 지원  
v0.0.76 : R의 View() 구현, DB Insert 고도화