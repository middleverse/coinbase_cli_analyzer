# ==============================
# Authenticate User With API Key
# ==============================

# 'hmac' for MAC (signing) functionality
# 'hashlib' for sha256 (hash) functionality
# 'requests' for HTTP access
import json, hmac, hashlib, time, requests, sys
from requests.auth import AuthBase

API_KEY = None
API_SECRET = None
API_URL = 'https://api.coinbase.com/v2/'

def load_environment_variables():
    global API_KEY, API_SECRET
    water = open('water.txt', 'r')
    for l in water:
        if 'API KEY:' in l.upper():
            API_KEY = str(l[9:]).rstrip()
        elif 'API SECRET:' in l.upper():
            API_SECRET = str(l[12:]).rstrip()
    
    if API_KEY == None or API_SECRET == None:
        print('API Login credentials are empty, check creds.')
    water.close()
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
    print('Authentication successful. Logged into Coinbase.\n')
    print(">> User Name: %s\n" % data['name'])
    print(">> User Email: %s\n" % data['email'])
    return auth