import chardet
import csv
from typing import Tuple

from spotlight.common.protoSelector import ProtoABSSelector

class PreCheck(ProtoABSSelector):

    def run(self, fileName:str) -> Tuple[str, str]: #반환값1 : encoding, 반환값2 : separator
        
        # 샘플 크기 설정 (예: 1024 바이트)
        #fileName = myfd.askopenfilename()
        sample_size = 1024

        # 인코딩 추측 (파일의 일부분만 읽음)
        with open(fileName, 'rb') as file:
            raw_data = file.read(sample_size)  # 파일의 첫 1024바이트만 읽음
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        # 구분자 추측 및 파일 읽기 (파일의 일부분만 읽음)
        with open(fileName, 'r', encoding=encoding, newline='') as file:
            sample = file.read(sample_size)
            separator = csv.Sniffer().sniff(sample).delimiter

        # pandas로 데이터프레임 읽기
        # df = pd.read_csv(file, sep=separator, encoding=encoding)

        print(f"Detected encoding: {encoding}")
        print(f"Detected separator: {separator}")

        return encoding, separator
