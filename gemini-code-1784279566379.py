import requests
from bs4 import BeautifulSoup
import time
import os
from telegram import Bot

# Configurazione Telegram
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID") # Sostituisci con il tuo ID numerico
bot = Bot(token=TOKEN)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = "https://www.vinted.it/catalog?search_text=Vans%20Sk8-Mid&search_id=1109702021&size_ids[]=784&page=1"

def controlla_vinted():
    print("Sto interrogando Vinted...")
    try:
        risposta = requests.get(url, headers=headers)
        if risposta.status_code == 200:
            soup = BeautifulSoup(risposta.text, 'html.parser')
            prodotti = soup.find_all('div', class_='feed-item')
            
            for prodotto in prodotti:
                prezzo = prodotto.find('h3', class_='c-box__title')
                if prezzo:
                    messaggio = f"Nuovo prodotto trovato! Prezzo: {prezzo.text.strip()}"
                    print(messaggio)
                    bot.send_message(chat_id=CHAT_ID, text=messaggio)
        else:
            print(f"Errore: {risposta.status_code}")
    except Exception as e:
        print(f"Errore nel bot: {e}")

if __name__ == "__main__":
    while True:
        controlla_vinted()
        time.sleep(3600) # Aspetta 1 ora
