"""cashflow.py: Scannar igenom x antal sidor i cashflow och hittar alla STUDS22
                utlägg som HAR attesterats men som INTE bekräftats i pärmen."""

__author__ = "Tobias Fröberg"

import requests
import time
from bs4 import BeautifulSoup

# Kopiera in dina cookies från din GET request
cookies = {
}

response = requests.get('https://cashflow.datasektionen.se/admin/expenses/?page=1&committee=STUDS%202022', cookies=cookies)
soup = BeautifulSoup(response.content, 'html5lib')
maxNum = len(soup.find('span', attrs = {'class':'step-links'}).find_all('a'))-1

try:
    # Om exempelvis siffran 5 anges kommer de sida 1, 2, 3, 4 och 5 av utläggen att skannas
    pageNr = int(input("Skriv in hur många sidor (1-" + str(maxNum) + ") med utlägg som ska kontrolleras: "))
except ValueError:
    print("Input måste vara en siffra")
    quit()

if maxNum < pageNr or pageNr < 1:
    print("Du angav ej giltlig siffra (1-" + str(maxNum) + ")")
    quit()

f = open("cashflow.txt", "w")
totalNonConfirmedReceipts = 0
while pageNr >= 1:
    response = requests.get('https://cashflow.datasektionen.se/admin/expenses/?page='+str(pageNr)+'&committee=STUDS%202022', cookies=cookies)
    soup = BeautifulSoup(response.content, 'html5lib')
    newNonConfirmedReceipts = 0
    for link in soup.find_all('a'):
        if link.has_attr('href') and link.text == "Attesterad men inte i pärmen":
            #print(link.text)
            print("https://cashflow.datasektionen.se" + link.attrs['href'], file=f)
            newNonConfirmedReceipts += 1
    totalNonConfirmedReceipts += newNonConfirmedReceipts
    time.sleep(1/4)
    print("Klar med sida " + str(pageNr) + ". " + str(newNonConfirmedReceipts) + " nya obekräftade kvitton hittade. Totalt " + str(totalNonConfirmedReceipts) + ".")
    pageNr -= 1
f.close()
