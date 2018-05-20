import pandas as pd
import numpy as np
from difflib import get_close_matches
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

countries = ['Austria', 'Belgium', 'Czech', 'Estonia', 'Finland', 'France',
             'Germany', 'HongKong', 'Iceland', 'Ireland', 'Italy', 'Korea',
             'Lithuania', 'Netherlands', 'Poland', 'Portugal', 'Spain',
             'Sweden', 'Turkey']

uni = {'D MUNCHEN01': 'LM Munich', 'CZ PRAHA10': 'CTU Prauge', 'Daegu': 'KNU Korea', 'CZ PRAHA07': 'UK Prague', 'I ROMA01': 'SU Rome'}


class Recommender:

    def __init__(self):
        self.df = pd.read_csv('recommender_data/students1.csv')
        self.df['cost'] /= 100
        self.unis = pd.read_csv('recommender_data/universities.csv')
        self.numeric = self.df.select_dtypes(include=['int64', 'float64'])

    def query(self, **kwargs):

        if 'country' in kwargs.keys() and kwargs['country'] not in countries:
            kwargs['country'] = self._corr_country(kwargs['country'])
        # pattern = pd.DataFrame(data=kwargs, index=[0])
        pattern = pd.DataFrame(np.zeros((1, len(self.numeric.columns))), columns=self.numeric.columns)
        pattern.replace(to_replace=0.0, value=-99, inplace=True)
        pattern = pattern.drop(labels='sat', axis=1)
        pattern['cost']/=100
        # pattern.fillna(value=0)
        # print(pattern)
        # print(pattern)
        filtered = self.df.copy()
        filtered = filtered.loc[:, filtered.columns != 'ID']
        filtered = filtered.drop(labels='sat', axis=1)
        # = self.df.loc[self.df['country'] == 'Lithuania', self.df.dtypes != object ]
        # print(self.numeric)
        for key in kwargs.keys():
            val = kwargs[key]
            if filtered[key].dtype == object:
                filtered = filtered.loc[filtered[key] == val, filtered.columns != key]
                # pattern = pattern.loc[:, filtered.columns != key]
            else:
                pattern[key] = val
        filtered = filtered.select_dtypes(include=['int64', 'float64'])
        print(filtered)
        print(pattern)
        x = pd.DataFrame(cosine_similarity(filtered, pattern) *50, columns=['similarity'])

        out = pd.concat([self.df['ID'].copy(), x], axis=1)
        out = out.sort_values(by=['similarity'], ascending=False)
        out = out.head(5)
        # out = out.as_matrix()
        print(out)
        # uni_names = [uni[i] for i in out.loc[:5, 'ID']]
        for i in out.loc[:5, 'ID']:
            print(i)
        # print(uni_names)
        plt.bar(uni[out['ID']], out['similarity'], tick_label=out['ID'])
        plt.show()


    @staticmethod
    def plot_recom(top):
        pass



    @staticmethod
    def _corr_country(country):
        return get_close_matches(country, countries, 1)


if __name__ == '__main__':
    # args = {'field': 'AI', 'duration': 5, 'cost': 600}
    # rs = Recommender()
    # rs.query(**args)
    x = ['LM Munich', 'CTU Prauge', 'KNU Korea', 'UK Prague', 'SU Rome']
    y = [21.4, 18.7, 13.8, 12.7, 9.9]
    plt.figure(1)
    plt.bar(x, y)
    plt.ylabel('Recommendation index')

    plt.figure(2)
    labels = ["U. of Vienna", "CTU Prague", "Paris", "LM Munich", "TU Berlin"]
    values = [29, 16, 4, 2, 2]
    plt.bar(labels, values)
    plt.ylabel("Number of students")
    plt.show()
