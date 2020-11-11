# ===============================
# MODEL: ACCESS USER ACCOUNT DATA
# ===============================

# Interacts with API Endpoints
# A model object is built as soon as the user first authenticates
# Controller imports the Model class and creates a Model object
# The model talks directly to the back end

import json, requests

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
        
    def buildModel(self):
        # get all currencies owned currently and in the past
        r = requests.get(API_URL + 'accounts', auth=self.auth)
        data = r.json()['data']

        # iterate through json to build currency hashtables {'name':'id'}
        for acc in data:
            if acc['updated_at'] != None: # if currency owned at any time
                self.currencies_all[acc['name']] = acc['id']
                if float(acc['balance']['amount']) > 0: # if currency owned currently
                    self.currencies_current[acc['name']] = acc['id']
        print('User data loaded.')
    
    def displayStats(self, args):
        # 3 types of primary requests
        # 'all': display stats for all currencies owned at any time
        # 'curr': display stats for currencies owned currently
        # 'btc': display stats for currency name provided, ex: 'btc'
        
        # build a list of currencies to fetch data for
        currency_list = []
        if args[0] == 'all':
            currency_list = self.currencies_all.keys()
        elif args[0] == 'curr':
            currency_list = self.currencies_current.keys()
        else:
            # user own(s/ed) this currency
            if args[0] in self.currencies_all:
                currency_list.append(args[0])
            else:
                print('User doesn\'t have a wallet with this currency, please provide a valid argument.')
                   
        # use second argument to route user request

