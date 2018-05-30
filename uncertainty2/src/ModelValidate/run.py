# -*- coding: utf-8 -*-
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mashi as ms
import oushi as ou
import manhadun as mh
import qiebixuefu as qbxf
import xuangduishang as kl
import zhi as zi
import scipy.stats
import matplotlib.mlab as mlab


N = 10
n = 100
mm = 20
nnn = 4



#样本
m = []
for i in range(0, n):
   d = np.round(np.random.normal(6.0, 0.4, N),nnn)
   m.append(d)
   # print d
 #print ("sdsdsddsd")
#print(m)
#仿真
z = []
for i in range(0, mm):
#    d =np.round(np.random.uniform(0.1*i,0.11*i,N),nnn)
 d = np.round(np.random.normal(18.0, 0.4, N), nnn)
 z.append(d)
 y = z[0]
#or i in range(0,100):
   # m[i] = np.random.random(10)
    #print(m[i])

# 马氏距离要求样本数要大于维数，否则无法求协方差矩阵
#print map(list,zip(*m))





##########################################q

###########################################
#

#####################
#求欧式距离
#####################

#dd1 = []

#print("欧式距离")

#print(d1)
###########################


#print("曼哈顿距离")
#print(d2)

#################################

#print(d3)



###############################################



#############################################

##############################################




###########################################





########################################


################################

#plt.ylabel("ylabel")
#plt.xlabel("xlabel")  # 我们设置横纵坐标的标题。

#plt.title("马氏距离")
