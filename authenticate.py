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
        message = timestamp + request.method + request.path_url + (request.body or '')
        keyBytes = bytes(self.secretKey, 'latin-1') # string to bytes
        messageBytes = bytes(message, 'latin-1') # string to bytes
        signature = hmac.new(keyBytes, messageBytes, hashlib.sha256).hexdigest()
        
        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.apiKey,
        })
        return request

apiUrl = 'https://api.coinbase.com/v2/'
loadEnvironmentVariables()
auth = CoinbaseWalletAuth(API_KEY, API_SECRET)

# get current user
r = requests.get(apiUrl + 'user', auth=auth)
print (r.json()) # print {u'data'}