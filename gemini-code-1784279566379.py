import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Il Token viene letto automaticamente dalle variabili d'ambiente di Railway
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
        # URL di ricerca standard
        url = f"https://www.vinted.it/catalog?search_text={query}"
        
        # Headers simulano un browser reale
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'it-IT,it;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        risposta = requests.get(url, headers=headers)
        
        if risposta.status_code != 200:
            await update.message.reply_text(f"Errore: Vinted ha risposto con codice {risposta.status_code}.")
            return

        soup = BeautifulSoup(risposta.text, 'html.parser')
        
        # Selezione dei contenitori prodotto usando data-testid
        prodotti = soup.select('div[data-testid="item-box"]')
        
        if not prodotti:
            await update.message.reply_text("Nessun prodotto trovato. Vinted potrebbe aver bloccato temporaneamente la richiesta.")
            return

        # Invio dei primi 3 risultati trovati
        for prodotto in prodotti[:3]:
            # Estrazione titolo dal tag h3 all'interno del box
            titolo = prodotto.select_one('h3')
            # Estrazione link dal tag a
            link_tag = prodotto.select_one('a')
            
            if titolo and link_tag:
                link = "https://www.vinted.it" + link_tag.get('href')
                msg = f"✅ Trovato: {titolo.text.strip()}\n🔗 {link}"
                await update.message.reply_text(msg)
                
    except Exception as e:
        await update.message.reply_text(f"Errore tecnico: {str(e)}")

if __name__ == '__main__':
    if not TOKEN:
        print("ERRORE: TELEGRAM_TOKEN non trovato nelle variabili d'ambiente!")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('cerca', cerca))
        
        print("Bot in ascolto...")
        application.run_polling()
