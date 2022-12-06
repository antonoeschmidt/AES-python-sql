""" 
Rows in the database:
Prøvetagning, Prøvesvar, Prøvenummer, CPRnummer, Fornavn, Efternavn, Telefon, Samtykke, SORnummer, Teststed, PAX, Off_finans, Testtype, Materiale, Lokalisation, Resultat, Kommentar, Udlandsrejser, Rejsemål, Smittekontakt, Screening, DIN
"""
import os
import sqlite3
import csv
from dotenv import load_dotenv
from aes import AESCipher

load_dotenv()

ROOT_DIR = os.getenv("ROOT_DIR")
PASSWORD = os.getenv("PASSWORD")
TABLE_NAME = "testResults"
DATABASE_FILE = "database.db"
SALT="salt2162"

aes_cipher = AESCipher(PASSWORD, SALT)

def encrypt(data):
    """ Encrypts data using AES"""
    return aes_cipher.encrypt(data)

connection = sqlite3.connect(DATABASE_FILE)
print("Cleaning up and creating table")
with open("schema.sql") as f:
    connection.executescript(f.read())

files_list = []
print("Reading files...")
for root, dirs, files in os.walk(ROOT_DIR):
    for fi in files:
        if fi.split(".")[-1] == 'csv':
            files_list.append(f"{root}/{fi}")
print(f"Found {len(files_list)} files")

cur = connection.cursor()
# utf-8-sig to remove BOM (\ufeff) from the first line
with open(files_list[0], 'r', encoding='utf-8-sig') as f: 
    # Adds the header to the database
    headers = f.readlines()
    cur.execute(f"INSERT INTO headers (Headers) VALUES (?)", (headers[0],))

for index, file in enumerate(files_list):
    print(f'Processing file {index + 1} of {len(files_list)}')

    # Open the file to read the raw lines.
    with open(file,"r") as textlines:
        next(textlines) # skip header line

        # Open the file a second time to parse CSV records.
        with open(file,"r") as csvlines:
            csvrows = csv.DictReader(csvlines, delimiter=";")

            # While reading the two file iterators in parallel,
            # encrypt the raw lines and insert database records.
            cur.executemany(f"INSERT INTO {TABLE_NAME} VALUES (?, ?, ?, ?, ?)", 
                [ ( None, row["CPRnummer"], row["Fornavn"], row["Efternavn"], encrypt(line) ) for line,row in zip(textlines,csvrows) ]
            )

print("Finished processing files")

# Adding index to CPRnummer for optimization
print("Creating index...")
cur.execute(f"CREATE INDEX Idx1 ON {TABLE_NAME}(CPRnummer)")

connection.commit()
connection.close()

print("Finished")