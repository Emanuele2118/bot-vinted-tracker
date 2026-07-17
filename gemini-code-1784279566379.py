import requests
from bs4 import BeautifulSoup
import time
import os
import asyncio
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = Bot(token=TOKEN)

async def invia_messaggio(testo):
    await bot.send_message(chat_id=CHAT_ID, text=testo)

def controlla_vinted():
    print("Sto interrogando Vinted...")
    try:
        risposta = requests.get("https://www.vinted.it/catalog?search_text=Vans%20Sk8-Mid&search_id=1109702021&size_ids[]=784&page=1", 
                                headers={'User-Agent': 'Mozilla/5.0...'})
        if risposta.status_code == 200:
            soup = BeautifulSoup(risposta.text, 'html.parser')
            prodotti = soup.find_all('div', class_='feed-item')
            for prodotto in prodotti:
                prezzo = prodotto.find('h3', class_='c-box__title')
                if prezzo:
                    # Usiamo asyncio.run per chiamare la funzione asincrona da una normale
                    asyncio.run(invia_messaggio(f"Nuovo prodotto: {prezzo.text.strip()}"))
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    # Messaggio di test iniziale
    asyncio.run(invia_messaggio("Bot avviato con successo!"))
    while True:
        controlla_vinted()
        time.sleep(3600)
