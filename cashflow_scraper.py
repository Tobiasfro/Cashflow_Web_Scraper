"""cashflow.py: Goes through x number of pages in cashflow and finds all Studs22 receipts 
                that HAS been certified but NOT yet confirmed to be in the ledger.
                Prints the URL's to these receipts in a .txt file. Also prints (in the terminal)
                the number of found unconfirmed receipts and the total cost of them in SEK."""

__author__ = "Tobias Fröberg"

import requests
import time
from bs4 import BeautifulSoup

# Insert your cookies from your GET request
cookies = {
}

def main():
    response = requests.get('https://cashflow.datasektionen.se/admin/expenses/?page=1&committee=STUDS%202022', cookies=cookies)
    soup = BeautifulSoup(response.content, 'html5lib')
    maxPageNum = max(1,len(soup.find('span', attrs = {'class':'step-links'}).find_all('a'))-1)

    try:
        # If for example 5 is given, page nr 1, 2, 3, 4 and 5 of the receipts will be scanned
        pageNum = int(input("Insert the number of pages (1-" + str(maxPageNum) + ") to scan: "))
    except ValueError:
        print("Input has to be a number.")
        quit()

    if maxPageNum < pageNum or pageNum < 1:
        print("You submitted an invalid number, submit a number in the range of 1-" + str(maxPageNum) + ".")
        quit()

    f = open("cashflow.txt", "w")
    totUnconfirmReceipts = 0
    while pageNum >= 1:
        response = requests.get('https://cashflow.datasektionen.se/admin/expenses/?page='+str(pageNum)+'&committee=STUDS%202022', cookies=cookies)
        soup = BeautifulSoup(response.content, 'html5lib')
        newUnconfirmReceipts = 0
        for link in soup.find_all('a'):
            if link.has_attr('href') and link.text == "Attesterad men inte i pärmen":
                f.write("https://cashflow.datasektionen.se" + link.attrs['href'] + "\n")
                newUnconfirmReceipts += 1
        totUnconfirmReceipts += newUnconfirmReceipts
        time.sleep(1/4)
        print("Done with page " + str(pageNum) + ". " + str(newUnconfirmReceipts) + " new unconfirmed receipts found.")
        print("The total is now " + str(totUnconfirmReceipts) + " receipts.")
        pageNum -= 1
    f.close()

main()