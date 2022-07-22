# Cashflow Webscraper
Finds all receipts that have been approved by us (ekoms) but not yet confirmed to be in the ledger.

## How To Use
Since you have to be logged in as an admin the webscraper will need a valid admin session cookie. This is very easy to set up in order to start using cashflow_scraper.py.

In cashflow_scraper.py, there are two empty dictionaries, cookies and headers. The video below shows how to generate these two dictionaries. The webpage used to convert the curl command to python dictionaries can be found [here.](https://curlconverter.com/#python) When the dictionaries are generated, just copy and paste them into the python file and you are set to use the webscraper. Just make sure to also download via pip the libraries requests, html5lib and beautifulsoup4.

https://user-images.githubusercontent.com/58815745/180486620-95c6bd73-b3e7-4967-9c21-87dc376dcbf8.mp4

## Important Note
The webscraper will only work for Studs22, modifications will have to be made by the user if it needs to be used elsewhere. See the committee parameter in the URL used for the GET requests.
