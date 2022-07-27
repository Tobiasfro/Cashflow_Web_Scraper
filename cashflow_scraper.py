'''cashflow.py: Goes through x number of pages from the selected committee in cashflow and finds
                all receipts that HAS been certified but NOT yet confirmed to be in the ledger.
                Prints the URL's to these receipts in a .txt file. Also prints (in the terminal)
                the number of found unconfirmed receipts and the total cost of them in SEK.'''

__author__ = 'Tobias Fröberg'

import sys
import time
from ast import literal_eval
import requests
from bs4 import BeautifulSoup

# Insert your cookies from your GET request.
cookies = {
}

def main():
    '''Asks the user what comittee and how many pages to scan and finds all the receipts that
    HAS been certified but NOT yet confirmed to be in the ledger. Prints the URL's to these
    receipts cashflow.txt. Also prints (in the terminal) the number of found unconfirmed
    receipts and the total cost of them in SEK.'''

    # Select the committee of your choice.
    committee = committee_selector()

    # Select the number of pages of your choice.
    page_num = page_num_selector(committee)

    tot_unconfirm_receipts = 0
    tot_receipt_cost = 0.0
    file = open('cashflow.txt', 'wt', encoding='utf8')
    while page_num >= 1:
        response = requests.get('https://cashflow.datasektionen.se/admin/expenses/?page='
            +str(page_num)+'&committee=' + committee, cookies=cookies)
        soup = BeautifulSoup(response.content, 'html.parser')
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
                    tot_receipt_cost += receipt_cost_to_float(tag)

        time.sleep(1/4)
        tot_unconfirm_receipts += new_unconfirm_receipts
        print('\nDone with page ' + str(page_num) + '. ' + str(new_unconfirm_receipts)
            + ' new unconfirmed receipts found.')
        print('The total is now ' + str(tot_unconfirm_receipts) + ' receipts with the cost of '
            + str(round(tot_receipt_cost,2)) + ' kr.')
        page_num -= 1

    file.close()

def committee_selector():
    '''Prints all the availabale committees and returns the committee
    that matches to the user's entered committee id if it's valid.'''

    response = requests.get('https://cashflow.datasektionen.se/admin/expenses', cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')

    # All committees are stored in a javascript array.
    # Select correct script, filter out everything in the script except the array
    # and convert the string representation of the array to an array.
    committees = literal_eval(soup.find_all('script')[6].text.
        split('committees: ')[1].split(',\n                committee: ')[0])

    committee_dict = {}
    committee_id = 0
    for committee in committees:
        committee_id += 1
        committee_dict[committee_id] = committee
        print(committee_id, committee)

    try:
        committee_num = int(input('\nEnter the number (1-'
            + str(committee_id) + ') corresponding to the committee you want to scan: '))
    except ValueError:
        sys.exit('Input has to be a number.')

    if committee_id < committee_num or committee_num < 1:
        sys.exit('You submitted an invalid number, submit a number in the range of 1-'
            + str(committee_id) + '.')

    selected_committee = committee_dict[committee_num]
    print(selected_committee + ' was selected.\n')

    return selected_committee

def page_num_selector(committee):
    '''Given the chosen committee, ask the user for the number of pages
    to be scanned and checks if that number is in a valid range.'''

    response = requests.get('https://cashflow.datasektionen.se/admin/expenses/?page=1&'
        'committee=' + committee, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    max_page_num = max(1,len(soup.find('span', attrs = {'class':'step-links'}).find_all('a'))-1)

    try:
        # If for example 5 is given, page nr 1, 2, 3, 4 and 5 of the receipts will be scanned.
        page_num = int(input('Insert the number of pages (1-' + str(max_page_num) + ') to scan: '))
    except ValueError:
        sys.exit('Input has to be a number.')

    if max_page_num < page_num or page_num < 1:
        sys.exit('You submitted an invalid number, submit a number in the range of 1-'
            + str(max_page_num) + '.')
    return page_num

def receipt_cost_to_float(tag):
    '''Finds and converts the cost of the receipt (string) to float.'''

    cost_string = tag.find('td', attrs = {'class':'right'}).text.split(' ')[0]
    return float(replacer(cost_string))

def replacer(cost_string):
    '''Replaces unwanted characters in the cost_string so that
    the float function can convert the string to float.'''

    replacers = {',':'.', '\xa0':''}
    for key, value in replacers.items():
        cost_string = cost_string.replace(key, value)
    return cost_string

main()
