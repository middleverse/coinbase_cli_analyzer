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
    'prices' : 'prices/%s-usd/spot', # %s is currency_pair, ex: 'btc_cad'
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
        self.currencies_previously_held = {}
        self.query_currencies = []
        self.native_currency = ''
        self.buildModel()
        
    def buildModel(self):
        # get all currencies owned currently and in the past
        r = requests.get(API_URL + 'accounts', auth=self.auth)
        data = r.json()['data']
        # print(data)
        # iterate through json to build currency hashtables {'name':'id'}
        for acc in data:
            if acc['updated_at'] != None: # if currency owned at any time
                self.currencies_all[acc['currency']['code']] = acc['id']
                if float(acc['balance']['amount']) > 0: # if currency owned currently
                    self.currencies_current[acc['currency']['code']] = acc['id']
                else: # currency previously held
                    self.currencies_previously_held[acc['currency']['code']] = acc['id']

        r = requests.get(API_URL + 'user', auth=self.auth)
        data = r.json()['data']
        self.native_currency = data['native_currency']
        print('User data loaded.')
    
    def displayStats(self, args):
        # 3 types of primary requests
        # 'all': display stats for all currencies owned at any time
        # 'curr': display stats for currencies owned currently
        # 'btc': display stats for currency name provided, ex: 'btc'
        self.query_currencies = []
        # figure out which currencies to display data for
        if args[0] == 'ALL':
            self.query_currencies = list(self.currencies_all.keys())
        elif args[0] == 'CURR':
            self.query_currencies = list(self.currencies_current.keys())
        else:   
            # user own(s/ed) this currency
            if args[0] in self.currencies_all:
                self.query_currencies.append(args[0])
            else:
                print('User doesn\'t have a wallet with this currency, please provide a valid argument.')
                return

        # use second argument to route user request
        if args[1] == 'PRICE':
            self.displaySpotPrice()
        elif args[1] == 'OWNED':
            self.displayOwned()
        elif args[1] == 'TRANSACTIONS':
            self.displayTransactions()
        elif args[1] == 'BUYS':
            self.displayBuys()
        elif args[1] == 'SELLS':
            self.displaySells()
        elif args[1] == 'PROFIT':
            if args[0] == 'CURR' or args[0] in self.currencies_current:
                print('Profits can only be displayed for previously held currencies!')
            else:
                self.displayProfit()
        elif args[1] == 'BALANCE':
            if args[0] == 'ALL' or args[0] in self.currencies_previously_held:
                print('Profits can only be displayed for currently held currencies!')
            else:
                self.displayBalance()
        else: # TODO: move this to controller
            print('No query (second argument) provided for currency, please provide a valid argument.')

    def displayOwned(self):
        self.queryTitlePrinter('CURRENCIES OWNED:')
        for currency in self.query_currencies:
            print(currency)
            print()

    def displaySpotPrice(self):
        self.queryTitlePrinter('CURRENT PRICE FOR 1 UNIT OF:')
        for currency in self.query_currencies:
            r = requests.get(API_URL + 'prices/%s-cad/spot' % (currency), auth=self.auth)
            data = r.json()['data']
            print('%s: %s %s' % (currency, data['amount'], self.native_currency))
            print()

    def displayTransactions(self):
        self.queryTitlePrinter('TRANSACTIONS PER CURRENCY:')
        for currency in self.query_currencies:
            print(currency)
            r = requests.get(API_URL + 'accounts/%s/transactions' % (currency), auth=self.auth)
            data = r.json()['data']
            for transaction in data:
                if transaction['type'].lower() != 'buy' and transaction['type'].lower() != 'sell':
                    continue
                print('Type: ' + transaction['type'].upper())
                print('Amount: %s %s' % (transaction['amount']['amount'], currency)) # TODO: didn't endpoint return in USD? Check again
                print('Status: ' + transaction['status'])
                print('Time: ' + transaction['updated_at'])
                print('-----')
            print()

    def displayBuys(self):
        self.queryTitlePrinter('BUYS PER CURRENCY:')
        for currency in self.query_currencies:
            print(currency)
            r = requests.get(API_URL + 'accounts/%s/buys' % (currency), auth=self.auth)
            data = r.json()['data']
            for transaction in data:
                print('Type : BUY')
                print('Currency Amount: %s %s' % (transaction['amount']['amount'], currency))
                print('Native Amount: %s %s' % (transaction['subtotal']['amount'], transaction['subtotal']['currency']))
                print('Native Fee Amount: %s %s' % (transaction['fee']['amount'], transaction['fee']['currency']))
                print('Status: ' + transaction['status'])
                print('Time: ' + transaction['updated_at']) 
                print('-----')
            print()

    def displaySells(self):
        self.queryTitlePrinter('SELLS PER CURRENCY:')
        for currency in self.query_currencies:
            print(currency)
            r = requests.get(API_URL + 'accounts/%s/sells' % (currency), auth=self.auth)
            data = r.json()['data']
            for transaction in data:
                print('Type : SELL')
                print('Currency Amount: %s %s' % (transaction['amount']['amount'], currency))
                print('Native Amount: %s %s' % (transaction['subtotal']['amount'], transaction['subtotal']['currency']))
                print('Native Fee Amount: %s %s' % (transaction['fee']['amount'], transaction['fee']['currency']))
                print('Status: ' + transaction['status'])
                print('Time: ' + transaction['updated_at']) 
                print('-----')
            print()

    def displayProfit(self):
        self.queryTitlePrinter('PROFITS: ')
        print('>> NOTE: Profits are only displayed for previously held currencies.\n')
        profit_queries = []
        global_net = 0
        if len(self.query_currencies) == 1: # print profit for one currency
            profit_queries = self.query_currencies
        else:
            profit_queries = self.currencies_previously_held
            # print profit for all currencies (prev held)          
            # for each currency that has been bought and sold and doesn't have a balance
            # hence any currency that isn't in the current portfolio
            # -> print a profit/loss statement
            # keep a total tally of these profits/losses
            # -> print a totals statement at the end
            # NOTE: we can't print profits for currencies with balance since 
            # there can be multiple positions bought and sold at various times, gets tricky
        for currency in profit_queries:
            print(currency)
            r = requests.get(API_URL + 'accounts/%s/transactions' % (currency), auth=self.auth)
            data = r.json()['data']
            local_net = 0 # currency profit
            for transaction in data:
                if transaction['type'] == 'sell' and transaction['status'] == 'completed':
                    local_net += float(transaction['native_amount']['amount']) * -1
                if transaction['type'] == 'buy' and transaction['status'] == 'completed':
                    local_net -= float(transaction['native_amount']['amount'])
            global_net += local_net
            print('Net Profit: %s %s' % (round(local_net, 2), self.native_currency))
            print()
        if len(profit_queries) > 1:
            print('Total Profit: %s %s' % (round(global_net, 2), self.native_currency))
            print()

    def displayBalance(self):
        self.queryTitlePrinter('BALANCE: ')
        global_balance = 0
        for currency in self.query_currencies:
            
            r = requests.get(API_URL + 'accounts/%s/transactions' % (currency), auth=self.auth)
            data = r.json()['data']
            local_balance = 0 # currency profit
            for transaction in data:
                if transaction['type'] == 'sell' and transaction['status'] == 'completed':
                    local_balance -= float(transaction['native_amount']['amount']) * -1
                if transaction['type'] == 'buy' and transaction['status'] == 'completed':
                    local_balance += float(transaction['native_amount']['amount'])
            global_balance += local_balance
            if len(self.query_currencies) == 1:
                print(currency)
                print('Balance: %s %s' % (round(local_balance, 2), self.native_currency))
                print()
        if len(self.query_currencies) > 1:
            print('Account Balance: %s %s' % (round(global_balance, 2), self.native_currency))
            print()


        

    def queryTitlePrinter(self, str):
        print('============================')
        print(str)
        print('----------------------------')