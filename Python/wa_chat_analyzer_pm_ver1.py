import re #pip install regex
import io
import os
import glob
import sys
import pandas as pd #pip install pandas
import numpy as np #pip install numpy
from datetime import datetime #pip install DateTime
from dateutil import parser #pip install python-dateutil
import warnings 
warnings.filterwarnings('ignore')


# read the file
os.chdir(r'.')
myFiles = glob.glob('*.txt')

number_file = []
file_name = []

for num in range(1,len(myFiles)+1):
    number_file.append(num)
for files in myFiles:
    file_name.append(files)

dic_files = dict(zip(number_file,file_name))
for key, value in dic_files.items():
    print(key, ' : ', value)

date_from = str(input('From YYYY-MM-DD:'))
date_end = str(input('To YYYY-MM-DD:'))

for num, f_name in dic_files.items():  
    file_name = str(f_name)
    with io.open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
    # extract the datetime from chat
    # extract phone number that have conversation (end with ':')
    date = []
    count = []
    for line in lines:
        dt = re.split(r'[-:]',line)[0].replace('.',':')
        n_hp = ",".join(str.split(line)[3:]).replace(',',' ')
        if re.search(r'(\d+/\d+/\d+)',dt) != None and re.search(':', n_hp) != None and re.search('This message was deleted',n_hp) == None and re.search('Pesan ini telah dihapus',n_hp) == None and re.search('Anda telah menghapus pesan ini',n_hp) == None:
            timestamp = parser.parse(dt, dayfirst=True)
            ex_hp = re.split(r':',n_hp)[0]
            date.append(timestamp)
            count.append(ex_hp)
        else:
            date.append(datetime.now())
            count.append(None)
    df = pd.DataFrame({'date':date, 'count':count })
    df.set_index('date',drop= True, inplace= True)
    df = df[date_from:date_end]
    
    #date generator
    date_gen = pd.date_range(start= date_from, end= date_end).to_frame()
    date_gen.rename(columns = {0:'day_name'}, inplace=True)
    date_gen['day_name'] = pd.to_datetime(date_gen.index).date 
    date_gen['day_name'] = date_gen['day_name'].map(str) + ' (' + date_gen.index.day_name().map(str) + ')'

    #unique user group by date
    cnt =  df.groupby(df.index.date)['count'].nunique()
    cnt = cnt.to_frame()

    #left join date and fill null value with 0
    data = date_gen.join(cnt).fillna(0)
    rmv_txt = file_name.replace('.txt', '')
    data.to_excel(f'PM-{rmv_txt}.xlsx',index=True)

print('Program Sukses Boss !!')