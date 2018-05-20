import numpy as np
import pandas as pd
from random import choice

fields = ['AI', 'MP', 'CG', 'IS', 'NW', 'HW', 'Sec', 'Alg', 'Bio', 'Math']
avgcost = {'Austria': 800, 'Belgium': 400, 'Czech': 400 , 'Estonia': 400,
           'Finland': 800, 'France': 600, 'Germany': 850, 'HongKong': 1200,
           'Iceland': 1500, 'Ireland': 1000, 'Italy': 800, 'Korea': 900,
           'Lithuania': 300, 'Netherlands': 900, 'Poland': 400, 'Portugal': 650,
           'Spain': 800, 'Sweden': 850, 'Turkey': 450}

n_students = 500

class Uni:
    def __init__(self, ID, country, no_students, maxlen, bc, msc, phd, fields):
        self.ID = ID
        self.country = country
        self.no_students = int(no_students)
        self.maxlen = int(maxlen)
        self.bc = int(bc)
        self.msc = int(msc)
        self.phd = int(phd)
        self.fields = fields

    def toArray(self):
        return [self.ID, self.country, self.no_students, self.maxlen, self.bc, self.msc, self.phd]

    def toDict(self):
        return {'ID': self.ID,
                'country': self.country,
                'no_students': self.no_students,
                'maxlen': self.maxlen,
                'bc': self.bc,
                'msc': self.msc,
                'phd': self.phd}

if __name__ == '__main__':
    with open('fakultete.txt', 'r') as f:
        lines = f.readlines()

    # generate list of universities
    unis = []
    for i in range(0, len(lines), 8):
        flds = np.random.rand(len(fields))
        flds = flds > 0.7
        unis.append(Uni(*(line.rstrip().split(':')[1] for line in lines[i+1:i+8]), fields=flds))
    pd.DataFrame.from_records([u.toDict() for u in unis]).to_csv('recommender_data/universities.csv')

    student_uni = np.random.randint(0, len(unis), size=n_students)
    costdev = np.random.rand(n_students) * 2 - 0.5
    randsat = np.random.rand(n_students, 4)
    randsat_rowsum = randsat.sum(axis=1)
    randsat = np.divide(randsat, randsat_rowsum[:, np.newaxis])
    grades = np.random.randint(5, 10, n_students)
    difficulty = np.random.randint(5, 10, n_students)
    ects = np.random.randint(15, 30, n_students)
    duration = np.random.randint(4, 12, n_students)
    accomodation = np.random.randint(0, 3, n_students)  # 0=cheap dorm, 1=pricey dorm, 2=cheap flat, 3=pricey flat
    compl = np.random.rand(n_students) < 0.1
    totalsat = 0
    with open('recommender_data/students1.csv', 'w') as f:
        header = 'ID,country,cost,accommodation,duration,field,ects,grades,difficulty,sat\n'
        f.write(header)
        for i in range(n_students):
            uni = unis[student_uni[i]]
            country = uni.country
            cost = avgcost[country] + costdev[i] * 0.1 * avgcost[country]
            fidx = choice(fields)
            field = [x == fidx for x in fields]
            duration[i] = min(duration[i], uni.maxlen)
            # values that affect satisfaction
            field_equal = np.any(np.logical_and(np.array(field), np.array(uni.fields)))
            balance = avgcost[country] - cost
            sat = 5 + \
                  balance * randsat[i, 0] * 0.01 + \
                  field_equal * randsat[i, 1] + \
                  randsat[i, 2] * (grades[i] - difficulty[i]) + \
                  randsat[i, 3] - \
                  compl[i]
            totalsat += sat
            # fieldstr = ','.join([str(int(x is True)) for x in field])
            # s = '{},{},{},{},{},{},{}\n'.format(
            #     uni.ID, uni.country, cost, fieldstr, ects[i], grades[i], sat)
            s = '{},{},{},{},{},{},{},{},{},{}\n'.format(
                uni.ID, uni.country, cost, accomodation[i], duration[i], fidx,
                ects[i], grades[i], difficulty[i], sat)
            f.write(s)
