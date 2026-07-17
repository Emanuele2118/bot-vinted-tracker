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
    # MODIFICA QUI IL PREZZO MASSIMO DESIDERATO
    PREZZO_MASSIMO = 50.0 
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        # URL della tua ricerca
        url = "https://www.vinted.it/catalog?search_text=Vans%20Sk8-Mid&search_id=1109702021&size_ids[]=784&page=1"
        risposta = requests.get(url, headers=headers)
        
        if risposta.status_code == 200:
            soup = BeautifulSoup(risposta.text, 'html.parser')
            prodotti = soup.find_all('div', class_='feed-item')
            
            for prodotto in prodotti:
                prezzo_tag = prodotto.find('h3', class_='c-box__title')
                link_tag = prodotto.find('a', class_='new-item-box__overlay')
                
                if prezzo_tag and link_tag:
                    # Pulizia stringa prezzo per confronto numerico
                    testo_prezzo = prezzo_tag.text.strip().replace('€', '').replace(',', '.').strip()
                    try:
                        prezzo_valore = float(testo_prezzo)
                    except:
                        continue
                    
                    # Filtro: invia solo se il prezzo è minore o uguale alla soglia
                    if prezzo_valore <= PREZZO_MASSIMO:
                        link_prodotto = "https://www.vinted.it" + link_tag.get('href')
                        messaggio = f"✅ Affare trovato!\n💰 Prezzo: {prezzo_tag.text.strip()}\n🔗 Link: {link_prodotto}"
                        
                        asyncio.run(invia_messaggio(messaggio))
                        time.sleep(2) # Anti-spam
                    
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    # Avvio bot
    asyncio.run(invia_messaggio("🤖 Bot monitoraggio Vinted attivato con filtro prezzo!"))
    while True:
        controlla_vinted()
        # Attesa di 1 ora prima del prossimo controllo
        time.sleep(3600)
