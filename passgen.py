#!/usr/bin/env python3
import os
import pyperclip
import random
import sys
import time

if __name__ == '__main__':
    password_size = None
    password_array = []

    # Get the terminal dimensions
    rows, columns = os.popen('stty size', 'r').read().split()

    for row in range(int(rows)-2):
        if len(sys.argv) > 1:
            password_size = sys.argv[1]
        else:
            password_size = random.randint(9, 32)

        # Limit charset to the ascii codes between 33 and 126:
        # !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}
        password_string = ''.join([chr(random.randint(33, 126)) for i in range(0, int(password_size))])

        numbers = chr(random.randint(48,57))
        lowers = chr(random.randint(97,122))
        uppers = chr(random.randint(65,90))
        symbols1 = chr(random.randint(33,47))

        # Add the password to the array
        password_array.append(password_string)
        row += 1

    # Sort the passwords by their length, descending
    password_array.sort(key=len, reverse=True)

    # Print each password with its index number
    for i in range(len(password_array)):
        print("%02d   " % (i,) + password_array[i])

    # Ask the user which password to save
    passwdToSave = int(input('Enter the number of the password you want sent to the clipboard: '))

    # Copy the password to the clipboard
    pyperclip.copy(password_array[passwdToSave])

    # Erase the clipboard after 30 seconds
    time.sleep(30)

    # Copy unprintable data to the clipboard
    pyperclip.copy(''.join([chr(random.randint(1,31)) for i in range(0, len(password_array[-1]))]))
