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
API_URL = 'https://api.coinbase.com/v2/'

def load_environment_variables():
    # # API_KEY = input('Enter API KEY: ')
    # print(API_KEY)
    # # API_SECRET = input('Enter API SECRET: ')
    # print(API_SECRET)
    print('Authenticating...')
    print()
    
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

# TODO: ADD SSL encryption
def authenticate():
    load_environment_variables()
    auth = CoinbaseWalletAuth(API_KEY, API_SECRET)
    
    # for acc in range(len(accountIds)):
    #     print('====')
    #     print(accountIds[acc])
    #     print(accountNames[acc])
    return auth
    
def main():
    auth = authenticate()
    #getClientProfile(auth)    
    # getAllClientAccounts(auth)
    # getClientPortfolio(auth)
    # getClientAccount('ETH', auth)

if __name__ == '__main__':
    main()