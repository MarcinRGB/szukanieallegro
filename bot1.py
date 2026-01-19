import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

MAX_CENA = 2500
SILNIK = "Diesel"
URL = "https://allegro.pl/kategoria/motoryzacja-samochody-osobowe-4?string=diesel&search[locations][0]=Kraków"

BOT = Bot(token=TOKEN)
znalezione = set()

def sprawdz_allegro():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    oferty = soup.find_all("div", {"data-role": "offer"})

    for oferta in oferty:
        link_tag = oferta.find("a", {"class": "link"})
        if not link_tag: continue
        link = link_tag['href']
        tytul = link_tag.text.strip()
        if link in znalezione: continue
        znalezione.add(link)

        cena_tag = oferta.find("span", {"class": "price"})
        if not cena_tag: continue
        cena_str = cena_tag.text.replace("zł","").replace(" ","").replace("\xa0","")
        try: cena = int(cena_str)
        except: continue

        if cena <= MAX_CENA and SILNIK.lower() in tytul.lower():
            msg = f"🔥 Znalezione! {tytul} - {cena} zł\n{link}"
            BOT.send_message(chat_id=CHAT_ID, text=msg)
            print(msg)

sprawdz_allegro()
