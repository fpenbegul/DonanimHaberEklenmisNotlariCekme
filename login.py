import requests
from lxml import html
from html.parser import HTMLParser
from lxml import etree
import timeit
import pymongo
import time
import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db=client.DonanimHaber_Kisisel_Mesajlar
collection = db.veri
collection_dakika=db.dakika

mesaji_yok="Bu kullanıcıya hiç not girmemişsiniz. Girdiğiniz notları sadece siz görebilirsiniz."
mesaji_yok2="personal_notes_delete.asp?recID"

LOGIN_URL = "https://forum.donanimhaber.com/login"
headers = {'Content-Type': 'text/html; charset=utf-8',"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)" }
payload={'LoginName':'','Password':''}

    #defined request goes here
eski_y=0
start = timeit.default_timer()

with requests.Session() as session:
    post = session.post(LOGIN_URL, data=payload)
    #2680668
sayac=0
def basasar(y):
    try:
        dakika = datetime.datetime.now()
        dakika = dakika.minute
        sayac2=0
        for i in range(y, 2680668, 1):
            #if i % 1111500 == 0:
                # print("500 sayfa check edildi. Bekleniyor 99 sn")
                #time.sleep(99)



            start = timeit.default_timer()
            dakika_guncel = datetime.datetime.now()
            dakika_guncel = dakika_guncel.minute

            if sayac2==0:
                eski_y=i
                sayac2=sayac2+1

            if dakika_guncel>dakika and dakika_guncel!=0:
                kac_kullanici=i-eski_y
                zaman = datetime.datetime.now()
                dakika = zaman.minute
                saat=zaman.hour
                print(str(dakika)+" 1 dakikada kontrol edilen kullanıcı sayısı "+str(kac_kullanici))
                cpm = {"eski":str(eski_y),"yeni":str(i),"Zaman":str(saat)+":"+str(dakika),'Check per minutes': str(kac_kullanici)}
                collection_dakika.insert(cpm)
                print(eski_y)
                print(i)
                eski_y = i

            if dakika_guncel<1:
                zaman = datetime.datetime.now()
                dakika = zaman.minute

            URL = "https://forum.donanimhaber.com/personal_notes.asp?mem=" + str(i)
            r = session.get(URL, headers=headers, timeout=500)
            if r.status_code!=200:
                print("status:"+str(r.status_code)+" HATASI ALINDI TEKRAR KONTROL EDİLECEK...")
                print("Kullanıcı id= "+str(i))
                time.sleep(5)
                print("tekrar kontrole gönderiliyor Kullanıcı "+str(i))
                basasar(i)
                print(datetime.datetime.now())

            #  time.sleep(.5)

            r.encoding = 'iso-8859-9'
            source = BeautifulSoup(r.text, "lxml")
            icerik = source.find_all("div", class_="fislemeprofil")
            if mesaji_yok in str(icerik) and mesaji_yok2 not in str(icerik):
                print("status:"+str(r.status_code)+" "+str(i) + ". Kullanıcı için daha önce hiç mesaj girmediğim tespit edildi atlanıyor...")
                #time.sleep(.7)
                stop = timeit.default_timer()
                print('Time: ', stop - start)
                print(datetime.datetime.now())
                #time.sleep(1.7)

            else:
                stop = timeit.default_timer()
                document = {'uid': str(i), 'nick': '', 'tarih': str(datetime.datetime.now()), 'icerik': str(icerik),
                            'kayıt süre': stop - start}
                collection.insert(document)

                print("status:"+str(r.status_code)+" " + str(i) + ". Kullanıcı Eklendi ")
                stop = timeit.default_timer()
                print('Time: ', stop - start,'  ')
                print(datetime.datetime.now())
                time.sleep(25)

    except  Exception as e:
        print(e)
        for x in range(1, 101, 1):
            print("status:"+str(r.status_code)+" " + str(x) + ". saniye bekleniyor bağlantı timeout'a düştü " +str(i-1))
            #time.sleep(.6)
            if x==50:
                basasar(i);
                print(str(i)+". sıradan tekrar dönderilecek ")
                #time.sleep(.2)
                print(datetime.datetime.now())
    return


if sayac==0:
    basasar(2600000);
    #2002250 *
    #2621652
    #1839221
    #1837570
    #737597

    #971895
    sayac=sayac+1




stop = timeit.default_timer()
print('Time: ', stop - start)


print('Bitti.')