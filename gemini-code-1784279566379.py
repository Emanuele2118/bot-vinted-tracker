import requests
from bs4 import BeautifulSoup
import time

# I "vestiti" da browser per non farti bloccare subito
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Il tuo link di Vinted
url = "https://www.vinted.it/catalog?search_text=Vans%20Sk8-Mid&search_id=1109702021&size_ids[]=784&page=1"

def controlla_vinted():
    print("Sto interrogando Vinted...")
    try:
        risposta = requests.get(url, headers=headers)
        
        if risposta.status_code == 200:
            soup = BeautifulSoup(risposta.text, 'html.parser')
            # Cerchiamo i contenitori degli articoli
            prodotti = soup.find_all('div', class_='feed-item')
            
            print(f"Trovati {len(prodotti)} prodotti nella pagina.")
            
            for prodotto in prodotti:
                # Nota: le classi di Vinted cambiano spesso, se non stampa nulla
                # dovremo aggiornare il nome della classe qui sotto
                prezzo = prodotto.find('h3', class_='c-box__title') 
                if prezzo:
                    print(f"Prezzo trovato: {prezzo.text.strip()}")
                else:
                    print("Prezzo non leggibile in questo annuncio.")
        else:
            print(f"Errore nella connessione: {risposta.status_code}")
            
    except Exception as e:
        print(f"Si è verificato un errore: {e}")

# Eseguiamo il controllo
if __name__ == "__main__":
    controlla_vinted()