import os
import cloudscraper
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Il Token viene letto dalle variabili d'ambiente di Railway
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
        scraper = cloudscraper.create_scraper()
        url = f"https://www.vinted.it/catalog?search_text={query}&order=newest_first"
        
        # Header ottimizzati per simulare un browser e superare il blocco 406
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.vinted.it/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1'
        }
        
        risposta = scraper.get(url, headers=headers)
        
        if risposta.status_code != 200:
            await update.message.reply_text(f"Errore: Vinted ha risposto con codice {risposta.status_code}.")
            return

        soup = BeautifulSoup(risposta.text, 'html.parser')
        prodotti = soup.select('div[data-testid="item-box"]')
        
        if not prodotti:
            await update.message.reply_text("Nessun prodotto trovato. Vinted ha bloccato il contenuto.")
            return

        # Invio dei primi 3 risultati
        for prodotto in prodotti[:3]:
            titolo = prodotto.select_one('h3')
            link_tag = prodotto.select_one('a')
            if titolo and link_tag:
                link = "https://www.vinted.it" + link_tag.get('href')
                await update.message.reply_text(f"✅ Trovato: {titolo.text.strip()}\n🔗 {link}")
                
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
        
