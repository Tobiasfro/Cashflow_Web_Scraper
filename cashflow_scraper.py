"""cashflow.py: Goes through x number of pages in cashflow and finds all Studs22 receipts 
                that HAS been certified but NOT yet confirmed to be in the ledger.
                Prints the URL's to these receipts in a .txt file. Also prints (in the terminal)
                the number of found unconfirmed receipts and the total cost of them in SEK."""

__author__ = "Tobias Fröberg"

import requests
import time
from bs4 import BeautifulSoup

# Insert your cookies from your GET request.
cookies = {
}

def main():
    response = requests.get('https://cashflow.datasektionen.se/admin/expenses/?page=1&committee=STUDS%202022', cookies=cookies)
    soup = BeautifulSoup(response.content, 'html5lib')
    maxPageNum = max(1,len(soup.find('span', attrs = {'class':'step-links'}).find_all('a'))-1)

    try:
        # If for example 5 is given, page nr 1, 2, 3, 4 and 5 of the receipts will be scanned.
        pageNum = int(input("Insert the number of pages (1-" + str(maxPageNum) + ") to scan: "))
    except ValueError:
        print("Input has to be a number.")
        quit()

    if maxPageNum < pageNum or pageNum < 1:
        print("You submitted an invalid number, submit a number in the range of 1-" + str(maxPageNum) + ".")
        quit()

    totUnconfirmReceipts = 0
    totalReceiptCost = 0.0
    f = open("cashflow.txt", "w")
    while pageNum >= 1:
        response = requests.get('https://cashflow.datasektionen.se/admin/expenses/?page='+str(pageNum)+'&committee=STUDS%202022', cookies=cookies)
        soup = BeautifulSoup(response.content, 'html5lib')
        newUnconfirmReceipts = 0

        for tag in soup.find_all('tr'):
            for link in tag.find_all('a'):
                if link.has_attr('href') and link.text == "Attesterad men inte i pärmen":
                    f.write("https://cashflow.datasektionen.se" + link.attrs['href'] + "\n")
                    newUnconfirmReceipts += 1

                    # Add the cost of this receipt to the total cost of the previous found unconfirmed receipts.
                    costString = tag.find('td', attrs = {'class':'right'}).text.split(" ")[0]
                    costFloat = float(replacer(costString))
                    totalReceiptCost += costFloat
        
        time.sleep(1/4)
        totUnconfirmReceipts += newUnconfirmReceipts
        print("Done with page " + str(pageNum) + ". " + str(newUnconfirmReceipts) + " new unconfirmed receipts found.")
        print("The total is now " + str(totUnconfirmReceipts) + " receipts with the cost of "+ str(round(totalReceiptCost,2)) + " kr.\n")
        pageNum -= 1

    f.close()

def replacer(str):
    # Replaces the unwanted characters in the string so that the float function can convert the string to float.
    replacers = {',':'.', '\xa0':''}
    for ch in replacers:
        str = str.replace(ch, replacers[ch])
    return str

main()