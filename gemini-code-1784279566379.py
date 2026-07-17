import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono il tuo Vinted Tracker. Usa /cerca [prodotto] per vedere gli ultimi annunci.")

async def cerca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Per favore, scrivi cosa cercare, es: /cerca Vans")
        return
    
    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Sto cercando '{query}' per te...")
    
    try:
        # Costruiamo l'URL dinamico
        url = f"https://www.vinted.it/catalog?search_text={query}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        risposta = requests.get(url, headers=headers)
        soup = BeautifulSoup(risposta.text, 'html.parser')
        prodotti = soup.find_all('div', class_='feed-item')
        
        if not prodotti:
            await update.message.reply_text("Nessun prodotto trovato.")
            return

        # Inviamo i primi 3 risultati trovati
        for prodotto in prodotti[:3]:
            prezzo = prodotto.find('h3', class_='c-box__title')
            link_tag = prodotto.find('a', class_='new-item-box__overlay')
            
            if prezzo and link_tag:
                link = "https://www.vinted.it" + link_tag.get('href')
                msg = f"✅ Trovato: {prezzo.text.strip()}\n🔗 {link}"
                await update.message.reply_text(msg)
                
    except Exception as e:
        await update.message.reply_text(f"Errore durante la ricerca: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('cerca', cerca))
    
    print("Bot in ascolto...")
    application.run_polling()
