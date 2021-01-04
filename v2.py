import requests
from bs4 import BeautifulSoup
import re
import time
from win10toast import ToastNotifier
from datetime import datetime


def olx_karta():
    url = 'https://www.olx.pl/oferty/q-rx-580/?search%5Bfilter_float_price%3Afrom%5D=400&search%5Bfilter_float_price%3Ato%5D=700'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    tmp = []
    for l in soup.find(id="offers_table").findAll('a', attrs={'href': re.compile("oferta")}):
        tmp.append(l.get('href'))
    return tmp


def allegro():
    url = 'https://allegro.pl/kategoria/podzespoly-komputerowe-karty-graficzne-260019?string=rx%20580%208gb&bmatch=cl-dict201214-ctx-fd-ele-1-5-1218&price_to=700&price_from=400'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    tmp = []
    for paragraph in soup.find_all("div", class_="opbox-listing"):
        for a in paragraph("a"):
            tmp.append(a.get('href'))
    return tmp


def main():
    links = []
    links += allegro()
    links += olx_karta()

    links = list(dict.fromkeys(links))

    f = open("C:/Users/ultor/PycharmProjects/Powiadomienia/links.txt", "r+")
    old_links = f.read().splitlines()

    fine_links = [x for x in links if x not in old_links]

    if len(fine_links) > 0:
        with open("C:/Users/ultor/Desktop/LINKI.TXT", "a") as myfile:
            myfile.write("\n")
            myfile.write(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
            myfile.write("\n")
            for a in fine_links:
                f.write(str(a))
                f.write("\n")
                myfile.write(a)
                myfile.write("\n")
        toaster.show_toast("Znaleziono nowe linki!", str(len(fine_links)) + " nowe linki.")
    f.close()

toaster = ToastNotifier()
toaster.show_toast("Program działa", ":)")
while 1:
    main()
    time.sleep(600)
