# ==============================
# Authenticate User With API Key
# ==============================

# 'hmac' for MAC (signing) functionality
# 'hashlib' for sha256 (hash) functionality
# 'requests' for HTTP access
import json, hmac, hashlib, time, requests, sys
from requests.auth import AuthBase

API_KEY = 'qVBekOChVfjgMEvS'
API_SECRET = 'TlO0IJbw0wFpOa3NeeT9wJJJU6Wx0nkO'
API_URL = 'https://api.coinbase.com/v2/'

def load_environment_variables():
    # # API_KEY = input('Enter API KEY: ')
    # print(API_KEY)
    # # API_SECRET = input('Enter API SECRET: ')
    # print(API_SECRET)
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
        
        # create headers expected by coinbase API (refer to coinbase documentation for syntax)
        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.apiKey,
        })
        return request

# TODO: ADD SSL encryption
def authenticate():
    load_environment_variables()
    
    # create auth object for endpoint requests
    auth = CoinbaseWalletAuth(API_KEY, API_SECRET)
    
    # get account data
    r = requests.get(API_URL + 'user', auth=auth)
    
    # if authentication was unsucessful, exit system
    if 'errors' in r.json():
        print('Authentication unsuccesful. Check credentials.')
        sys.exit()

    # print user name and email    
    data = r.json()['data']
    print('Authentication successful.')
    print()
    print("User Name: %s" % data['name'])
    print("User Email: %s" % data['email'])
    print()
    print("Check README for usage instructions. Type \"q\" to end session.") 
    
    return auth