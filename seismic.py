#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 12:38:06 2020

@author: guillaume
"""


from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.cm as cmx
from time import process_time
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cmx
import matplotlib.colors
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import LabelEncoder

def scatter(x,y, cs, colorsMap='jet'):
    #si=[n**3 for n in cs]
    cm = plt.get_cmap(colorsMap)
    cNorm = matplotlib.colors.Normalize(vmin=min(cs), vmax=max(cs))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    #fig = plt.figure()
    plt.scatter(x, y, c=scalarMap.to_rgba(cs),marker='o',s=5)
    scalarMap.set_array(cs)
    #fig.colorbar(scalarMap)
    plt.show()

def clust_geo(x,y,delta_d):
    X=[]
    for n in range(0,len(x)) :
            X+=[[x[n],y[n]]]   
    X=np.array(X)        
    clustering = DBSCAN(eps=delta_d, min_samples=1).fit(X)
    lab_d=clustering.labels_
    clust_d = len(set(lab_d)) - (1 if -1 in lab_d else 0)
    return lab_d,clust_d

def clust_temp(sec,delta_t):
    lab_t=[0]
    n=0
    for t in range(0,len(sec)-1):
      if abs(sec[t]-sec[t+1])<delta_t:
        lab_t+=[n]
      else : 
        n+=1
        lab_t+=[n]
    clust_t=n+1
    return lab_t,clust_t

def seismic_clust(data, delta_d, delta_t,min_clust,max_clust) :
  start_time = process_time()
    
  [lab_d,clust_d]=clust_geo(data.p0, data.p1, delta_d)
  
  [lab_t,clust_t]=clust_temp(data.sec,delta_t)
  
  dt=[str([lab_d[n],lab_t[n]]) for n in range(0,len(lab_t))] 

  data["label"]=dt

  label_encoder = LabelEncoder()
  data['label']= label_encoder.fit_transform(data['label']) 
  
  data = data.reset_index(drop=True)

  clust_tot=len(data['label'].unique())
  
  print("clusters spatiaux :",clust_d)
  print("clusters temporels :",clust_t)
  print("clusters : "+str(clust_tot)+" ("+str(round(100*(1-(clust_tot/(clust_d*clust_t))),2))+"% de fusion)")

  lab=data.groupby(['label']).size().to_dict()
  
  def card_lab(label):
      return lab.get(label)
  
  data['card']=data['label'].apply(card_lab)
  
  back=data.loc[data['card'] <= min_clust] 
  main=data.loc[(data['card'] > min_clust) & (data['card'] < max_clust)] 
  
  print("sequence : "+str(len(main))+" points en "+str(len(main["label"].unique()))+" clusters")
  print("background : "+str(len(back))+" points en "+str(len(back["label"].unique()))+" clusters")
  print ("duration : "+str(round(process_time() - start_time,2))+ " seconds")
  
  return data,back,main

def get_seq(data,label,path):
    data=data[data["label"]==label]
    data.to_csv(r''+path+'label_'+str(label)+'.txt', header=True, sep='\t')
    print("Saved to"+path+'label_'+str(label)+'.txt')
    return data

if __name__ == '__main__':
    
    data = pd.read_csv('ReNaSS_1980-2011_full.txt', sep='\t')
    delta_d=2000
    delta_t=43200#259200
    min_clust,max_clust=10,30000
    
    data,back,main=seismic_clust(data,delta_d, delta_t,min_clust,max_clust)
    
    maxi_main= main.groupby(['label'], sort=False)['mag'].idxmax()
    main_filtred=main.loc[maxi_main]
    
    scatter(back.p0,back.p1,back.label)
    plt.figure()
    scatter(main.p0,main.p1,main.label)
    plt.figure()
    plt.scatter(back.sec,back.mag)
    plt.scatter(main_filtred.sec,main_filtred.mag)
    plt.show()

    path="/home/guillaume/Bureau/"
    seq=get_seq(main,220,path)


