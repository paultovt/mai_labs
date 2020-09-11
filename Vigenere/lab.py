import sys
from math import gcd, floor

key = 'Alexandre Dumas'

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)

if __name__ == '__main__':
    if sys.argv[2:]:
        action = sys.argv[1]
        filename = sys.argv[2]
    else:
        print('\nUsage: python3 lab.py e/d/h <file>\n')
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
                outfile.write((ord(data) + ord(key[c])).to_bytes(4, byteorder='big', signed=True))
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
                outfile.write(chr(int.from_bytes(data, byteorder='big') - ord(key[c])))
                c += 1
        outfile.close()
        infile.close()

        print('\nDecrypted data saved to', filename.split('.')[0] + '.dec\n')

    # hack file
    elif action == 'h':
        data_str = ''
        with open(filename, 'rb') as infile:
            while True:
                data = infile.read(4)
                if data == b'':
                    break
                data_str += chr(int.from_bytes(data, byteorder='big'))
        infile.close()
        arr = []
        for c in range(10, 0, -1):
            for i in range(0, len(data_str), c):
                positions = list(find_all(data_str, data_str[i:i+c]))
                if len(positions) > 2 and positions not in arr:
                    arr.append(positions)
            if arr:
                break
        
        nods = []
        for each in arr:
            nums = []
            for i, c in enumerate(each):
                if i > 0:
                    nums.append(each[i] - each[i-1])
            for n, num in enumerate(nums):
                if n > 0:
                    nod = gcd(nums[n],nums[n-1])
                    if nod > 1 and nod not in nods:
                        nods.append(nod)
        while len(nods) > 1:
            nods.append(gcd(nods.pop(-1),nods.pop(-1)))

        print('\nThe most probable key length =', str(nods[0]), '\n')

    else:
        print('\nUsage: python3 lab.py e/d/h <file>\n')
        exit()
