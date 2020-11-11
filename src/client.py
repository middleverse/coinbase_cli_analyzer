import json
import requests

API_URL = 'https://api.coinbase.com/v2/'

# return client name, email
def getClientProfile(auth):
    r = requests.get(API_URL + 'user', auth=auth)
    data = r.json()['data']

    print("User Name: %s" % data['name'])
    print("User Email: %s" % data['email']) 

def getAllClientAccounts(auth):
    r = requests.get(API_URL + 'accounts', auth=auth)
    data = r.json()['data']
    accountIds = []
    accountNames = []
    for acc in data:
        if acc['updated_at'] != None:
            accountIds.append(acc['id'])
            accountNames.append(acc['name'])
            print(acc['id'])
            print(acc['name'])
            print()
    print('All accounts listed!')

def getClientAccount(acc_name, auth):
    r = requests.get(API_URL + 'accounts/' + acc_name, auth=auth)
    acc_data = r.json()['data']
    print('Currency: ' + acc_data['balance']['currency'])
    print('Balance: ' + acc_data['balance']['amount'])

# return accounts with balance
def getClientPortfolio(auth):
    r = requests.get(API_URL + 'accounts', auth=auth)
    data = r.json()['data']
    for acc in data:
        if float(acc['balance']['amount']) > 0:
            print('Currency: %s' % acc['balance']['currency'])
            print('Native Balance: %s' % acc['balance']['amount'])
            # TODO: Add USD balance
            print()
    print('All accounts listed!')