import pandas as pd
import numpy as np
import keras
import tensorflow as tf
from keras.preprocessing.sequence import TimeseriesGenerator
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from keras.models import load_model
from tkinter import *
from tkinter.ttk import Combobox
from keras.models import Sequential
from keras.layers import LSTM, Dense
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


date=[]
price=[]

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}
url="https://tr.investing.com/currencies/usd-try-historical-data"
r=requests.get(url,headers=headers)
soup=BeautifulSoup(r.content,"html.parser")
gelen_veri=soup.find("table",{"class":"genTbl closedTbl historicalTbl"})
a=gelen_veri.find_all("tr")
for i in range(1,len(a)):
    date.append(a[i].text.split('\n')[1])
    price.append(a[i].text.split('\n')[2].replace(",","."))

price=np.asarray(price)

def ekle(a):
    global price
    price=np.insert(price, a, np.float64('NaN'))


def cevir(a):
    for i in range(len(a)-1):
        b=(a[i].split('.'))
        start_time = datetime(int(b[2]),int(b[1]),int(b[0]))

        start_time=datetime.timestamp(start_time)

        b = a[i+1].split('.')
        end_time = datetime(int(b[2]), int(b[1]), int(b[0]))
        end_time=datetime.timestamp(end_time)
        c=start_time-end_time
        if c!=float(86400.0):
            s2=start_time-86400.0
            a.insert(i+1,datetime.fromtimestamp(s2).strftime('%d.%m.%Y'))
            ekle(i+1)


cevir(date)
date=np.asarray(date)
price=price.astype(dtype="float64")
df=pd.DataFrame()
df['Tarih']=date[::-1]
df['Fiyat']=price[::-1]

df['Fiyat'].interpolate(method='linear', inplace=True)

df['Date'] = pd.to_datetime(df.Tarih, format='%d.%m.%Y')
close_data = df['Fiyat'].values
close_data = close_data.reshape((-1,1))

split_percent = 0.6
split = int(split_percent*len(close_data))

close_train = close_data[:split]
close_test = close_data[split:]

date_train = df['Date'][:split]
date_test = df['Date'][split:]

print(len(close_train))
print(len(close_test))

look_back = 3

train_generator = TimeseriesGenerator(close_train, close_train, length=look_back, batch_size=20)
test_generator = TimeseriesGenerator(close_test, close_test, length=look_back, batch_size=1)


from keras.models import Sequential
from keras.layers import LSTM, Dense

model = Sequential()
model.add(
    LSTM(10,
        activation='relu',
        input_shape=(look_back,1))
)
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

num_epochs = 250
model.fit_generator(train_generator, epochs=num_epochs, verbose=1)
prediction = model.predict_generator(test_generator)

close_train = close_train.reshape((-1))
close_test = close_test.reshape((-1))
prediction = prediction.reshape((-1))

model.save("lstmf2.h5")
