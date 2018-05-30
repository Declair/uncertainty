# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import scipy.stats
import zhi as zi
import pandas as pd
def KLdistanse(zz,mm5,mm6):
 mm = mm5
 y= []
 m = mm6
 z = zz
 for i in range(0, mm):
    y.append(m[i])
    i=i+1

 px = z / np.sum(z)
 py = y / np.sum(y)
#print(py)
 KL = scipy.stats.entropy(px, py)
 return KL

def figure_kl(z,mm,m):
 plt.figure("4")
 KL = KLdistanse(z,mm,m)
 ax9=plt.subplot(221)#在图表2中创建子图1
 s2 = pd.Series(np.array(KL))
 data1 = pd.DataFrame({"KL": s2})
 plt.title("KL")
 num_list5 = zi.Orang(KL,len(KL))
 data1.boxplot()  # 这里，pandas自己有处理的过程，很方便哦。
 ax10=plt.subplot(222)
 name_list = ['sum','var','1/4','3/4','median']
 plt.title("data")
 plt.bar(range(len(num_list5)), num_list5,color='black',tick_label=name_list)
 plt.show()