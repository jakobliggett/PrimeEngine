from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import SieveEratosthenes
import os

version = 0.01
methods = ['Standard Sieve of Eratosthenes', 'Settings', 'Help', 'Quit']
store_mode = 'print' #or write to file

print('Welcome to PrimeEngine v{}\n'.format(version))

def ClearScreen():
    print ('\n'*20)

def InputLoop(strng, cast_type, invalid_text='invalid argument', valid_answers = None):
    done = None
    while not done:
        value = raw_input(strng)
        try:
            if cast_type == 'int':
                new_value = int(value)
            elif cast_type == 'alpha':
                new_value = str(value).lower()
                if not new_value.isalpha():
                    #print('not alpha')
                    raise Exception
            if valid_answers != None:
                if new_value not in valid_answers:
                    #print('not in valid')
                    raise Exception
            done = True
        except:
            print(invalid_text)
    return new_value

def HandlePrimes(primes):
    filename = 'primes'
    if store_mode == 'print':
        print(primes)
    elif store_mode == 'file':
        valid = False
        i = 0
        while not valid:
            if not os.path.isfile(filename+i+'.txt'):
                valid = True
            else:
                i += 1
        with open(filename+i+'.txt', mode='w') as f:
            f.write(primes)

def main():
    for method in range(len(methods)):
        print('{} ********** {}'.format(methods[method], method))
    print('\n')

    valid_num = False
    while not valid_num:
        choice = raw_input('')
        try:
            intchoice = int(choice)
            test_for_valid_num = methods[intchoice]
            valid_num = True
        except ValueError:
            print('Invalid Choice, not a number.')
        except IndexError:
            print('Invalid Choice, number not an available choice')

    ClearScreen()
    if (methods[intchoice]).lower() == 'standard sieve of eratosthenes':
        print('The sieve of eratosthenes finds prime numbers')
        limit = InputLoop('Find all primes under: ', 'int')
        primes = SieveEratosthenes.sieve(limit)
        HandlePrimes(primes)
    elif (methods[intchoice]).lower() == 'settings':
        selection = InputLoop('(P)rint primes or store in (F)ile: ', 'alpha', valid_answers=['p', 'f'])
        if selection == 'p':
            store_mode = 'print'
        elif selection == 'f':
            store_mode = 'file'
    elif (methods[intchoice]).lower() == 'quit':
        print('Quitting, thank you')
        quit()

while True:
    main()