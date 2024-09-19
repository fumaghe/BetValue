import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Fai una richiesta HTTP al sito
url = 'https://fbref.com/it/comp/Big5/misc/squadre/Statistiche-di-I-5-campionati-europei-piu-importanti'
response = requests.get(url)

# Step 2: Parsare l'HTML con BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Trova tutte le tabelle di interesse
tables = soup.find_all('table')

# Seleziona la prima tabella o quella con più colonne, o filtra per contenuto
table = None
for t in tables:
    if t.find('thead') and t.find('tbody'):
        table = t
        break

if table is None:
    print("Nessuna tabella trovata.")
    exit()

# Step 4: Estrai le intestazioni della tabella (saltando eventuali intestazioni multiple)
headers = []
for th in table.find('thead').find_all('tr')[-1].find_all('th'):
    headers.append(th.text.strip())

# Step 5: Estrai i dati delle righe della tabella
rows = []
for row in table.find('tbody').find_all('tr'):
    cells = row.find_all(['th', 'td'])
    # Controlla che il numero di celle corrisponda alle intestazioni
    if len(cells) == len(headers):
        row_data = [cell.text.strip() for cell in cells]
        rows.append(row_data)

# Step 6: Creare un DataFrame con Pandas
df = pd.DataFrame(rows, columns=headers)

# Step 7: Salva i dati in un file CSV
df.to_csv('statisticheVarie.csv', index=False)

print("CSV creato con successo!")
