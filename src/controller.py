import sys
from authenticate import authenticate
import model

EXIT_MARKERS = {'q', 'quit'}

def findCurrency(currency):
    return 1

def displayStats(args):

    # if stats for all currencies (owned now and before) are required
    if args[0] == 'all':
        if len(args) == 1: # display basic stats
            return 1
            
    # if stats for currently owned currencies are required        
    elif args[0] == 'curr':
        if len(args) == 1:
            return 2
    else:
        currency = findCurrency(args[0])
        if (currency == None):
            print('Currency stats not found. Try another currency.')
            return 0
        
# returns stats for all currently held portfolio
def getPortfolioStats(args):
    return 1

# handles user input and delegation of requests
def controller():
    # initiate authentication
    # get an auth object in return
    auth = authenticate()

    # if program doesn't exit during authentication,
    # initiate user input
    command = ''
    while(command.upper() not in EXIT_MARKERS):
        command = input('> ') or 'empty'
        args = []

        # parse user input into readable commands
        for arg in command.split():
            args.append(arg.lower())
        
        # CHECK FOR HIGH LEVEL INPUT TYPES (exit request, empty or valid input)
        # if user wants to quit program
        if args[0] in EXIT_MARKERS:
            print('Ending Sesson...')
            sys.exit()
        # if input is empty
        elif args[0] == 'empty':
            print('No input entered... Check README file for usage instructions.')       
        # all other inputs (checked for validity later)
        else:
            displayStats(args)        

def main():
    controller()

if __name__ == '__main__':
    main()

