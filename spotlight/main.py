from spotlight.read import runReadColumnLength
from spotlight.txt2db import runTxt2Db

from spotlight.concatText import runConcatText

def run():

    text = "1. Read Column Length\n"
    text += "2. Create Table => with mySQL\n"
    text += "3. Import file and Insert to DB\n"

    while True:
        print(text)
        flag = input(">>")
        match flag:
            case '1':
                runReadColumnLength()
            case '2':
                print("USE mySQL")
            case '3':
                runTxt2Db()
            case _:
                print("END")
                break

def preprocess():

    text = "Preprocessing\n"    
    text += "1. concatenate text\n"    

    while True:
        print(text)
        flag = input(">>")
        match flag:
            case '1':
                runConcatText()
            case _:
                print("END")
                break

if __name__=="__main__":
    run()
