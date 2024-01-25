import numpy as np
import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF
from spotlight.common.protoSelector import ProtoABSSelector

class CreateSigned(ProtoABSSelector):

    #df:pd.DataFrame
    #def __init__(self, df:pd.DataFrame): self.df = df
    #차대구분에 따라 (-)처리 : 변경컬럼선택 / 차대컬럼선택 / 차변구분자 선택 / 시행
    @ErrRetryF    
    def run(self, cNameSigned:str, cNameUnsignedD:str, cNameUnsignedC:str): 
        
        self.df[cNameUnsignedD] = self.df[cNameUnsignedD].astype('float64').fillna(0)
        self.df[cNameUnsignedC] = self.df[cNameUnsignedC].astype('float64').fillna(0)
        
        #Run
        print("SignedAmount = + UnsignedDebit - UnsignedCredit")
        self.df[cNameSigned] = self.df[cNameUnsignedD] + self.df[cNameUnsignedC]

        print("DONE")        
