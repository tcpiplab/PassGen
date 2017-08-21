import random, sys, os

passwdSize = None

# Get the terminal dimensions
rows, columns = os.popen('stty size', 'r').read().split()

for row in range(int(rows)-2):
    if len(sys.argv) > 1:
        passwdSize = sys.argv[1]
    else:
        passwdSize = random.randint(9,32)
    # Limit charset to the ascii codes between 33 and 126:
    # !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}
    print "%02d   " % (row,) + ''.join( [chr(random.randint(33,126)) for i in xrange(0,passwdSize)] )
#    print '[' + str(row) + ']  ' + ''.join( [chr(random.randint(33,126)) for i in xrange(0,passwdSize)] )
    row += 1




    # for x in range(33,126):
    #     sys.stdout.write(chr(x))
    #
    #    !"#$%&'()*+,-./
    #    0123456789
    #    :;<=>?@
    #    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    #    [\]^_`
    #    abcdefghijklmnopqrstuvwxyz
    #    {|}
