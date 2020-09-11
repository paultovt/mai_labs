import sys
import numpy
import math
from tabulate import tabulate
import pandas

epochs = 5
learn = 0.3
speed = 0.05
in_c = 6
out_c = 3

if __name__ == '__main__':
    if sys.argv[1:]:
        fn = sys.argv[1]
    else:
        print('\nUsage: python3 lab.py <file>\n')
        exit()

    types = pandas.read_csv(fn, delimiter = ';', usecols = [0])
    dataset = numpy.loadtxt(fn, delimiter = ';', skiprows = 1, usecols = (1,2,3,4,5,6))
    weights = numpy.random.random((out_c, in_c)) * 0.1
    classes = {}
    while learn > 0:
        for k in range(epochs):
            for c, data in enumerate(dataset):
                norm_data = 1 / (dataset.max() - dataset.min()) * data - (dataset.min() / (dataset.max() - dataset.min()))
                dists = [] 
                for weight in weights:
                    dists.append(math.sqrt(sum( (d - w)**2 for d, w in zip(norm_data, weight))))
                weights[dists.index(min(dists))] += learn * (norm_data - weights[dists.index(min(dists))])
                classes[c] = dists.index(min(dists))

        learn -= speed

    for i in range(out_c):
        print('\n\033[1m\033[92mКЛАСС', i + 1, '\033[0m')
        out = []
        for c in classes:
            if classes[c] == i:
                tmp = dataset[c].tolist()
                tmp.reverse()
                tmp.append(types['Тип'][c])
                tmp.reverse()
                out.append(tmp)
        print(tabulate(out, headers = ['Тип', 'Число двигателей', 'Тяга, кН', 'Число пассажиров', 'Дальность, км', 'Крейсерская скорость, км/ч', 'Максимальный вес, т']))

