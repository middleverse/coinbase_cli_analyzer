import sys
from authenticate import authenticate
from model import AccountModel 

EXIT_MARKERS = {'Q', 'QUIT'}
      
# handles user input and delegation of requests
def controller():
    # initiate authentication
    # get an auth object in return
    auth = authenticate()

    # create model
    m = AccountModel(auth)
    
    # if program doesn't exit during authentication,
    # initiate user input
    command = ''
    while(command.upper() not in EXIT_MARKERS):
        command = input('> ') or 'EMPTY_STRING'
        print()
        args = []

        # parse user input into readable commands
        for arg in command.split():
            args.append(arg.upper())
        
        # CHECK FOR HIGH LEVEL INPUT TYPES (exit request, empty or valid input)
        # if user wants to quit program
        if args[0] in EXIT_MARKERS:
            print('Ending Sesson...')
            sys.exit()
        # if input is empty
        elif args[0] == 'EMPTY_STRING':
            print('No input entered... Check README file for usage instructions.')       
        # all other inputs (checked for validity later) 
        else:
            m.displayStats(args)   
        print()   

def main():
    controller()

if __name__ == '__main__':
    main()

