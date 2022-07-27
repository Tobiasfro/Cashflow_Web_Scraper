# Cashflow Webscraper
Given a committee and the number of pages of receipts to scan, the web scraper finds all the receipts that have been approved but not yet confirmed to be in the ledger. It also prints the URL's to these receipts in a .txt file. Also prints (in the terminal) the number of found unconfirmed receipts and the total cost of them in SEK.

## How To Use
Since you have to be logged in as an admin, the web scraper will need a valid admin session cookie. This is very easy to set up and is necessary in order to start using cashflow_scraper.py.

In cashflow_scraper.py, there are one empty dictionary, called cookies. The video below shows how to generate this dictionary. The webpage used to convert the curl command to a python dictionary can be found [here.](https://curlconverter.com/#python) When the dictionary is generated, just copy and paste it into the python file and you are set to use the web scraper. Just make sure to also download via pip the libraries called requests and beautifulsoup4.

Type the following in the terminal to run the script
```bash
python cashflow_scraper.py
```  

https://user-images.githubusercontent.com/58815745/180486620-95c6bd73-b3e7-4967-9c21-87dc376dcbf8.mp4

## Important Note
The web scraper works not only for Studs22, it works for all of the committees in cashflow! Be free to use the web scraper outside Studs22 related activities.
