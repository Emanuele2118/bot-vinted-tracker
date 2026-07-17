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
        # Nota: ho completato l'User-Agent per renderlo più realistico
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        risposta = requests.get("https://www.vinted.it/catalog?search_text=Vans%20Sk8-Mid&search_id=1109702021&size_ids[]=784&page=1", 
                                headers=headers)
        
        if risposta.status_code == 200:
            soup = BeautifulSoup(risposta.text, 'html.parser')
            prodotti = soup.find_all('div', class_='feed-item')
            
            for prodotto in prodotti:
                prezzo = prodotto.find('h3', class_='c-box__title')
                # Cerchiamo il link dentro il tag 'a'
                link_tag = prodotto.find('a', class_='new-item-box__overlay')
                
                if prezzo and link_tag:
                    link_prodotto = "https://www.vinted.it" + link_tag.get('href')
                    messaggio = f"👟 Nuovo prodotto trovato!\n💰 Prezzo: {prezzo.text.strip()}\n🔗 Link: {link_prodotto}"
                    
                    asyncio.run(invia_messaggio(messaggio))
                    # Un piccolo sleep per evitare di inondare Telegram se trova troppi risultati
                    time.sleep(2)
                    
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    asyncio.run(invia_messaggio("Bot avviato con successo!"))
    while True:
        controlla_vinted()
        time.sleep(3600) # Aspetta 1 ora prima di ricontrollare
