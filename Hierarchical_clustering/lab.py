import sys
import numpy
import math
from tabulate import tabulate
import pandas

def mid_vector(x):
    result = numpy.zeros((len(x)))
    for i in x:
        result += dataset[i]
    return result / len(x)


if __name__ == '__main__':
    if sys.argv[1:]:
        fn = sys.argv[1]
        num = int(sys.argv[2])
    else:
        print('\nUsage: python3 lab.py <file> <number of classes>\n')
        exit()

    types = pandas.read_csv(fn, delimiter = ';', usecols = [0])
    dataset = numpy.loadtxt(fn, delimiter = ';', skiprows = 1, usecols = (1,2,3,4,5,6))
    dists = numpy.zeros((len(dataset), len(dataset)))
    for i in range(len(dataset)):
        for j in range(len(dataset)):
            dists[i][j] = math.sqrt(sum( (i - j)**2 for i, j in zip(dataset[i], dataset[j])))
    max_d = dists.max() * 2
    for i in range(len(dists)):
        dists[i][i] = max_d

    classes = {}
    for n in range(len(dataset)):
        classes[n] = n
    class_num = -1
    total_classes = [x for x in range(len(dataset))]
    while len(total_classes) > num:
        ii, jj = numpy.where(dists == dists.min())
        for i, j in zip(ii, jj):
            tmp = classes[j]
            for n in classes:
                if classes[n] == tmp:
                    classes[n] = classes[i]

            dists[i][j] = max_d

        total_classes = set()
        for n in classes:
            total_classes.add(classes[n])

    class_num = 1
    for i in range(len(dataset)):
        out = []
        for c in classes:
            if classes[c] == i:
                tmp = dataset[c].tolist()
                tmp.reverse()
                tmp.append(types['Тип'][c])
                tmp.reverse()
                out.append(tmp)
        if len(out) > 0:
            print('\n\033[1m\033[92mКЛАСС', class_num, '\033[0m')
            print(tabulate(out, headers = ['Тип', 'Число двигателей', 'Тяга, кН', 'Число пассажиров', 'Дальность, км', 'Крейсерская скорость, км/ч', 'Максимальный вес, т']))
            class_num += 1
    
