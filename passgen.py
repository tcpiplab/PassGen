#!/usr/bin/env python3
import os
import pyperclip
from termcolor import colored
import random
import sys
import time
import argparse

# Argument parsing

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

parser.add_argument('-l', '--password-length', default=20, help='The length of the passwords to be generated.')

parser.add_argument('-w', '--random-words', action='store_true', help='Embed a random English word within each password.')

parser.add_argument('-j', '--japanese', action='store_true', help='Include random Japanese characters in each password.')

args = parser.parse_args()


def create_english_wordlist() -> object:

    # TODO: Detect OS, choose this file or the Linux dictionary. Error out if Windows?

    # Using the wordlists from MacOS
    wordlist = [line.strip() for line in open('/usr/share/dict/words')]

    wordlist += [line.strip() for line in open('/usr/share/dict/propernames')]

    wordlist += [line.strip().replace(" ", "") for line in open('/usr/share/dict/web2a')]

    wordlist += [line.strip().replace(" ", "") for line in open('/usr/share/zoneinfo.default/iso3166.tab')]

    wordlist_length = wordlist.__len__()

    return wordlist, wordlist_length

def get_random_word(wordlist, wordlist_length):

    word = wordlist[random.randint(0, wordlist_length)]

    # TODO: For random words longer than 8 chars, replace one letter in the middle with another char

    return word, len(word)


def get_memorable_password(size_of_password):

    # TODO: add check for japanese flag and add japanese chars if needed.
    random_word_of_proper_length = ''

    if size_of_password < 20:
        print("That won\'t work.")
        print("You should have a password of 20 characters or more when using")
        print("the random word feature.")
        exit()

    # Grab a random English word and its length
    random_word, random_word_length = get_random_word(wordlist, wordlist_length)

    # Chop the random word down to about 60% as long as the password
    truncated_random_word_length = round(int(size_of_password) * 0.6)

    random_word_of_proper_length = random_word[:truncated_random_word_length]

    # Now surround the random word with random chars on each side
    while len(random_word_of_proper_length) < int(password_size):

        random_word_of_proper_length = add_entropy_right(random_word_of_proper_length)

        # About half of the time, skip adding the left char. So we have more on the right
        if random.randint(0,1) == 0:

            pass

        else:

            random_word_of_proper_length = add_entropy_left(random_word_of_proper_length)

    return random_word_of_proper_length





def add_entropy_right(rand_word):

    # Append one random char to the right
    rand_word += ''.join(chr(random.randint(33, 126)))

    return rand_word

def add_entropy_left(rand_word):

    # Append one random char to the left
    random_char = ''.join(chr(random.randint(33, 126)))

    rand_word = (random_char + rand_word)

    return rand_word


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

        if len(sys.argv) < 1:
            password_size = random.randint(10, 32)

        if args.random_words:
            password_string = get_memorable_password(password_size)

        elif args.japanese:
            # Limit charset to the ascii codes between 33 through 126 and 12353 through 12436:
            # !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}
            # ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのばぱひびぴふぶぷへべぺほぼぽまみむ
            # めもゃやゅゆょよらりるれろゎわゐゑをんゔ
            # numbers = chr(random.randint(48, 57))
            # lowers = chr(random.randint(97, 122))
            # uppers = chr(random.randint(65, 90))
            # symbols1 = chr(random.randint(33, 47))
            # hiragana = chr(random.randint(12353, 12436))

            password_string = ''.join([chr(random_ascii_or_hiragana()) for i in range(0, int(password_size))])



        else:

            # If not wanting a random word in the passwords,
            # and not wanting Japanese chars, then just
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
        # Unneeded row is defined at the top of this loop
    #   row += 1

    # Sort the passwords by their length, descending
    password_array.sort(key=len, reverse=True)

    # TODO: Split the printing of the passwords out to a separate function
    # Print each password with its index number
    for index_number in range(len(password_array)):

        # Print the index number of this password in the left column
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

    # TODO: Get a PR from Tunl-Lite for his fix for when the wrong char is entered
    # Ask the user which password to save
    password_to_save = input_number('Enter the number of the password you want sent to the clipboard: ')

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

    # Copy unprintable data to the clipboard
    pyperclip.copy(''.join([chr(random.randint(1, 31)) for i in range(0, len(password_array[-1]))]))
