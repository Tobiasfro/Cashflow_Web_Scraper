'''cashflow.py: Goes through x number of pages in cashflow and finds all Studs22 receipts
                that HAS been certified but NOT yet confirmed to be in the ledger.
                Prints the URL's to these receipts in a .txt file. Also prints (in the terminal)
                the number of found unconfirmed receipts and the total cost of them in SEK.'''

__author__ = 'Tobias Fröberg'

import sys
import time
import requests
from bs4 import BeautifulSoup

# Insert your cookies from your GET request.
cookies = {
}

def main():
    '''Asks the user how many pages to scan and finds all the receipts that HAS been certified
    but NOT yet confirmed to be in the ledger. Prints the URL's to these receipts cashflow.txt.
    Also prints (in the terminal) the number of found unconfirmed receipts and the total cost
    of them in SEK.'''

    response = requests.get('https://cashflow.datasektionen.se/admin/expenses/?page=1&'
        'committee=STUDS%202022', cookies=cookies)
    soup = BeautifulSoup(response.content, 'html5lib')
    max_page_num = max(1,len(soup.find('span', attrs = {'class':'step-links'}).find_all('a'))-1)

    try:
        # If for example 5 is given, page nr 1, 2, 3, 4 and 5 of the receipts will be scanned.
        page_num = int(input('Insert the number of pages (1-' + str(max_page_num) + ') to scan: '))
    except ValueError:
        sys.exit('Input has to be a number.')

    if max_page_num < page_num or page_num < 1:
        sys.exit('You submitted an invalid number, submit a number in the range of 1-'
            + str(max_page_num) + '.')

    tot_unconfirm_receipts = 0
    total_receipt_cost = 0.0
    file = open('cashflow.txt', 'wt', encoding='utf8')
    while page_num >= 1:
        response = requests.get('https://cashflow.datasektionen.se/admin/expenses/?page='
            +str(page_num)+'&committee=STUDS%202022', cookies=cookies)
        soup = BeautifulSoup(response.content, 'html5lib')
        new_unconfirm_receipts = 0

        for tag in soup.find_all('tr'):
            for link in tag.find_all('a'):
                # Only interested in the receipts that HAS been certified but NOT yet 
                # confirmed to be in the ledger.
                if link.has_attr('href') and link.text == 'Attesterad men inte i pärmen':
                    file.write('https://cashflow.datasektionen.se' + link.attrs['href'] + '\n')
                    new_unconfirm_receipts += 1

                    # Add the cost of this receipt to the total cost of the previous 
                    # found unconfirmed receipts.
                    total_receipt_cost += receipt_cost_to_float(tag)

        time.sleep(1/4)
        tot_unconfirm_receipts += new_unconfirm_receipts
        print('\nDone with page ' + str(page_num) + '. ' + str(new_unconfirm_receipts)
            + ' new unconfirmed receipts found.')
        print('The total is now ' + str(tot_unconfirm_receipts) + ' receipts with the cost of '
            + str(round(total_receipt_cost,2)) + ' kr.')
        page_num -= 1

    file.close()

def receipt_cost_to_float(tag):
    '''Finds and converts the cost of the receipt (string) to float.'''

    cost_string = tag.find('td', attrs = {'class':'right'}).text.split(' ')[0]
    return float(replacer(cost_string))

def replacer(cost_string):
    '''Replaces the unwanted characters in the string so that the float
    function can convert the string to float.'''

    replacers = {',':'.', '\xa0':''}
    for key, value in replacers.items():
        cost_string = cost_string.replace(key, value)
    return cost_string

main()
