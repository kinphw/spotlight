import pandas as pd
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

# Tkinter 애플리케이션 생성
class DataFrameViewer:

    root:tk.Tk

    def __init__(self, root, dataframe):
        self.root = root
        self.tree = ttk.Treeview(self.root, columns=list(dataframe.columns), show='headings')
        
        # 열 제목 설정
        for col in dataframe.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # 데이터 삽입
        for index, row in dataframe.iterrows():
            self.tree.insert("", "end", values=list(row))
        
        self.tree.pack(expand=True, fill='both')
        
        # 복사 기능 추가
        self.tree.bind("<Control-c>", self.copy_selection)
        self.tree.bind("<Control-a>", self.select_all)  # Bind Ctrl+A to select all items

    def copy_selection(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            selected_values = [self.tree.item(item)['values'] for item in selected_items]
            header_values = self.tree['columns']
            copied_text = '\t'.join(header_values) + '\n'  # Include header
            copied_text += '\n'.join(['\t'.join(map(str, values)) for values in selected_values])
            self.root.clipboard_clear()
            self.root.clipboard_append(copied_text)
            messagebox.showinfo("Copy", "Selected items copied to clipboard.")

    def select_all(self, event):
        self.tree.selection_set(self.tree.get_children())  # Select all items, including the header        

class DfViewer:

    df:pd.DataFrame
    root:tk.Tk
    
    def __init__(self, df:pd.DataFrame):
        self.df = df

    def run(self): #cnt : 조회할 행수
        
        if not self.validate(): return

        # 메인 애플리케이션 창 생성
        self.root = tk.Tk()
        self.root.title("DataFrame Viewer")
        self.setXY(0.8, 0.8)
        self.root.attributes('-topmost', True)

        # 데이터 프레임을 표시하는 객체 생성
        viewer = DataFrameViewer(self.root, self.df)

        # 애플리케이션 실행
        self.root.mainloop()

    def validate(self) -> bool:
        if not isinstance(self.df, pd.DataFrame):
            print("df가 설정되지 않았습니다.")
            return False
        return True

    def setXY(self, width:float, height:float) -> None:
        self.root.geometry(f"{int(width * self.root.winfo_screenwidth())}x{int(height * self.root.winfo_screenheight())}+50+50")
