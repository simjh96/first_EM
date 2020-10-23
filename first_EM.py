import numpy as np
import pandas as pd
import math
    """
    2^3 cell prob

    p1s = [p(--1), p(1--|--1), p(1--|--0), p(-1-|1-1), p(-1-|1-0), p(-1-|0-1), p(-1-|0-0)]
    p0s = 1 - p1s

    weights
    Kw1s = [p(-1-|1-1), p(-1-|1-0), p(-1-|0-1), p(-1-|0-0)]
    Kw0s = 1 - Kw1s

    Kw1s.T %@% K = pkeK1
    Kw0s.T %@% K = pkeK0

    Lw1s = [p(1--|-11), p(1--|-10), p(1--|-01), p(1--|-00)]
    Lw0s = 1 - Lw1s

    Lw1s.T %@% L = pkeL1
    Lw0s.T %@% L = pkeL0

    """

H = [293, 4, 176, 3, 23, 2, 197, 17]
pkH = ['111','110','101','100','011','010','001','000']
df_H = pd.DataFrame(H, index = pkH, columns = ['H'])

K = [100, 5, 82, 6]
Kw1s = np.array([0.5,0.5,0.5,0.5])
Kw0s = 1 - Kw1s

pkK = ['11','10','01','00']
pkeK1 = ['111','110','011','010']
pkeK0 = ['101','100','001','000']
df_K = pd.DataFrame(K, index = pkK)
df_eK = pd.DataFrame((df_K.iloc[:,0]*Kw1s).tolist(), index = pkeK1).append(pd.DataFrame((df_K.iloc[:,0]*Kw0s).tolist(), index = pkeK0))
df_eK.columns = ['eK']



L = [90, 5, 150, 10]
Lw1s = np.array([0.5,0.5,0.5,0.5])
Lw0s = 1 - Lw1s

pkL = ['11','10','01','00']
pkeL1 = ['111','110','101','100']
pkeL0 = ['011','010','001','000']
df_L = pd.DataFrame(L, index = pkL)
df_eL = pd.DataFrame((df_L.iloc[:,0]*Lw1s).tolist(), index = pkeL1).append(pd.DataFrame((df_L.iloc[:,0]*Lw0s).tolist(), index = pkeL0))
df_eL.columns = ['eL']

df_final = df_H.join(df_eK).join(df_eL)

def make_current_estimated_df(H,K,L):
    df_eK = pd.DataFrame((df_K.iloc[:,0]*Kw1s).tolist(), index = pkeK1).append(pd.DataFrame((df_K.iloc[:,0]*Kw0s).tolist(), index = pkeK0))
    df_eK.columns = ['eK']
    df_eL = pd.DataFrame((df_L.iloc[:,0]*Lw1s).tolist(), index = pkeL1).append(pd.DataFrame((df_L.iloc[:,0]*Lw0s).tolist(), index = pkeL0))
    df_eL.columns = ['eL']
    return df_H.join(df_eK).join(df_eL)
# E step
def update_Kw1s(current_weight, current_df):
    Kw1s[0] = sum(df_final.loc['111',:])/(sum(df_final.loc['111',:])+sum(df_final.loc['101',:]))
    Kw1s[1] = sum(df_final.loc['110',:])/(sum(df_final.loc['110',:])+sum(df_final.loc['100',:]))
    Kw1s[2] = sum(df_final.loc['011',:])/(sum(df_final.loc['011',:])+sum(df_final.loc['001',:]))
    Kw1s[3] = sum(df_final.loc['010',:])/(sum(df_final.loc['010',:])+sum(df_final.loc['000',:]))


for i in range(10):

    old_Kw1s = Kw1s.copy()
    old_Lw1s = Lw1s.copy()

    Kw1s[0] = sum(df_final.loc['111',:])/(sum(df_final.loc['111',:])+sum(df_final.loc['101',:]))
    Kw1s[1] = sum(df_final.loc['110',:])/(sum(df_final.loc['110',:])+sum(df_final.loc['100',:]))
    Kw1s[2] = sum(df_final.loc['011',:])/(sum(df_final.loc['011',:])+sum(df_final.loc['001',:]))
    Kw1s[3] = sum(df_final.loc['010',:])/(sum(df_final.loc['010',:])+sum(df_final.loc['000',:]))

    Lw1s[0] = sum(df_final.loc['111',:])/(sum(df_final.loc['111',:])+sum(df_final.loc['011',:]))
    Lw1s[1] = sum(df_final.loc['110',:])/(sum(df_final.loc['110',:])+sum(df_final.loc['010',:]))
    Lw1s[2] = sum(df_final.loc['101',:])/(sum(df_final.loc['101',:])+sum(df_final.loc['001',:]))
    Lw1s[3] = sum(df_final.loc['100',:])/(sum(df_final.loc['100',:])+sum(df_final.loc['000',:]))

    df_eK = pd.DataFrame((df_K.iloc[:,0]*Kw1s).tolist(), index = pkeK1).append(pd.DataFrame((df_K.iloc[:,0]*Kw0s).tolist(), index = pkeK0))
    df_eK.columns = ['eK']
    df_eL = pd.DataFrame((df_L.iloc[:,0]*Lw1s).tolist(), index = pkeL1).append(pd.DataFrame((df_L.iloc[:,0]*Lw0s).tolist(), index = pkeL0))
    df_eL.columns = ['eL']

    df_final = df_H.join(df_eK).join(df_eL)

    print(sum(abs(old_Kw1s-Kw1s)))


