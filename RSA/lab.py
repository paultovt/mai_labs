from joblib import Parallel, delayed
import multiprocessing
import sys
from alive_progress import alive_bar
from math import gcd, sqrt
from random import randint

num_jobs = multiprocessing.cpu_count()

def prime(n):
    for i in range(2, int(sqrt(n)) + 1):
        if not n % i:
            return
    return True

def get_primes(x):
    arr = set([])
    core = x // (10 ** n // num_jobs)
    for c in range(x, x + (10 ** n // num_jobs)):
        if len(str(c)) == n:
            if prime(c):
                arr.add(c)
    return sorted(arr)

def modulo_multiplicative_inverse(A, M):
    gcd, x, y = extended_euclid_gcd(A, M)
    if x < 0:
        x += M
    return x

def extended_euclid_gcd(a, b):
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a
    while r != 0:
        quotient = old_r//r 
        old_r, r = r, old_r - quotient*r
        old_s, s = s, old_s - quotient*s
        old_t, t = t, old_t - quotient*t
    return [old_r, old_s, old_t]

def find_pqs(a, b, arr, min_a, max_b):
    if a < max_b - 1:
        core = a // ( (max_b - min_a) // num_jobs) % num_jobs
        for i in range(a, b):
            simple_p = arr[i]
            for simple_q in arr:
                if simple_q > m / simple_p:
                    break
                if simple_p * simple_q == m:
                    return sorted([simple_p, simple_q])

if __name__ == '__main__':
    if sys.argv[1:]:
        action = sys.argv[1]
    else:
        print('\nUsage: python3 lab.py g/e/d/h <file>\n')
        exit()

    # generate keys
    if action == 'g':
        print('\nGenerating keys\n')
        n = 5
        primes = []
        print('Calculating primes')
        with alive_bar(num_jobs) as bar:
            for v in Parallel(n_jobs=num_jobs)(delayed(get_primes)(x) for x in range(10 ** (n - 1), 10 ** n, 10 ** n // num_jobs)):
                bar()
                primes += v 
        #print('\nprimes:', len(primes))
        while True:
            x = randint(10 ** (n - 1), 10 ** n)
            if x in primes:
                p = x
                break
        while True:
            x = randint(10 ** (n - 1), 10 ** n)
            if x in primes and x != p:
                q = x
                break
        #print('p q:', p, q)
        m = p * q
        #print('m:', m)
        fm = (p - 1) * (q - 1)
        #print('fm:', fm)
        for x in range(fm-1, 1, -1):
            if gcd(fm, x) == 1 and prime(x):
                e = x
                d = modulo_multiplicative_inverse(e, fm)
                if e != d:
                    break
        #print('e:', e)
        #print('d:', d)
        outfile = open('rsa.pub', 'wb')
        outfile.write(m.to_bytes(8, byteorder='big', signed=True))
        outfile.write(e.to_bytes(8, byteorder='big', signed=True))
        outfile.close()
        outfile = open('rsa.pri', 'wb')
        outfile.write(m.to_bytes(8, byteorder='big', signed=True))
        outfile.write(d.to_bytes(8, byteorder='big', signed=True))
        outfile.close()
        print('\n   open key:', m, e, '(saved to rsa.pub)')
        print('private key:', m, d, '(saved to rsa.pri)\n')

    # encrypt file
    elif action == 'e':
        infile = open('rsa.pub', 'rb')
        m = int.from_bytes(infile.read(8), byteorder='big')
        e = int.from_bytes(infile.read(8), byteorder='big')
        infile.close()
        filename = sys.argv[2]
        print('\nEncrypting file', filename)
        infile = open(filename, 'r')
        data = infile.read()
        infile.close()
        outfile = open(filename.split('.')[0] + '.enc', 'wb')
        for char in data:
            outfile.write(pow(ord(char), e, m).to_bytes(8, byteorder='big', signed=True))
        outfile.close()
        print('\nEncrypted data saved to', filename.split('.')[0] + '.enc\n')

    # decrypt file
    elif action == 'd':
        infile = open('rsa.pri', 'rb')
        m = int.from_bytes(infile.read(8), byteorder='big')
        d = int.from_bytes(infile.read(8), byteorder='big')
        infile.close()
        filename = sys.argv[2]
        print('\nDecrypting file', filename)
        outfile =  open(filename.split('.')[0] + '.dec', 'w')
        with open(filename, 'rb') as infile:
            while True:
                data = infile.read(8)
                if data == b'':
                    break
                outfile.write(chr(pow(int.from_bytes(data, byteorder='big'), d, m)))
        outfile.close()
        infile.close()
        print('\nDecrypted data saved to', filename.split('.')[0] + '.dec\n')

    # hack file
    elif action == 'h':
        infile = open('rsa.pub', 'rb')
        m = int.from_bytes(infile.read(8), byteorder='big')
        e = int.from_bytes(infile.read(8), byteorder='big')
        infile.close()
        filename = sys.argv[2]
        print('\nHacking the file', filename, 'using open key in file rsa.pub\n')
        n = len(str(m)) // 2
        primes = []
        print('Calculating primes')
        with alive_bar(num_jobs * 2) as bar:
            for v in Parallel(n_jobs=num_jobs)(delayed(get_primes)(x) for x in range(10 ** (n - 1), 10 ** n, 10 ** n // num_jobs)):
                primes += v 
                bar()
            n += 1
            for v in Parallel(n_jobs=num_jobs)(delayed(get_primes)(x) for x in range(10 ** (n - 1), 10 ** n, 10 ** n // num_jobs)):
                primes += v 
                bar()
        #print('\nprimes:', len(primes))
        arr = []
        for c in range(0, len(primes), len(primes) // num_jobs // num_jobs):
            arr.append([c, c + len(primes) // num_jobs // num_jobs])
        print('\nCalculating p and q')
        with alive_bar(len(arr)) as bar:
            c = len(arr)
            for each in arr:
                bar()
                c -= 1
                a, b = each
                pqs = Parallel(n_jobs=num_jobs)(delayed(find_pqs)(c, c + ((b - a) // num_jobs), primes, a, b) for c in range(a, b, (b - a) // num_jobs))
                if list(filter(None, pqs)):
                    pqs = list(filter(None, pqs))[0]
                    break
            while c:
                bar()
                c -= 1
        if pqs:
            p, q = pqs
            #print('p q:', p, q)
            fm = (p - 1) * (q - 1)
            #print('fm:', fm)
            d = modulo_multiplicative_inverse(e, fm)
            #print('d:', d)
            outfile =  open(filename.split('.')[0] + '.hacked', 'w')
            with open(filename, 'rb') as infile:
                while True:
                    data = infile.read(8)
                    if data == b'':
                        break
                    outfile.write(chr(pow(int.from_bytes(data, byteorder='big'), d, m)))
            outfile.close()
            infile.close()
            print('\nHacked data saved to', filename.split('.')[0] + '.hacked\n')
        else:
            print('\nHacking failed :(')

    else:
        print('\nUsage: python3 lab.py g/e/d/h <file>\n')
        exit()
