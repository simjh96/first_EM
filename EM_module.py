import numpy as np
import pandas as pd
import random

class Em():
    """
    2^3 cell prob

    p1s = [p(--1), p(1--|--1), p(1--|--0), p(-1-|1-1), p(-1-|1-0), p(-1-|0-1), p(-1-|0-0)]
    p0s = 1 - p1s

    weights
    Kw1s = [p(-1-|1-1), p(-1-|1-0), p(-1-|0-1), p(-1-|0-0)]
    Kw0s = 1 - Kw1s

    Kw1s.T @ K = pkeK1
    Kw0s.T @ K = pkeK0

    Lw1s = [p(1--|-11), p(1--|-10), p(1--|-01), p(1--|-00)]
    Lw0s = 1 - Lw1s

    Lw1s.T @ L = pkeL1
    Lw0s.T @ L = pkeL0
    """
    def __init__(self):

        #data
        self.H = [293, 4, 176, 3, 23, 2, 197, 17]
        self.K = [100, 5, 82, 6]
        self.L = [90, 5, 150, 10]

        #prime index
        self.pkH = ['111','110','101','100','011','010','001','000']

        self.pkK = ['11','10','01','00']
        self.pkeK1 = ['111','110','011','010']
        self.pkeK0 = ['101','100','001','000']
        
        self.pkL = ['11','10','01','00']
        self.pkeL1 = ['111','110','101','100']
        self.pkeL0 = ['011','010','001','000']

        #record prob by time
        self.p = []

        #initial weights
        self.Kw1s = np.array([0.5,0.5,0.5,0.5])
        self.Kw0s = 1 - self.Kw1s
        self.Lw1s = np.array([0.5,0.5,0.5,0.5])
        self.Lw0s = 1 - self.Lw1s

        #df for H K L
        self.df_H = pd.DataFrame(self.H, index = self.pkH, columns = ['H'])
        self.df_K = pd.DataFrame(self.K, index = self.pkK)
        self.df_L = pd.DataFrame(self.L, index = self.pkL)


    #methods
    def make_current_estimated_df(self):
        print("system>>> merging data frame")
        self.df_eK = pd.DataFrame((self.df_K.iloc[:,0]*self.Kw1s).tolist(), index = self.pkeK1).append(pd.DataFrame((self.df_K.iloc[:,0]*self.Kw0s).tolist(), index = self.pkeK0))
        self.df_eK.columns = ['eK']
        self.df_eL = pd.DataFrame((self.df_L.iloc[:,0]*self.Lw1s).tolist(), index = self.pkeL1).append(pd.DataFrame((self.df_L.iloc[:,0]*self.Lw0s).tolist(), index = self.pkeL0))
        self.df_eL.columns = ['eL']
        self.df_curr = self.df_H.join(self.df_eK).join(self.df_eL)
        
    def update_w1s(self):
        print("system>>> updating weight")
        self.Kw1s[0] = sum(self.df_curr.loc['111',:])/(sum(self.df_curr.loc['111',:])+sum(self.df_curr.loc['101',:]))
        self.Kw1s[1] = sum(self.df_curr.loc['110',:])/(sum(self.df_curr.loc['110',:])+sum(self.df_curr.loc['100',:]))
        self.Kw1s[2] = sum(self.df_curr.loc['011',:])/(sum(self.df_curr.loc['011',:])+sum(self.df_curr.loc['001',:]))
        self.Kw1s[3] = sum(self.df_curr.loc['010',:])/(sum(self.df_curr.loc['010',:])+sum(self.df_curr.loc['000',:]))
        self.Kw0s = 1 - self.Kw1s

        self.Lw1s[0] = sum(self.df_curr.loc['111',:])/(sum(self.df_curr.loc['111',:])+sum(self.df_curr.loc['011',:]))
        self.Lw1s[1] = sum(self.df_curr.loc['110',:])/(sum(self.df_curr.loc['110',:])+sum(self.df_curr.loc['010',:]))
        self.Lw1s[2] = sum(self.df_curr.loc['101',:])/(sum(self.df_curr.loc['101',:])+sum(self.df_curr.loc['001',:]))
        self.Lw1s[3] = sum(self.df_curr.loc['100',:])/(sum(self.df_curr.loc['100',:])+sum(self.df_curr.loc['000',:]))
        self.Lw0s = 1 - self.Lw1s

    def get_curr_p(self):
        p_list = []
        p_index = ['p(--1)', 'p(1--|--1)', 'p(1--|--0)', 'p(-1-|1-1)', 'p(-1-|1-0)', 'p(-1-|0-1)', 'p(-1-|0-0)']
        p_list.append(self.df_curr.iloc[[0,2,4,6],:].sum().sum()/self.df_curr.sum().sum())
        p_list.append(self.df_curr.iloc[[0,2],:].sum().sum()/self.df_curr.iloc[[0,2,4,6],:].sum().sum())
        p_list.append(self.df_curr.iloc[[1,3],:].sum().sum()/self.df_curr.iloc[[1,3,5,7],:].sum().sum())
        p_list.append(self.df_curr.iloc[[0],:].sum().sum()/self.df_curr.iloc[[0,2],:].sum().sum())
        p_list.append(self.df_curr.iloc[[1],:].sum().sum()/self.df_curr.iloc[[1,3],:].sum().sum())
        p_list.append(self.df_curr.iloc[[4],:].sum().sum()/self.df_curr.iloc[[4,6],:].sum().sum())
        p_list.append(self.df_curr.iloc[[5],:].sum().sum()/self.df_curr.iloc[[5,7],:].sum().sum())
        return pd.DataFrame(p_list, index = p_index)

    def get_curr_p0(self):
        p_list = []
        p_index = ['p(111)', 'p(110)', 'p(101)', 'p(100)', 'p(011)', 'p(010)', 'p(001)','p(000)']
        p_list.append(self.df_curr.iloc[0,:].sum().sum()/self.df_curr.sum().sum())
        p_list.append(self.df_curr.iloc[1,:].sum().sum()/self.df_curr.sum().sum())
        p_list.append(self.df_curr.iloc[2,:].sum().sum()/self.df_curr.sum().sum())
        p_list.append(self.df_curr.iloc[3,:].sum().sum()/self.df_curr.sum().sum())
        p_list.append(self.df_curr.iloc[4,:].sum().sum()/self.df_curr.sum().sum())
        p_list.append(self.df_curr.iloc[5,:].sum().sum()/self.df_curr.sum().sum())
        p_list.append(self.df_curr.iloc[6,:].sum().sum()/self.df_curr.sum().sum())
        p_list.append(self.df_curr.iloc[7,:].sum().sum()/self.df_curr.sum().sum())
        return pd.DataFrame(p_list, index = p_index)

    def test_HKL(self):
        print("system>>> back checking start...")
        print("system>>> p0 = [0.1,0.4,0.2,0.05,0.02,0.1,0.12,0.01]")
        self.H = np.random.multinomial(2000, [0.1,0.4,0.2,0.05,0.02,0.1,0.12,0.01],size=1)[0]
        self.K = np.random.multinomial(2000, [0.1,0.4,0.2,0.05,0.02,0.1,0.12,0.01],size=1)[0]
        self.L = np.random.multinomial(2000, [0.1,0.4,0.2,0.05,0.02,0.1,0.12,0.01],size=1)[0]

        self.K = [self.K[0]+self.K[2],self.K[1]+self.K[3],self.K[4]+self.K[6],self.K[5]+self.K[7]]
        self.L = [self.L[0]+self.L[4],self.L[1]+self.L[5],self.L[2]+self.L[6],self.L[3]+self.L[7]]
        self.df_H = pd.DataFrame(self.H, index = self.pkH, columns = ['H'])
        self.df_K = pd.DataFrame(self.K, index = self.pkK)
        self.df_L = pd.DataFrame(self.L, index = self.pkL)


    def run(self, iter):
        self.make_current_estimated_df()
        print("system>>> ready...")
        print(self.df_curr)
        print("system>>> run...")

        for i in range(iter):    
            # print("system>>> {}th trial".format(i))
            old_Kw1s = self.Kw1s.copy()
            old_Lw1s = self.Lw1s.copy()
            self.update_w1s()    
            self.make_current_estimated_df()
            self.p.append([i,self.get_curr_p()])
            # print(self.df_curr.sum().sum())
            # print("system>>> abs change : K:{}, L:{}".format(sum(abs(old_Kw1s-self.Kw1s)),sum(abs(old_Lw1s-self.Lw1s))))

        print("system>>> finished")

if __name__ == "__main__":
    em = Em()
    # em.run(10)
    # print(em.df_curr)
    # print(em.p[4])
    # print(em.get_curr_p0)

#i python code
# import os
# os.chdir("C:\\EM_mid")
# from EM_module import Em
# em = Em()

#simulation result
#set p = [0.1,0.4,0.2,0.05,0.02,0.1,0.12,0.01]
#iter = 100
# p(111)	0.099057
# p(110)	0.390393
# p(101)	0.208457
# p(100)	0.044688
# p(011)	0.019553
# p(010)	0.107853
# p(001)	0.120599
# p(000)	0.009399