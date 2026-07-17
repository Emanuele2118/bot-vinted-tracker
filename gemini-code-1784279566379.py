import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Prendi il token da Railway
TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono il tuo Vinted Tracker. Usa /cerca [prodotto] per iniziare.")

async def cerca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Esempio: /cerca Vans -> context.args contiene ['Vans']
    if not context.args:
        await update.message.reply_text("Per favore, scrivi cosa cercare, es: /cerca Vans")
        return
    
    prodotto = " ".join(context.args)
    await update.message.reply_text(f"Perfetto! Sto cercando '{prodotto}' su Vinted per te...")
    # Qui in futuro chiameremo la funzione di ricerca

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Registrazione dei comandi
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('cerca', cerca))
    
    print("Bot in ascolto...")
    application.run_polling()
