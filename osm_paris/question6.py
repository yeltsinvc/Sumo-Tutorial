# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 17:32:51 2018

@author: a022927
"""

from xml2csv_multi import *
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
data_dir = r'path_to\duaiterate_result' # need to modify 
files_name  = [f for f in os.listdir(data_dir) if f.startswith('tripinfo') and f.endswith('.xml')]

list_mean_waiting_time = []
for i in files_name:
    output_file_name = i.split('.')[0] + '.csv'
    main(i, data_dir)
    df_tripinfo = pd.read_csv(data_dir+'\\' + output_file_name, sep=';')[['tripinfo_waitingTime', 'tripinfo_departDelay']].mean()
    list_mean_waiting_time.append(df_tripinfo['tripinfo_waitingTime'])


plt.plot(list_mean_waiting_time[0:10])
plt.ylabel('average waiting time/s')
plt.show()