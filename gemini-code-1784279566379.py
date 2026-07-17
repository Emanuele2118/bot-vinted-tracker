import os
import cloudscraper
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
    await update.message.reply_text(f"🔍 Sto cercando '{query}' tramite API...")
    
    try:
        scraper = cloudscraper.create_scraper()
        # Utilizziamo l'endpoint dell'API v2
        url = f"https://www.vinted.it/api/v2/catalog/items?search_text={query}&order=newest_first"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.vinted.it/'
        }
        
        risposta = scraper.get(url, headers=headers)
        
        if risposta.status_code != 200:
            await update.message.reply_text(f"Errore API: Vinted ha risposto con codice {risposta.status_code}.")
            return

        data = risposta.json()
        prodotti = data.get('items', [])
        
        if not prodotti:
            await update.message.reply_text("Nessun prodotto trovato tramite API.")
            return

        for item in prodotti[:3]:
            titolo = item.get('title', 'Nessun titolo')
            id_prodotto = item.get('id')
            link = f"https://www.vinted.it/items/{id_prodotto}"
            
            await update.message.reply_text(f"✅ Trovato: {titolo}\n🔗 {link}")
                
    except Exception as e:
        await update.message.reply_text(f"Errore tecnico: {str(e)}")

if __name__ == '__main__':
    if not TOKEN:
        print("ERRORE: TELEGRAM_TOKEN non trovato!")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('cerca', cerca))
        print("Bot in ascolto tramite API...")
        application.run_polling()
        
