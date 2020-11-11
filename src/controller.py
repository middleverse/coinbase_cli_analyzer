import sys
from authenticate import authenticate
from model import AccountModel 

EXIT_MARKERS = {'q', 'quit'}
      
# handles user input and delegation of requests
def controller():
    # initiate authentication
    # get an auth object in return
    auth = authenticate()

    # create model
    m = AccountModel(auth)
    m.buildModel() # TODO: make this an inherent model call?
    
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
            m.displayStats(args)      

def main():
    controller()

if __name__ == '__main__':
    main()

