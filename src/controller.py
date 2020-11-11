import sys

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



def controller():
    command = ''
    while(command.upper() not in EXIT_MARKERS):
        command = input('>')
        args = []

        # read all arugments
        for arg in command.split():
            args.append(arg.lower())
        
        # if user wants to quit program
        if arg[0] in EXIT_MARKERS:
            print('Ending Sesson...')
            sys.exit()
        
        displayStats(args)
        

def main():
    controller()

if __name__ == '__main__':
    main()

