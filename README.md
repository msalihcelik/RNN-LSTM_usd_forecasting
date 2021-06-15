# UYGULAMA AMACI VE TANIMI
* Yapay zekanın zaman serileri üzerinde uygulanabilirliği göz önüne alınarak, çalışmada temel olarak yapay sinir ağları LSTM modeli kullanılmıştır.
* Python programlama dili ve PyCharm geliştirme ortamı kullanılarak geliştirilmiştir.
* Uygulama test amaçlı geliştirilmiş olduğundan küçük bir veri seti oluşturulmuş-kullanılmıştır. Testin amacı ileriye yönelik tahminler yapabilmektir.

# KULLANILAN TEKNOLOJİLER
* Requests: Bu modül ile web üzerindeki isteklerimizi yönetebiliriz. Mesela bu modül ile API’lere PUT, DELETE, POST gibi istekler atabiliriz.
* Matplotlib: Veri görselleştirme kütüphanesidir.
* Sci-kit learn: Ücretsiz bir makinesi öğrenmesi kütüphanesidir.
* Keras: Keras, Python'da yazılmış açık kaynaklı bir sinir ağı kütüphanesidir. Derin sinir ağları ile hızlı deney yapabilmek için tasarlanmıştır.
* Tkinter: Tkinter, Python programlama dili ile birlikte gelen grafiksel kullanıcı arayüzü aracıdır.
* LSTM: Uzun Kısa Vadeli Hafıza Ağları genellikle “LSTM” olarak adlandırılır. Uzun vadeli bağımlılıkları öğrenebilen özel bir RNN türüdür. LSTM’ler, uzun vadeli bağımlılık sorununun önüne geçmek için açıkça tasarlanmıştır.

# GEREKSİNİMLER VE İSTENEN İŞLEVLER
* https://tr.investing.com/currencies/usd-try-historical-data adresinden 30 günlük dolar verisi elde edilir. Hafta sonları için fiyat bilgisi boş tanımlanır. Bunun için Requests kütüphanesini kullanarak ilgili adresten verileri aldık. Pandas kütüphanesini kullanarak veri seti üzerinde düzenlemeler yaptık ve Keras kütüphanesini kullanarak LSTM sinir ağı modelini oluşturduk. Bu model sayesinde istenen günlerdeki dolar durumlarının tespitini gerçekleştirdik.

# SONUÇ VE KULLANIM
* Çalıştırılması durumunda son 30 günün dolar verileri ekranda gösterilir.
* Görselleştir butonu ile veriler grafik olarak görüntülenir.
* Tahmin oluştur butonu önceki günlerin verilerinden faydalanarak ileriye yönelik tahminler oluşturmamızı sağlar.

https://user-images.githubusercontent.com/48419933/122105780-d7851d80-ce21-11eb-8713-4a9c2dcb1adb.mp4

# KAYNAKLAR
* https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/
* https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/
* https://towardsdatascience.com/time-series-forecasting-with-recurrent-neural-networks-74674e289816
* https://www.youtube.com/c/Makine%C3%96%C4%9Frenmesi
