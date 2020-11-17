# ===============================
# MODEL: ACCESS USER ACCOUNT DATA
# ===============================

# Interacts with API Endpoints
# A model object is built as soon as the user first authenticates
# Controller imports the Model class and creates a Model object
# The model talks directly to the back end

import json, requests
from requests import auth

API_URL = 'https://api.coinbase.com/v2/'
API_ENDPOINTS = {
    'price' : 'prices/%s/spot', # %s is currency_pair, ex: 'btc_cad'
    'transactions' : 'accounts/%s/transactions', # %s is account id
    'buys' : 'accounts/%s/buys', # %s is account id
    'sells' : 'accounts/:account_id/sells', # %s is account id
    'profit' : 'accounts/%s/transactions', # %s is account id
    'balance' : 'accounts/%s' # %s is account id
}

class AccountModel():
    def __init__(self, auth):
        self.auth = auth
        self.currencies_all = {}
        self.currencies_current = {}
        self.query_currencies = []
        self.isUSD = False
        self.isPCT = False
        self.buildModel()
        
    def buildModel(self):
        # get all currencies owned currently and in the past
        r = requests.get(API_URL + 'accounts', auth=self.auth)
        data = r.json()['data']
        # print(data)
        # iterate through json to build currency hashtables {'name':'id'}
        for acc in data:
            if acc['updated_at'] != None: # if currency owned at any time
                self.currencies_all[acc['currency']['code']] = None
                if float(acc['balance']['amount']) > 0: # if currency owned currently
                    self.currencies_current[acc['currency']['code']] = None
        print('User data loaded.')
    
    def displayStats(self, args):
        # 3 types of primary requests
        # 'all': display stats for all currencies owned at any time
        # 'curr': display stats for currencies owned currently
        # 'btc': display stats for currency name provided, ex: 'btc'
        
        # build a list of currencies to fetch data for
        if args[0] == 'all':
            self.query_currencies = self.currencies_all.keys()
        elif args[0] == 'curr':
            self.query_currencies = self.currencies_current.keys()
        else:   
            # user own(s/ed) this currency
            if args[0] in self.currencies_all:
                self.query_currencies.append(args[0])
            else:
                print('User doesn\'t have a wallet with this currency, please provide a valid argument.')
                return

        # use second argument to route user request
        if args[1] == 'price':
            self.displaySpotPrice()
        elif args[1] == 'owned':
            self.displayOwned()
        elif args[1] == 'transactions':
            self.displayTransactions()
        elif args[1] == 'buys':
            self.displayBuys()
        elif args[1] == 'sells':
            self.displaySells()
        elif args[1] == 'profit':
            self.displayProfit()
        elif args[1] == 'balance':
            self.displayBalance()
        else: # TODO: move this to controller
            print('No query (second argument) provided for currency, please provide a valid argument.')

    def displayOwned(self):
        self.queryTitlePrinter('CURRENCIES OWNED:')
        for currency in self.query_currencies:
            print(currency)

    def displaySpotPrice(self):
        self.queryTitlePrinter('CURRENT PRICE FOR 1 UNIT OF:')
        for currency in self.query_currencies:
            r = requests.get(API_URL + 'prices/%s-usd/spot' % (currency), auth=self.auth)
            data = r.json()['data']
            print('%s: %s USD' % (currency, data['amount']))
        return 1

    def displayTransactions():
        return 1

    def displayBuys():
        return 1

    def displaySells():
        return 1

    def displayProfit():
        return 1

    def displayBalance():
        return 1

    def queryTitlePrinter(self, str):
        print('============================')
        print(str)
        print('----------------------------')
# TODO:
# FINISH DISPLAY STATS ROUTING
# CREATE QUERY FUNCTIONS