# -*- coding: utf-8 -*-

import numpy as np

#求 中位数 平均数 1/4  3/4 方差
def Orang(dd,nn):
  array = dd
  n = nn
  for i in range(0,n):
    for j in range(i):
        if array[j] > array[j + 1]:
            array[j], array[j + 1] = array[j + 1], array[j]

  narray=np.array(array)
  sum1=narray.sum()
  narray2=narray*narray
  sum2=narray2.sum()
  mean=sum1/n
  varo=sum2/n-mean**2##
  sumo = sum(array)/n##
#求中位数
  if n % 2 == 0:
    ozw = (array[n/2]+array[n/2-1])/2
  else:
    ozw = array[(n-1)/2]


#求上四分之一位
  if n%4 == 0:
    fouro1 = (array[n/4]+array[n/4-1])/2
    fouro3 = (array[(n/2+n)/2] + array[(n/2+n)/2-1]) / 2


  if n%4 == 1:
    fouro1 = (array[((n+1)/2+1)/2-1])
    fouro3 = (array[((n+1)/2+n)/2-1])

  ###
  if n%4 == 2:
    fouro1 = (array[(n/2+1)/2-1])
    fouro3 = (array[(n/2+1+n)/2-1]+array[(n/2+1+n)/2])/2
  if n%4 == 3:
    fouro1 = array[(n+1)/4-1]
    fouro3 = array[3*(n + 1)/4-1]

  return sumo,varo,fouro1,fouro3,ozw
