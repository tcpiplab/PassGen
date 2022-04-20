#!/usr/bin/env python3
import os
import platform
from pathlib import Path
import pyperclip
from termcolor import colored
import random
import sys
import time
import argparse

# Argument parsing

parser = argparse.ArgumentParser(description='Generate random passwords, copy to clipboard, erase clipboard')

parser.add_argument('-l', '--password-length', '--length', default=20,
                    help='The length of the passwords to be generated.')

parser.add_argument('-w', '--random-words', action='store_true',
                    help='Embed a random English word within each password.')

parser.add_argument('-j', '--japanese', action='store_true',
                    help='Include random Japanese characters in each password.')

parser.add_argument('-s', '--silent', action='store_true',
                    help='Silently return a password to the clipboard (default behavior).')

parser.add_argument('-i', '--interactive', action='store_true',
                    help='Generate a list of random passwords, allowing the user to choose one to copy to \
                    the clipboard, erase the clipboard afterward.')

args = parser.parse_args()


# Detect the OS so we know where to find word dictionary files
this_os = platform.system()


def random_ascii_or_hiragana():
    """
    Gather a random selection from two ranges for the password string
    :return:
    """

    random_num = random.randint(1, 2)

    if random_num == 1:
        return random.randint(33, 126)
    else:
        return random.randint(12353, 12436)


def input_number(message):
    """
    Provide repeating request for index number if the user's entry is not a number
    :param message:
    :return:
    """

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


def create_english_wordlist() -> object:
    """
    Determine the OS, find any existing dictionary file.
    Put those words into a list, return the list and length of the list.
    :return: list: wordlist, int: wordlist_length
    """

    # Create a wordlist list object we can populate from the words file
    wordlist = []

    # For Mac OS there are several good files we can cat together
    if this_os == 'Darwin':
        # Using the word lists from MacOS
        wordlist += [line.strip() for line in open('/usr/share/dict/words')]
        wordlist += [line.strip() for line in open('/usr/share/dict/propernames')]
        wordlist += [line.strip().replace(" ", "") for line in open('/usr/share/dict/web2a')]
        wordlist += [line.strip().replace(" ", "") for line in open('/usr/share/zoneinfo.default/iso3166.tab')]

    # For Linux we can try to find the traditional Unix words file, but it is not always there
    elif this_os == 'Linux':
        # Check if a dictionary file exists
        dictionary_path_one = Path('/usr/share/dict/words')
        dictionary_path_two = Path('/usr/dict/words')

        # Check the first possible location for a dictionary file to see if it exists
        if dictionary_path_one.is_file():
            try:
                wordlist += [line.strip() for line in open(dictionary_path_one)]
            except FileNotFoundError:
                pass
        # Check the second possible location for a dictionary file to see if it exists
        if dictionary_path_two.is_file():
            try:
                wordlist += [line.strip() for line in open(dictionary_path_two)]
            except FileNotFoundError:
                pass
        # By now we hopefully have a populated wordlist
        # But if we're on Kali Linux there probably is only known-weak-password wordlists, which we obv don't want
        elif platform.node() == 'kali':
            print('The \'-w\', \'--random-words\' option is not yet supported on Kali Linux.')
            print('This is because Kali does not have a dictionary of words to use.')
            print('Do NOT use the dictionary in /usr/share/dict. That is a dictionary of weak passwords.')
            # print('You can install one in ')
            pass
        else:
            print('Whatever kind of Linux you\'re running does not seem to have a dictionary file.')
            print('So the \'-w\', \'--random-words\' option will not work.')
            print('You can try manually placing one in \'/usr/share/dict/words\'.')
            print('If you\'re on a Debian/Ubuntu variant maybe try one of these:')
            print('    \'sudo apt-get install wamerican\'')
            print('    \'sudo apt-get install wbritish\'')
            exit()

    elif this_os == 'Windows':
        print('The \'-w\', \'--random-words\' option is not yet supported on {}.'.format(this_os))
        pass

    elif this_os == 'Java':
        print('The \'-w\', \'--random-words\' option is not yet supported on {}.'.format(this_os))
        pass

    elif this_os == '':
        print('{} can not determine the name of the OS you\'re running. '
              'This means that '.format(os.path.basename(__file__)))
        print('the \'-w\', \'--random-words\' option is not supported for your OS.')

    else:
        # For FreeBSD or anything else...
        print('The \'-w\', \'--random-words\' option is not yet supported on {}.'.format(this_os))

    wordlist_length = wordlist.__len__()

    return wordlist, wordlist_length


def get_random_word(wordlist, wordlist_length):

    word = wordlist[random.randint(0, wordlist_length)]

    # TODO: For random words longer than 8 chars, replace one letter in the middle with another char

    return word, len(word)


def get_memorable_password(size_of_password):

    # TODO: add check for japanese flag and add japanese chars if needed.

    if size_of_password < 20:
        print("That won\'t work.")
        print("You should have a password of 20 characters or more when using")
        print("the random word feature.")
        exit()

    # Grab a random English word and its length
    random_word, random_word_length = get_random_word(the_wordlist, the_wordlist_length)

    # Chop the random word down to about 60% as long as the password
    truncated_random_word_length = round(int(size_of_password) * 0.6)

    random_word_of_proper_length = random_word[:truncated_random_word_length]

    # Now surround the random word with random chars on each side
    while len(random_word_of_proper_length) < int(password_size):

        random_word_of_proper_length = add_entropy_right(random_word_of_proper_length)

        # About half of the time, skip adding the left char. So we have more on the right
        if random.randint(0, 1) == 0:

            pass

        else:

            random_word_of_proper_length = add_entropy_left(random_word_of_proper_length)

    return random_word_of_proper_length


def add_entropy_right(rand_word):
    """
    Append one random char to the right
    :param rand_word:
    :return:
    """

    rand_word += ''.join(chr(random.randint(33, 126)))

    return rand_word


def add_entropy_left(rand_word):
    """
    Append one random char to the left
    :param rand_word:
    :return:
    """

    random_char = ''.join(chr(random.randint(33, 126)))

    rand_word = (random_char + rand_word)

    return rand_word


def print_passwords_interactive(password_array):
    """

    :param password_array:
    :return:
    """

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


def interactive_mode(array_of_passwords):

    print_passwords_interactive(array_of_passwords)

    # Ask the user which password to save
    password_to_save = input_number('Enter the number of the password you want sent to the clipboard: ')

    copy_to_clipboard(array_of_passwords, password_to_save)

    clipboard_countdown_and_erase()


def clipboard_countdown_and_erase():

    # Show a countdown timer leading up to erasing the clipboard after 60 seconds
    for i in range(60, -1, -1):
        sys.stdout.write(" The clipboard will be cleared in {} seconds ".format(str(i)) + '\r')
        # Switch color of prompt to red near less 10 seconds to completion
        if i < 11:
            sys.stdout.write(colored(" The clipboard will be cleared in {} seconds ", 'red').format(str(i)) + '\r')
        if i < 1:
            sys.stdout.write("\033[K")
            print("The clipboard has been cleared")
        sys.stdout.flush()
        time.sleep(1)

    # Copy unprintable data to the clipboard
    pyperclip.copy(''.join([chr(random.randint(1, 31)) for _ in range(0, password_size)]))

    # TODO: create an at job so that we can exit before erasing the clipboard
    # See https://stackoverflow.com/a/10676359/1114256 for how to do this
    # That will enable true silent mode


def copy_to_clipboard(array_of_passwords, password_to_save):

    try:
        # Copy the password to the clipboard
        pyperclip.copy(array_of_passwords[password_to_save])

    except pyperclip.PyperclipException:

        print(colored("\nError", 'red'))
        print("If you're on Linux and seeing this error it probably means that ")
        print("you don't have a clipboard program installed. ")
        print("You can fix this by installing one of the copy/paste mechanisms:\n")
        print("    'sudo apt-get install xsel' to install the xsel utility.")
        print("    'sudo apt-get install xclip' to install the xclip utility.")
        print("    'pip3 install gtk' to install the gtk Python module.")
        print("    'pip3 install PyQt4' to install the PyQt4 Python module.")
        exit()


def silent_mode(array_of_passwds):
    """
    Select a random password from the provided array of passwords,
    copy the selected password to the clipboard and exit.

    :param array_of_passwds:
    :return:
    """

    passwd_to_save = random.choice((range(0, array_of_passwds.__len__()))) 

    copy_to_clipboard(array_of_passwds, passwd_to_save)

    # TODO: create a silent option to skip the countdown and erase

    clipboard_countdown_and_erase()

    exit()


if __name__ == '__main__':

    # Set cli argument defaults.
    # If no options were specified on the command line, set silent mode by default
    if not len(sys.argv) > 1:
        args.silent = True

    # If no -i to ask for interactive mode, then set to silent mode by default
    if not args.interactive:
        args.silent = True

    password_size = int(args.password_length)

    password_array = []

    # Create a list of English words
    the_wordlist, the_wordlist_length = create_english_wordlist()

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

    # TODO: remove sort or add variable length passwords option
    # Sort the passwords by their length, descending
    password_array.sort(key=len, reverse=True)

    if args.silent:
        silent_mode(password_array)

    if args.interactive:
        interactive_mode(password_array)
