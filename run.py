# encoding:utf-8
import csv
import math
import numpy as np


def read_excel(l, d, ds, dt):
    csv_file = csv.reader(open('label.csv', 'r'))
    for i in csv_file:
        l.append(i)
    csv_file = csv.reader(open('data.csv', 'r'))
    for i in csv_file:
        d.append(i)
    temp = 0
    new = []
    for i in d:
        if int(i[0]) != temp:
            if temp != 0:
                ds.append(new)
            new = [0] * 61067
            temp += 1
        new[int(i[1]) - 1] = int(i[2])
    ds.append(new)
    npds = np.array(ds, np.int64)
    sqrl = []
    for i in range(0, 1000):
        sqrl.append(np.sum(np.square(npds[i])))
    for i in range(0, 1000):
        ll = []
        for j in range(0, 1000):
            if j < i:
                ll.append(dt[j][i])
            elif j == i:
                ll.append(1)
            else:
                ll.append(cos_sim(npds[i], npds[j], sqrl, i, j))
        dt.append(ll)
        print(str(i)+' is calculated')
    return npds


def cos_sim(a, b, sqrl, i, j):
    xy = np.sum(np.multiply(a, b))
    return xy/math.sqrt(sqrl[i]*sqrl[j])


def brute_force(l, d, ds, dt):
    num = 0
    for i in range(0, 1000):  # for each article
        max = -1
        index = -1
        for j in range(0, 1000):  # for every other article
            if i != j:
                temp = dt[i][j]
                if temp > max:
                    max = temp
                    index = j
        if l[index] != l[i]:
            print("Wrong prediction at " + str(i))
            print(max)
            print(index)

        else:
            print("Good prediction at " + str(i))
            num += 1
    print("number of good prediction is: " + str(num))


def gene_unit_v():
    s = np.random.normal(0, 1, 61067)
    s = s/math.sqrt(np.sum(np.square(s)))
    return s


def myhash(ds, uv):
    l = []
    for i in range(0, len(uv)):
        temp = np.sum(np.multiply(ds, uv[i]))
        if temp >= 0:
            l.append(1)
        else:
            l.append(-1)
    return l


def lsh_algorithm(l, d, ds, dt, L, K):
    unit_vector = []
    for i in range(0, L):
        uv = []
        for j in range(0, K):
            uv.append(gene_unit_v())
        unit_vector.append(uv)
    num = 0
    pavg = 0
    all_hash_table = []  # storing all hash values for every data
    for i in range(0, L):
        hash_table = []
        for j in range(0, 1000):  # calculate hash_table
            my_slot = myhash(ds[j], unit_vector[i])  # (1, -1, 1, ...) k dimensions
            hash_table.append(my_slot)
        all_hash_table.append(hash_table)
    for i in range(0, 1000):  # for each article
        plist = []
        max = -1
        index = -1
        for j in range(0, L):
            my_slot = all_hash_table[j][i]
            for k in range(0, 1000):  # for each other article
                if k != i:
                    this_slot = all_hash_table[j][k]
                    if this_slot == my_slot:
                        plist.append(k)
        plist = list(set(plist))
        pavg += int(len(plist))
        for j in plist:
            temp = dt[i][j]
            if temp > max:
                max = temp
                index = j
        if index == -1:
            print("miss")
        else:
            if l[index] != l[i]:
                print("Wrong lsh_prediction at " + str(i))
            else:
                print("Good lsh_prediction at " + str(i))
                num += 1
    print("number of good lsh_prediction: " + str(num))
    print("average lsh_prediction number: " + str(pavg/1000))


if __name__ == '__main__':
    label = []  # label is 1x1000 array storing article class
    data = []  # data is 3*129532 array storing (article,word,freq)
    data_set = []  # data_set is 61067*1000
    data_table = []  # similarity calculated in table
    np_ds = read_excel(label, data, data_set, data_table)
    brute_force(label, data, data_set, data_table)
    lsh_algorithm(label, data, np_ds, data_table, 16, 8)


