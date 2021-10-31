#!/usr/bin/env python3
import os
import pyperclip
from termcolor import colored
import random
import sys
import time
import argparse


# Gather a random selection from two ranges for the password string
def random_ascii_or_hiragana():

    random_num = random.randint(1, 2)

    if random_num == 1:
        return random.randint(33, 126)
    else:
        return random.randint(12353, 12436)


# Provide repeatable request for index number if entry is not a number
def input_number(message):
    while True:
        try:
            input_selection = int(input(message))
            if input_selection not in range(0, len(password_array)):
                print(colored("Selection {} not within range", 'red').format(input_selection))
                continue
        except ValueError:
            print(colored("Selection is invalid!", 'red'))
            continue
        else:
            return input_selection


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

        # Limit charset to the ascii codes between 33 through 126 and 12353 through 12436:
        # !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}
        # ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのばぱひびぴふぶぷへべぺほぼぽまみむ
        # めもゃやゅゆょよらりるれろゎわゐゑをんゔ
        password_string = ''.join([chr(random_ascii_or_hiragana()) for i in range(0, int(password_size))])

        # numbers = chr(random.randint(48, 57))
        # lowers = chr(random.randint(97, 122))
        # uppers = chr(random.randint(65, 90))
        # symbols1 = chr(random.randint(33, 47))
        # hiragana = chr(random.randint(12353, 12436))

        # Add the password to the array
        password_array.append(password_string)
        # Uneeded row is defined at the top of this loop
    #   row += 1

    # Sort the passwords by their length, descending
#   for i in password_array:
    #   print(len(i))
#   password_array.sort(key=len, reverse=True)

    # Print each password with its index number
    for index_number in range(len(password_array)):
        # print("%02d   " % (i,) + password_array[i])

        # Print the index number of this password in the left column
        # print("%02d   " % (index_number,), end = '')
        print(colored("%02d   ", 'green') % (index_number,), end='')

        password = password_array[index_number]

        for character in password:

            # print symbols in yellow
            if ord(character) in range(33, 48):

                print(colored(character, 'yellow'), end='')

            # print uppercase strings in white
            elif ord(character) in range(65, 91):

                print(colored(character, 'white'), end='')

            # print lowercase strings in red
            elif ord(character) in range(97, 123):

                print(colored(character, 'red'), end='')

            # print numbers in cyan
            elif ord(character) in range(48, 58):

                print(colored(character, 'cyan'), end='')

            # print hiragana in magenta
            elif ord(character) in range(12353, 12437):

                print(colored(character, 'magenta'), end='')

            else:
                # print the rest of the symbols in yellow (ASCII 123 - 126)
                print(colored(character, 'yellow'), end='')

        print('')

    # Ask the user which password to save
    password_to_save = input_number('Enter the number of the password you want sent to the clipboard: ')

    # Copy the password to the clipboard
    pyperclip.copy(password_array[password_to_save])

    # Show a countdown timer leading up to erasing the clipboard after 60 seconds
    for i in range(60, -1, -1):
        sys.stdout.write(" The clipboard will be cleared in {} seconds ".format(str(i))+'\r')
    # Switch color of prompt to red near less 10 seconds to completion
        if i < 11:
            sys.stdout.write(colored(" The clipboard will be cleared in {} seconds ", 'red').format(str(i))+'\r')
        if i < 1:
            sys.stdout.write("\033[K")
            print("The clipboard has been cleared")
        sys.stdout.flush()
        time.sleep(1)

    pyperclip.copy(''.join([chr(random.randint(1, 31)) for i in range(0, len(password_array[-1]))]))
