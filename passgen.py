#!/usr/bin/env python3
import os
import pyperclip
from termcolor import colored
import random
import sys
import time
import argparse

# Argument parsing
parser = argparse.ArgumentParser(description='Generate random passwords, copy to clipboard, erase clipboard')

parser.add_argument('-L', '--password-length', default=20, help='The length of the passwords to be generated.')

parser.add_argument('-w', '--random-words', action='store_true', help='Embed a random English word within each password.')

args = parser.parse_args()


def create_english_wordlist() -> object:

    # Using the wordlist from MacOS
    wordlist = [line.strip() for line in open('/usr/share/dict/words')]

    wordlist_length = wordlist.__len__()

    return wordlist, wordlist_length

def get_random_word(wordlist, wordlist_length):

    word = wordlist[random.randint(0, wordlist_length)]

    return word, len(word)


if __name__ == '__main__':
    password_size = int(args.password_length)
    #print(args.password_length)
    password_array = []

    # Create a list of English words
    wordlist, wordlist_length = create_english_wordlist()

    # Get the terminal dimensions
    rows, columns = os.popen('stty size', 'r').read().split()

    # For each row, we create a password
    for row in range(int(rows) - 2):


        if args.random_words:

            # Blank out the random word first
            #random_word = ''

            # Grab a random English word and its length
            random_word, random_word_length = get_random_word(wordlist, wordlist_length)

            #print(random_word_length, password_size)

            if random_word_length <= int(password_size):

                # We didn't need to modify the length so we just go ahead and rename it
                random_word_of_proper_length = random_word
                #print(random_word_of_proper_length)

            else:

                if random_word_length > int(password_size):

                    # The random word is too long for the password it will inhabit
                    # Chop the random word down to about 70% as long as the password
                    truncated_random_word_length = round(int(password_size) * 0.7)

                    # Randomly decide to chop off the beginning or the end of the word
                    # It will be mod 2 only 1/3 of the time. This way we will more often
                    # use the beginning of the word, that being easier to read.
                    if not random.randint(0,2) % 2:

                        # For a 10 character word, we want the first 7 characters only
                        random_word_of_proper_length = random_word[:truncated_random_word_length]

                    else:

                        # For a 10 character word, we want the last 7 characters only
                        random_word_of_proper_length = random_word[truncated_random_word_length:]

                    #print(colored(random_word_of_proper_length, 'magenta'))
                    #exit()

            # Now that we have a random word of the right length,
            # build a password around it
            password_string = random_word_of_proper_length

            if random.choice([0, 1]) == 0:
                #print("Right")
                # Append random chars to the right
                password_string += ''.join([chr(random.randint(33, 126)) for i in range(0, int(password_size - len(random_word_of_proper_length)))])

            #elif random.choice([0, 1]) == 1:
            else:
                #print("Left")
                # Prepend random chars to the left
                random_string = ''.join([chr(random.randint(33, 126)) for i in
                                            range(0, int(password_size - len(random_word_of_proper_length)))])

                password_string = (random_string + password_string)

            #else:
                # For now this is a bug. But for now I'll split the difference by dividing the
                # length of the random chars by 2 and doing both the left and the right.
                # I asked for help at:
                # https://stackoverflow.com/questions/67239230/why-does-random-choice-sometimes-not-make-any-choice

             #   password_string += ''.join([chr(random.randint(33, 126)) for i in range(0, int(password_size - int((int(len(random_word_of_proper_length))))/2))])

                #random_string = ''.join([chr(random.randint(33, 126)) for i in
                 #                range(0, (int(password_size - int(len(random_word_of_proper_length))/2)))])

                #password_string = (random_string + password_string)

        else:

            # If not wanting a random word in the passwords, then just
            # generate a random string for each password
            # Limit charset to the ascii codes between 33 and 126:
            # numbers = chr(random.randint(48, 57))
            # lowers = chr(random.randint(97, 122))
            # uppers = chr(random.randint(65, 90))
            # symbols1 = chr(random.randint(33, 47))
            # !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}
            password_string = ''.join([chr(random.randint(33, 126)) for i in range(0, int(password_size))])

        # Add the newly created password to the array
        password_array.append(password_string)
        row += 1

    # Sort the passwords by their length, descending
    # password_array.sort(key=len, reverse=True)

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



