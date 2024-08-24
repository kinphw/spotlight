import pandas as pd
from sqlalchemy import create_engine, Table, MetaData

# 예시 데이터

df = pd.read_csv("24년 상반기 총계정원장(수정)_피벗_sheet1.tsv", encoding='cp949', sep='\t', dtype="str")

# MySQL 연결 정보
db_connection_str = 'mysql+pymysql://root:genius@localhost:3306/test'
db_connection = create_engine(db_connection_str)

# DataFrame 구조를 바탕으로 테이블 정의
table_name = 'my_table'

# DataFrame 구조를 기반으로 테이블 생성
df.head(0).to_sql(table_name, con=db_connection, if_exists='replace', index=False)

print(f"Table '{table_name}' created successfully without inserting data!")