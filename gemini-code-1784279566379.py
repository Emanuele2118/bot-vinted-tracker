import os
import cloudscraper
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
        # Creiamo lo scraper che simula un browser reale
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
        url = f"https://www.vinted.it/catalog?search_text={query}&order=newest_first"
        
        # Effettuiamo la richiesta
        risposta = scraper.get(url)
        
        if risposta.status_code != 200:
            await update.message.reply_text(f"Errore: Vinted ha risposto con codice {risposta.status_code}.")
            return

        soup = BeautifulSoup(risposta.text, 'html.parser')
        prodotti = soup.select('div[data-testid="item-box"]')
        
        if not prodotti:
            await update.message.reply_text("Nessun prodotto trovato. Vinted potrebbe aver cambiato la struttura della pagina.")
            return

        # Inviamo i risultati
        for prodotto in prodotti[:3]:
            titolo = prodotto.select_one('h3')
            link_tag = prodotto.select_one('a')
            
            if titolo and link_tag:
                link = "https://www.vinted.it" + link_tag.get('href')
                msg = f"✅ Trovato: {titolo.text.strip()}\n🔗 {link}"
                await update.message.reply_text(msg)
                
    except Exception as e:
        await update.message.reply_text(f"Errore tecnico: {str(e)}")

if __name__ == '__main__':
    if not TOKEN:
        print("ERRORE: TELEGRAM_TOKEN non trovato!")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('cerca', cerca))
        print("Bot in ascolto con CloudScraper...")
        application.run_polling()
