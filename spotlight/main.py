import pandas as pd

from spotlight.read import runReadColumnLength
from spotlight.txt2db import runTxt2Db
from spotlight.concatText import runConcatText
from spotlight.import2df.import2df import runImport2Df
from spotlight.save.save import Saver
from spotlight.automap.automap import AutoMap

class Spotlight:

    df:pd.DataFrame

    def run(cls):

        text =  "\n#"*10+"\n"
        text += "\nPreprocessing\n"    
        text += "11. Excel to Text\n"    
        text += "12. concatenate text\n"    

        text += "\nUSE SQL\n"    
        text += "21. To Insert to SQL, Read columns'length\n"
        text += "22. Create Table => with mySQL\n"
        text += "23. Import file and Insert to DB\n"

        text += "\nMain Run\n"            
        text += "31. Read text to dataframe\n"
        text += "32. Auto_MAP\n"
        text += "33. Modify mode(After Auto_MAP)\n" #조정자는 별도 클래스로 분리 #아직 미구현        

        text += "\nSave\n"            
        text += "41. Save text(임시파일 Load는 31 활용)\n"

        text += "90. MANUAL HANDLING - DEBUG\n"
        text += "99. df.head(10)"

        #####
        textMain = "enter '?' to help / 'q' to exit"

        while True:

            print("") #여기다 BREAK를 걸면 디버깅

            print(textMain)
            flag = input(">>")

            match flag:
                case '?': print(text)
                case 'q': print("END"); break
                
                case '11': print("USE VBA...(추후 연동예정)")
                case '12': runConcatText()

                case '21': runReadColumnLength()
                case '22': print("USE mySQL")
                case '23': runTxt2Db()

                case '31': cls.df = runImport2Df()
                case '32': cls.df = AutoMap().autoMap(cls.df)

                case '41': Saver().save(cls.df)

                case '90':
                    print("DEBUG NOW") #여기다 BREAKPOINT를 걸면 수기 디버깅가능
                case '99': print(cls.df.head(10))

                case _: print("Retry"); continue

def runMain(): 
    spot = Spotlight()
    spot.run()

if __name__=="__main__":
    runMain()
