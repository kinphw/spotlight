import pandas as pd

from spotlight.read import runReadColumnLength
from spotlight.txt2db import runTxt2Db
from spotlight.concatText import runConcatText
from spotlight.concatText.concatTextTest import ConcatTextTest
from spotlight.import2df.import2df import runImport2Df
from spotlight.save.save import Saver
from spotlight.save.savePart import SaverPart
from spotlight.save.saveSplit import SaverSplit
from spotlight.save.saveSplitFrText import SaverSplitFrText
from spotlight.automap.automap import AutoMap
from spotlight.modify.modify import Modifier
from spotlight.recon.recon import ReconGL
from spotlight.recon.calSum import CalSum
from spotlight.recon.pivot import PivotMonthAcct
from spotlight.recon.groupby import GroupbyUserDefine
from spotlight.recon.uniq import UniqueValidator

from spotlight.merge.merge import Merger
from spotlight.common.colors import Colors
from spotlight.common.protoSelector import ProtoABSSelector
from spotlight.common.ErrRetry import ErrRetryF

class Spotlight(ProtoABSSelector):
    df:pd.DataFrame    
    def run(self):

        print(Colors.RED + "Spotlight : v0.0.731" + Colors.END)

        text =  "#"*10+"\n"
        text += Colors.RED + "\nPreprocessing\n" + Colors.END
        text += "11. Excel to Text\n"    
        text += "12. concatenate text\n"    
        text += "13. check text header (TEST)\n"    
        text += "14. Merge or Concat Text (i.e. BSEG+BKPF) (if already set df, automatically transferred to dfA)\n"        

        text += Colors.RED + "\nUSE SQL\n" + Colors.END
        text += "21. To Insert to SQL, Read columns'length\n"
        text += "22. Create Table => with mySQL\n"
        text += "23. Import file and Insert to DB\n"

        text += Colors.RED + "\nMain Run\n" + Colors.END
        text += "31. Read text to dataframe\n"
        text += "32. Auto_MAP\n"
        text += "33. Modify mode\n"
        text += "34. To recon G/L and T/B, export SUM(AMT LC)groupby Acct\n"
        text += "35. export pivot table(ex. 월별/계정별, 계정별/차대별 등등..)\n" #240127 : 기능은 동일하나 설명을 변경
        text += "36. User-defined groupby (sum or count) \n"        
        text += "37. Calculate Sum a specific column (합계검증목적)\n" #240117
        text += "38. Uniqueness validation (유일성검증)\n" #240127

        text += Colors.RED + "\nSave\n" + Colors.END
        text += "41. Save text(임시파일 Load는 31 활용)\n"
        text += "42. Save a part of df(특정 계정과목 추출 등)\n"      
        text += "43. Save df spiltted(일정 길이로 분할하여 저장) FROM Dataframe\n"
        text += "44. Save text spiltted(텍스트를 바로 읽어서 일정 길이로 분할하여 저장) FROM Text\n"

        text += Colors.RED + "\nGeneral\n" + Colors.END
        text += "90. MANUAL HANDLING - DEBUG (USE self.df)\n"
        text += "91. df.info()\n"        
        text += "92. df.head(10)\n"
        text += "93. df.head(10) to_excel export\n"

        #####
        textMain = Colors.RED + "MAIN MODE : enter '?' to help / 'q' to exit" + Colors.END

        while True:

            print(textMain)
            flag = input(">>")

            match flag:
                case '?': print(text)
                case 'q': print("END"); break
                
                case '11': print("USE VBA...(추후 연동예정)")
                case '12': runConcatText()
                case '13': ConcatTextTest().run()
                case '14': 
                    if isinstance(self.df, pd.DataFrame): self.df = Merger(self.df).run()
                    else: self.df = Merger().run()

                case '21': runReadColumnLength()
                case '22': print("USE mySQL")
                case '23': runTxt2Db()

                case '31': self.df = runImport2Df()
                case '32': self.df = AutoMap().autoMap(self.df)
                case '33': self.df = Modifier(self.df).run() #240120
                case '34': ReconGL(self.df).run()
                case '35': PivotMonthAcct(self.df).run()
                case '36': GroupbyUserDefine(self.df).run()
                case '37': CalSum(self.df).run() #240117 추가
                case '38': UniqueValidator(self.df).run() #240127 추가

                case '41': Saver(self.df).run()
                case '42': SaverPart(self.df).run()   
                case '43': SaverSplit(self.df).run() #240121 추가
                case '44': SaverSplitFrText().run() #240121 추가

                case '90': breakpoint() #240119
                case '91': self.df.info()
                case '92': print(self.df.head(10))
                case '93': self._head2excel()
                case _: print("Retry"); continue

    @ErrRetryF
    def _head2excel(self):
        self.df.head(10).to_excel("view.xlsx") ; print("view.xlsx 추출완료")

def run(): 
    spot = Spotlight()
    spot.run()



if __name__=="__main__":
    run()
