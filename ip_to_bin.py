ip_addr = input('This script would convert IP address to binary. Please, write down your IP address. Divide by dots: ')
a,b,c,d = ip_addr.split('.')
a,b,c,d = int(a),int(b),int(c),int(d)

y = 1 # Var for triggering error in range of input

i = 1 # Var counter for exit from loop after fourth octet

z = 'Your IP in bin is equal to ' # Final string to print result of correct converting

# CHECKING RANGE OF OCTETS
if a > 255:
    y = y + 1
else:
    if b > 255:
        y = y + 1
    else:
        if c > 255:
            y = y + 1
        else:
            if d > 255:
                y = y + 1
            else:
                if a < 1:
                    y = y + 2 # Check first octet check in another way
                else:
                    if b < 0:
                        y = y + 1
                    else:
                        if c < 0:
                            y = y + 1
                        else:
                            if d < 0:
                                y = y + 1
                            else:
                                print('Yours octets seemed to be in range 0-255!')
# End of range check

octets = [a,b,c,d] # List for loop

for x in octets:
    if x < 128: # Beggining of check integer to be filled with the whole byte after converting
        x = x + 256
        x = bin(x)
        if i < 4:
            z = z + x[-8:] + '.'
            i = i + 1
        else:
            z = z + x[-8:]
            i = i + 1

    else:
        x = bin(x)
        if i < 4:
            z = z + x[-8:] + '.'
            i = i + 1
        else:
            z = z + x[-8:]
            i = i + 1

if y < 2:
    print(z)
else:
    if y > 2:
        print('You gotta be kidding! FAKE IP! I AM CALLING POLICE!!!')
    else:
        print('Error! Put the Integers in 0-255 range!')