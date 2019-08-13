import random, sys, os, pyperclip, time

passwdSize = None
passwdArray = []

# Get the terminal dimensions
rows, columns = os.popen('stty size', 'r').read().split()

for row in range(int(rows)-2):
    if len(sys.argv) > 1:
        passwdSize = sys.argv[1]
    else:
        passwdSize = random.randint(9,32)

    # Limit charset to the ascii codes between 33 and 126:
    # !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}
    passwdString = ''.join( [chr(random.randint(33,126)) for i in xrange(0,int(passwdSize))] )

    numbers = chr(random.randint(48,57))
    lowers = chr(random.randint(97,122))
    uppers = chr(random.randint(65,90))
    symbols1 = chr(random.randint(33,47))


    # Add the passsword to the array
    passwdArray.append(passwdString)
    row += 1

# Sort the passwords by their length, descending
passwdArray.sort(key=len, reverse=True)

# Print each password with its index number
for i in range(len(passwdArray)):
    print "%02d   " % (i,) + passwdArray[i]

# Ask the useer which password to save
passwdToSave = input('Enter the number of the password you want sent to the clipboard: ')

# Copy the password to the clipboard
pyperclip.copy(passwdArray[passwdToSave])

# Erase the clipboard after 30 seconds
time.sleep(30)

# Copy unprintable data to the clipboard
pyperclip.copy(''.join( [chr(random.randint(1,31)) for i in xrange(0,len(passwdArray[-1]))] ))
