import sys
import readchar

key = 5

if __name__ == '__main__':
    if sys.argv[2:]:
        action = sys.argv[1]
        filename = sys.argv[2]
    else:
        print('\nUsage: python3 lab.py e/d/h <file>\n')
        exit()

    # ecnrypt file
    if action == 'e':
        infile = open(filename, 'r')
        data = infile.read()
        infile.close()
        outfile = open(filename.split('.')[0] + '.enc', 'wb')
        for char in data:
            outfile.write((ord(char) + key).to_bytes(4, byteorder='big', signed=True))
        outfile.close()
        print('\nEncrypted data saved to', filename.split('.')[0] + '.enc\n')

    # decrypt file
    elif action == 'd':
        outfile =  open(filename.split('.')[0] + '.dec', 'w')
        with open(filename, 'rb') as infile:
            while True:
                data = infile.read(4)
                if data == b'':
                    break
                outfile.write(chr(int.from_bytes(data, byteorder='big') - key))
        outfile.close()
        infile.close()
        print('\nDecrypted data saved to', filename.split('.')[0] + '.dec\n')

    # hack file
    elif action == 'h':
        infile = open(filename, 'rb')
        data = infile.read()
        infile.close()
        print('\nHacking the file', filename)
        i = 1
        k = ''
        while k != 'y':
            if k == 'q':
                exit()
            decrypted_str = ''
            with open(filename, 'rb') as infile:
                while True:
                    data = infile.read(4)
                    if data == b'':
                        break
                    decrypted_str += chr(int.from_bytes(data, byteorder='big') - i)
            infile.close()
            print('\n\nkey = ' + str(i) + '\n-------------')
            i += 1
            print(decrypted_str[:100])
            print('-------------')
            print('Is this text readable? (y/n/q)')
            k = readchar.readchar()
        outfile = open(filename.split('.')[0] + '.hacked', 'w')
        outfile.write(decrypted_str)
        outfile.close()
        print('\nHacked data saved to', filename.split('.')[0] + '.hacked\n')

    else:
        print('\nUsage: python3 lab.py e/d/h <file>\n')
        exit()
