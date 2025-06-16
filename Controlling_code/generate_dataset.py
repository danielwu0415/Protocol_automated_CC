import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from findpeaks import findpeaks
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import os
from tqdm import tqdm
import heapq
file_path=r'Processed_data'
file_names = os.listdir(file_path)

threshold=20

def find_peak(x,find_number=1):
    max_index=np.argmax(x)
    max_value=np.max(x)
    all_core=[]
    all_core_length=[]
    if max_value<20:
        return []
    else:
        core_index=np.where((x>max_value-20))[0]
        for core in core_index:
            if len(np.where(x[0:core]<threshold)[0])!=0:
                left_bound=np.where(x[0:core]<threshold)[0][-1]
            else:
                continue
            if len(np.where(x[core:]<threshold)[0])!=0:
                right_bound=np.where(x[core:]<threshold)[0][0]+core
            else:
                continue
            if [left_bound,right_bound] not in all_core:
                all_core.append([left_bound,right_bound])
                all_core_length.append(right_bound-left_bound)
        if len(all_core_length)!=0:
            best_peak_index = list(map(all_core_length.index, heapq.nlargest(find_number, all_core_length)))
            best_peak=[]
            for bp in best_peak_index:
                best_peak.append(all_core[bp])
        else:
            best_peak=[]
        return best_peak

    # print(all_core)
    # print(max_value,max_index)

def draw_peak(x,best_peak,save_name):
    plt.figure()
    plt.plot(x)
    plt.ylim([-5, 105])
    if len(best_peak) != 0:
        for peak in best_peak:
            plt.scatter(peak, x[peak], color='red')
            plt.vlines(peak[0],ymin=0,ymax=100,linestyles='--',color='red')
            plt.vlines(peak[1], ymin=0, ymax=100,linestyles='--',color='red')
    else:
        plt.text(int(x.shape[0]/2),90,'No absorption or not end',verticalalignment="top",horizontalalignment="right",color='red')



    plt.savefig('fig_save/' + save_name + '.png')
    plt.clf()
    #plt.show()

def save_fig():
    for file_name in tqdm(file_names):
        file=pd.read_excel(file_path+'/'+file_name)
        AU1=file['AU1'].dropna()
        AU1[AU1<0]=0
        x=np.array(AU1)
        best_peak = find_peak(x, find_number=1)
        draw_peak(x,best_peak,file_name)

def identify_time():
    data_file=pd.read_excel('dataset.xlsx')
    file_names=data_file['Ending time'].values
    t1=data_file['t1'].values
    t2=data_file['t2'].values
    for index in tqdm(range(len(file_names))):
        file_name=file_names[index]

        if type(file_name).__name__=='str':
            if np.isnan(t1[index])==True or np.isnan(t2[index])==True:
                try:
                    file = pd.read_excel(file_path + '/' + file_name+'.xlsx')
                    AU1 = file['AU1'].dropna()
                    AU1[AU1 < 0] = 0
                    x = np.array(AU1)
                    best_peak = find_peak(x, find_number=1)
                    if len(best_peak)!=0:
                        t1[index]=best_peak[0][0]
                        t2[index]=best_peak[0][1]
                    else:
                        t1[index] = -1
                        t2[index] = -1
                except OSError:
                    continue

    data_file['t1']=t1
    data_file['t2']=t2
    data_file.to_excel('dataset.xlsx')




identify_time()





