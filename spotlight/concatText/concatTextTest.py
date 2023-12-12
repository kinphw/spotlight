from spotlight.concatText.concatText import ConcatText
# 함수부

#TEST 목적 상속
class ConcatTextTest(ConcatText): #INHERIT

    def run(cls): #OVERIDE
        cls.getFiles("헤더 테스트할 텍스트파일이 있는 폴더 지정")
        #cls.filenameNew = input("new file name(result.txt)>>") or 'result.txt'                
        cls.encodingOld = input("encodingOld(cp949)>>") or 'cp949'
        #cls.encodingNew = input("encodingNew(utf8)>>") or 'utf8'

        # flag = input("헤더가 포함되어 있습니까?(기본값 Y). Y인 경우 첫번째 파일만 포함함)>>") or 'Y'
        # if flag == 'Y': cls.bHeader = True
        # else: cls.bHeader = False
        cls.concat()
        print("DONE")

    def concat(cls, bHeader:bool = None): #OVERRIDE        
        print("총",len(cls.liTgt),"개 파일에 대해 헤더 순환출력")        
        for file in cls.liTgt:                                              
            fileOld = open(file, 'rt', encoding=cls.encodingOld)
            print(file+"",end=":\n")
            print(fileOld.readline())
            fileOld.close()