#-*- coding: utf-8 -*-
'''
Created on 201７-4-17

@author: Zhao Pengya
'''
import sys, random, math
from operator import itemgetter
from ..models import Rating
from math import sqrt

random.seed(0)


class UserBasedCF():
    ''' TopN recommendation - UserBasedCF '''
    def __init__(self):
        self.trainset = {}
        self.testset = {}

        self.n_sim_user = 20
        self.n_rec_movie = 10

        self.user_sim_mat = {}
        self.movie_popular = {}
        self.movie_count = 0

        # print('Similar user number = %d' % self.n_sim_user, file=sys.stderr)
        # print('recommended movie number = %d' % self.n_rec_movie, file=sys.stderr)


    @staticmethod
    def loadBase():
        ''' load file from dataBase, return a generator. '''
        ratings = Rating.query.all()
        for i,rating in enumerate(ratings):
            yield str(rating.user_id)+"::"+str(rating.movie_id)+"::"+str(rating.rating)
            if i%100000 == 0:
                print('loading (%s)' % i, file=sys.stderr)
        print('load database succ', file=sys.stderr)


    def generate_dataset(self, pivot=0.3):
        ''' load rating data and split it to training set and test set '''
        trainset_len = 0
        # testset_len = 0

        for line in self.loadBase():
            user, movie, rating = line.split('::')
            # split the data by pivot
            self.trainset.setdefault(user, {})
            self.trainset[user][movie] = float(rating)
            trainset_len += 1

            # if (random.random() < pivot):
            #     self.trainset.setdefault(user,{})
            #     self.trainset[user][movie] = float(rating)
            #     trainset_len += 1
            # else:
            #     self.testset.setdefault(user,{})
            #     self.testset[user][movie] = float(rating)
            #     testset_len += 1

        print('load set is suc!', file=sys.stderr)
        print('train set = %s' % trainset_len, file=sys.stderr)
        # print('test set = %s' % testset_len, file=sys.stderr)


    def calc_user_sim(self):

        usersim_mat = self.user_sim_mat

        for u in self.trainset.keys():
            for v in self.trainset.keys():
                if u == v: continue
                else:
                    usersim_mat.setdefault(u, {})
                    usersim_mat[u].setdefault(v, 0)
                    usersim_mat[u][v] = self.sim_pearson(u, v)

    def sim_pearson(self, u, v):

        # Get the list of mutually rated items
        common_rated = {}
        for movie in self.trainset[u]:
            if movie in self.trainset[v]:
                common_rated[movie] = 1

        # if they are no ratings in common, return 0
        if len(common_rated) == 0:
            return 0

        # Sum calculations
        n = len(common_rated)

        # Sums of all the preferences
        sum1 = sum([self.trainset[u][movie] for movie in common_rated])
        sum2 = sum([self.trainset[v][movie] for movie in common_rated])

        # Sums of the squares
        sum1Sq = sum([pow(self.trainset[u][movie], 2) for movie in common_rated])
        sum2Sq = sum([pow(self.trainset[v][movie], 2) for movie in common_rated])

        # Sum of the products
        pSum = sum([self.trainset[u][movie] * self.trainset[v][movie] for movie in common_rated])

        # Calculate r (Pearson score)
        num = pSum - (sum1 * sum2 / n)
        den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
        if den == 0:
            return 0
        r = num / den
        return r

    def recommend(self, user):
        ''' Find K similar users and recommend N movies. '''
        K = self.n_sim_user
        N = self.n_rec_movie
        rank = dict()
        if user not in self.trainset.keys():
            return None
        else:
            watched_movies = self.trainset[user]
            # v=similar user, wuv=similarity factor
            for v, wuv in sorted(list(self.user_sim_mat[user].items()),
                    key=itemgetter(1), reverse=True)[0:K]:
                for movie, rating in self.trainset[v].items():
                    if movie in watched_movies:
                        continue
                    # predict the user's "interest" for each movie
                    rank.setdefault(movie,0)
                    rank[movie] += wuv * rating
            # return the N best movies
            # print(sorted(list(rank.items()), key=itemgetter(1), reverse=True)[0:N])
            return sorted(list(rank.items()), key=itemgetter(1), reverse=True)[0:N]

    def evaluate(self):
        ''' return precision, recall, coverage and popularity '''
        print('Evaluation start...', file=sys.stderr)

        N = self.n_rec_movie
        #  varables for precision and recall 
        hit = 0
        rec_count = 0
        test_count = 0
        # varables for coverage
        all_rec_movies = set()
        # varables for popularity
        popular_sum = 0

        for i, user in enumerate(self.trainset):
            if i % 500 == 0:
                print('recommended for $d users' % i, file=sys.stderr)
            test_movies = self.testset.get(user, {})
            rec_movies = self.recommend(user)
            for movie, w in rec_movies:
                if movie in test_movies:
                    hit += 1
                all_rec_movies.add(movie)
                popular_sum += math.log(1 + self.movie_popular[movie])
            rec_count += N
            test_count += len(test_movies)

        precision = hit / (1.0*rec_count)
        recall = hit / (1.0*test_count)
        coverage = len(all_rec_movies) / (1.0*self.movie_count)
        popularity = popular_sum / (1.0*rec_count)

        print('precision=%.4f\trecall=%.4f\tcoverage=%.4f\tpopularity=%.4f' % \
                (precision, recall, coverage, popularity), file=sys.stderr)


usercf = UserBasedCF()
# usercf.generate_dataset()
# usercf.calc_user_sim()
# usercf.evaluate()
