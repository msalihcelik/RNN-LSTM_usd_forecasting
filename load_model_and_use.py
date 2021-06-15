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
import tkinter
from keras.models import Sequential
from keras.layers import LSTM, Dense
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from PIL import ImageTk,Image

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
            cevir(a)

cevir(date)
date=np.asarray(date)
price=price.astype(dtype="float64")

def yazdir():
    deger=kutu.get()
    print(forecast_dates[1],forecast[1])

pencere=Tk()
pencere.title("DOVIZ TAHMINI")
pencere.geometry("600x600")
pencere.resizable(FALSE,FALSE)

C = Canvas(pencere, bg="blue", height=250, width=300)
filename = PhotoImage(file = "C:/Users/FI/PycharmProjects/staj/d1.png")
background_label = Label(pencere, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()


yazi=Label(pencere,text="Elimizdeki Veriler",font=('Arial bold', 14),relief='raised')
yazi.place(x=230,y=120)

# yazi.pack()


listekutusu=Listbox(borderwidth=4, relief="solid")
listekutusu.place(x=240,y=160)

for i in range(len(date)):
    listekutusu.insert(END,str(date[i])+"          "+str(price[i]))



def yeni():
    global pencere
    global window

    pencere.withdraw()
    window=Tk()
    window.title("DOVIZ TAHMINI")
    window.geometry("600x600")
    window.resizable(FALSE,FALSE)
    C = Canvas(window, bg='blue', height=600, width=600)
    C.pack()
    label1=Label(window,text="Kaç gün sonrası için tahmin yapmak istiyorsunuz?")
    label1.place(x=165,y=131)
    lis=[i for i in range(1,10)]
    global kutu
    kutu=Combobox(window,values=lis,height=5)
    kutu.set(1)
    kutu.place(x=235,y=180)
    but1=Button(window,text="Görselleştir",command=aha2,bg='brown',fg='white',borderwidth=1, relief="solid")
    but1.place(x=270,y=220)
    but2=Button(window,text="Geri Dön",command=degis,bg='brown',fg='white',borderwidth=1, relief="solid")
    but2.place(x=277,y=260)

def degis():
    global pencere
    global window
    pencere.deiconify()
    window.withdraw()


buton=Button(pencere,text="Tahmin Oluştur",command=yeni,bg='brown',fg='white',borderwidth=3, relief="solid",height=4, width=11)
buton.place(x=310,y=350)


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

look_back = 3

train_generator = TimeseriesGenerator(close_train, close_train, length=look_back, batch_size=20)
test_generator = TimeseriesGenerator(close_test, close_test, length=look_back, batch_size=1)

model = load_model('lstmf.h5')

prediction = model.predict_generator(test_generator)

close_train = close_train.reshape((-1))
close_test = close_test.reshape((-1))
prediction = prediction.reshape((-1))

def aha():
    trace1 = go.Scatter(
        x = date_train,
        y = close_train,
        mode = 'lines',
        name = 'Data'
    )
    trace2 = go.Scatter(
        x = date_test,
        y = prediction,
        mode = 'lines',
        name = 'Prediction'
    )
    trace3 = go.Scatter(
        x = date_test,
        y = close_test,
        mode='lines',
        name = 'Ground Truth'
    )
    layout = go.Layout(
        title = "Google Stock",
        xaxis = {'title' : "Date"},
        yaxis = {'title' : "Close"}
    )

    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
    fig.show()


def aha2():
    global close_data
    close_data = close_data.reshape((-1))

    def predict(num_prediction, model):
        prediction_list = close_data[-look_back:]

        for _ in range(num_prediction):
            x = prediction_list[-look_back:]
            x = x.reshape((1, look_back, 1))
            out = model.predict(x)[0][0]
            prediction_list = np.append(prediction_list, out)
        prediction_list = prediction_list[look_back - 1:]

        return prediction_list

    def predict_dates(num_prediction):
        last_date = df['Date'].values[-1]
        prediction_dates = pd.date_range(last_date, periods=num_prediction + 1).tolist()
        return prediction_dates

    global kutu
    num_prediction = int(kutu.get())
    forecast = predict(num_prediction, model)
    forecast_dates = predict_dates(num_prediction)

    trace1 = go.Scatter(
        x = date_train,
        y = close_train,
        mode = 'lines',
        name = 'Data'
    )
    trace2 = go.Scatter(
        x = date_test,
        y = prediction,
        mode = 'lines',
        name = 'Prediction'
    )
    trace3 = go.Scatter(
        x = date_test,
        y = close_test,
        mode='lines',
        name = 'Ground Truth'
    )
    layout = go.Layout(
        title = "Google Stock",
        xaxis = {'title' : "Date"},
        yaxis = {'title' : "Close"}
    )
    trace11 = go.Scatter(
        x=forecast_dates,
        y=forecast,
        mode='lines',
        name='Guess'
    )

    fig = go.Figure(data=[trace1, trace2, trace3,trace11], layout=layout)
    fig.show()



buton2=Button(pencere,text="Görselleştir",command=aha,bg='brown',fg='white',borderwidth=3, relief="solid",height=4, width=11)
buton2.place(x=220,y=350)

mainloop()
