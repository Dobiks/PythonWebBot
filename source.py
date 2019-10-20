import requests
from bs4 import BeautifulSoup
import re
import smtplib
import time
import json

def gratka():
    url = 'https://gratka.pl/nieruchomosci/mieszkania/poznan/sprzedaz?data-dodania-search=ostatnich-24h&rynek=wtorny'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    tmp = []
    for l in soup.find(id='leftColumn').findAll('a', attrs={
        'href': re.compile("https://gratka.pl/nieruchomosci/mieszkanie")}):
        tmp.append(l.get('href'))
    return tmp


def otodom():
    url = 'https://www.otodom.pl/sprzedaz/mieszkanie/poznan/?search%5Bfilter_enum_market%5D%5B0%5D=secondary&search%5Bdescription%5D=1&search%5Bprivate_business%5D=private&search%5Bcreated_since%5D=1&search%5Bregion_id%5D=15&search%5Bsubregion_id%5D=462&search%5Bcity_id%5D=1'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    tmp = []
    for l in soup.find("div", {"class": "col-md-content section-listing__row-content"}).findAll('a', attrs={
        'href': re.compile("https://www.otodom.pl/oferta")}):
        tmp.append(l.get('href'))
    return tmp


def olx():
    url = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/poznan/?search%5Bfilter_enum_market%5D%5B0%5D=secondary&search%5Bprivate_business%5D=private'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    tmp = []
    for l in soup.find(id="offers_table").findAll('a', attrs={'href': re.compile("oferta")}):
        tmp.append(l.get('href'))
    return tmp


def gumtree():
    url = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/poznan/mieszkanie/v1c9073l3200366a1dwp1?df=ownr'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    tmp = []
    for l in soup.find("div", {"class": "view"}).findAll('a', attrs={
        'href': re.compile("a-mieszkania-i-domy")}):
        str = "https://www.gumtree.pl" + l.get('href')
        tmp.append(str)
    return tmp


def send_mail(detected):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    with open('login.json') as json_file:
        data = json.load(json_file)

    server.login(data['login'], data['password'])
    subject = 'Nowe ogloszenia!'
    body = "Nowe ogloszenia: "
    for a in detected:
        body += "\n"
        body += a

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(data['login'], data['email'], msg)
    print("Wyslano.")
    # print(msg)
    server.quit()


def main():
    links = []
    links += gratka()
    links += otodom()
    links += olx()
    links += gumtree()

    links = list(dict.fromkeys(links))

    f = open("links.txt", "r+")
    old_links = f.read().splitlines()

    fine_links = [x for x in links if x not in old_links]

    if len(fine_links) > 0:
        send_mail(fine_links)
    else:
        print("Brak nowych ogloszen")

    for a in fine_links:
        f.write(a)
        f.write("\n")


while 1:
    main()
    time.sleep(1800)
