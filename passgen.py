#!/usr/bin/env python3
import os
import pyperclip
from termcolor import colored
import random
import sys
import time
import argparse

# password_length = 10

parser = argparse.ArgumentParser(description='Generate random passwords, copy to clipboard, erase clipboard')
# Read this to customize this boilerplate:
# https://docs.python.org/3.3/library/argparse.html
parser.add_argument('integers', metavar='n (The length of the passwords to be generated)', type=int, nargs='+',
                    help='The length of the passwords to be generated.')
# nargs='+',
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))

# End argparse boilerplate

if __name__ == '__main__':
    password_size = None
    password_array = []

    # Get the terminal dimensions
    rows, columns = os.popen('stty size', 'r').read().split()

    for row in range(int(rows) - 2):
        if len(sys.argv) > 1:
            password_size = sys.argv[1]
        elif sys.argv[1] == '':
            password_size = random.randint(10, 32)

        # Limit charset to the ascii codes between 33 and 126:
        # !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}
        password_string = ''.join([chr(random.randint(33, 126)) for i in range(0, int(password_size))])

        # numbers = chr(random.randint(48, 57))
        # lowers = chr(random.randint(97, 122))
        # uppers = chr(random.randint(65, 90))
        # symbols1 = chr(random.randint(33, 47))

        # Add the password to the array
        password_array.append(password_string)
        row += 1

    # Sort the passwords by their length, descending
    password_array.sort(key=len, reverse=True)

    # Print each password with its index number
    for index_number in range(len(password_array)):
        #print("%02d   " % (i,) + password_array[i])

        # Print the index number of this password in the left column
        #print("%02d   " % (index_number,), end = '')
        print(colored("%02d   ", 'green') % (index_number,), end = '')

        password = password_array[index_number]

        for character in password:

            # print symbols in yellow
            if ord(character) in range(33,48):

                print(colored(character, 'yellow'), end='')

            # print uppercase strings in white
            elif ord(character) in range(65,91):

                print(colored(character, 'white'), end='')

            # print lowercase strings in red
            elif ord(character) in range(97,123):

                print(colored(character, 'red'), end='')

            # print numbers in cyan
            elif ord(character) in range(48,58):

                print(colored(character, 'cyan'), end='')

            else:
                # print the rest of the symbols in yellow (ASCII 123 - 126)
                print(colored(character, 'yellow'), end = '')

        print('')

    # Ask the user which password to save
    password_to_save = int(input('Enter the number of the password you want sent to the clipboard: '))

    try:
        # Copy the password to the clipboard
        pyperclip.copy(password_array[password_to_save])

    except pyperclip.PyperclipException:

        print("\nError")
        print("If you're on Linux and seeing this error it probably means that you don't have a clipboard program installed. ")
        print("You can fix this by installing one of the copy/paste mechanisms:\n")
        print("    'sudo apt-get install xsel' to install the xsel utility.")
        print("    'sudo apt-get install xclip' to install the xclip utility.")
        print("    'pip3 install gtk' to install the gtk Python module.")
        print("    'pip3 install PyQt4' to install the PyQt4 Python module.")
        exit()

    # Show a countdown timer leading up to erasing the clipboard after 60 seconds
    for i in range(60,0,-1):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(1)

    # Copy unprintable data to the clipboard
    pyperclip.copy(''.join([chr(random.randint(1, 31)) for i in range(0, len(password_array[-1]))]))
