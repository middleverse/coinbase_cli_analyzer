# ==============================
# Authenticate User With API Key
# ==============================

# 'hmac' for MAC (signing) functionality
# 'hashlib' for sha256 (hash) functionality
# 'requests' for HTTP access
import json, hmac, hashlib, time, requests
from requests.auth import AuthBase

API_KEY = ''
API_SECRET = ''

def loadEnvironmentVariables():
    API_KEY = input('Enter API KEY: ')
    print(API_KEY)
    API_SECRET = input('Enter API SECRET: ')
    print(API_SECRET)
    print('Authenticating...')
    
# custom authentication for Coinbase API
class CoinbaseWalletAuth(AuthBase):
    # load api key and secret key
    def __init__(self, apiKey, secretKey):
        self.apiKey = apiKey
        self.secretKey = secretKey
    # return auth request
    def __call__(self, request):
        timestamp = str(int(time.time()))
        # prehash string (message) : timestamp + method + requestPath + body
        message = timestamp + request.method + request.path_url + (request.body or '')
        # convert to bytes, expected format for hmac
        keyBytes = bytes(self.secretKey, 'latin-1') # string to bytes
        messageBytes = bytes(message, 'latin-1') # string to bytes
        # sign using secret key and prehash string (message)
        signature = hmac.new(keyBytes, messageBytes, hashlib.sha256).hexdigest()
        
        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.apiKey,
        })
        return request

def authenticate():
    apiUrl = 'https://api.coinbase.com/v2/'
    loadEnvironmentVariables()
    auth = CoinbaseWalletAuth(API_KEY, API_SECRET)

    # get current user
    r = requests.get(apiUrl + 'accounts', auth=auth)
    loaded_json = r.json()
    print(loaded_json['data'][20])

    accountIds = []
    accountNames = []
    for x in loaded_json['data']:
        if x['updated_at'] != None:
            accountIds.append(x['id'])
            accountNames.append(x['name'])

    for acc in range(len(accountIds)):
        print('====')
        print(accountIds[acc])
        print(accountNames[acc])


def main():
    authenticate()

if __name__ == '__main__':
    main()