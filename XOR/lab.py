import sys
import operator
from math import floor

key = 'Alexandre Dumas'

if __name__ == '__main__':
    if sys.argv[2:]:
        action = sys.argv[1]
        filename = sys.argv[2]
    else:
        print('\nUsage: python3 lab.py e/d <file>\n')
        exit()

    # encrypt file
    if action == 'e':
        outfile = open(filename.split('.')[0] + '.enc', 'wb')
        with open(filename, 'r') as infile:
            c = 0
            while True:
                if c >= len(key):
                    c = 0
                data = infile.read(1)
                if data == '':
                    break
                bin_chars = bin(ord(data))[2:].zfill(16)
                bin_keychars = bin(ord(key[c]))[2:].zfill(16)
                enc_bin = ''
                for ch, kch in zip(bin_chars, bin_keychars):
                    xor = operator.xor(int(ch), int(kch))
                    enc_bin += str(xor)
                outfile.write((int(enc_bin,2)).to_bytes(4, byteorder='big', signed=True))
                c += 1
        outfile.close()
        infile.close()
        print('\nEncrypted data saved to', filename.split('.')[0] + '.enc\n')

    # decrypt file
    elif action == 'd':
        outfile =  open(filename.split('.')[0] + '.dec', 'w')
        with open(filename, 'rb') as infile:
            c = 0
            while True:
                if c >= len(key):
                    c = 0
                data = infile.read(4)
                if data == b'':
                    break
                bin_chars = bin(int.from_bytes(data, byteorder='big'))[2:].zfill(16)
                bin_keychars = bin(ord(key[c]))[2:].zfill(16)
                dec_bin = ''
                for ch, kch in zip(bin_chars, bin_keychars):
                    xor = operator.xor(int(ch), int(kch))
                    dec_bin += str(xor)
                dec_char = chr(int(dec_bin,2))
                outfile.write(dec_char)
                c += 1
        outfile.close()
        infile.close()
        print('\nDecrypted data saved to', filename.split('.')[0] + '.dec\n')

    else:
        print('\nUsage: python3 lab.py e/d <file>\n')
        exit()
