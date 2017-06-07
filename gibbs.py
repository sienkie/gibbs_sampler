#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random
import sys


# TODO V=10 N=20

def inicjalizacja(V=2, N=3, X=2, R_MAX=500, gamma_pi=[1,1]):
    # R_MAX: maksymalna liczba słów w dokumencie
    # X: liczba labels

    gamma_theta = np.ones(V)

    R = [random.randint(1, R_MAX) for i in range(N)]
    # wszystkie słowa

    W = []
    for Rj in R:
        Wj = []
        for i in range(V - 1):
            Wj.append(random.randint(0, Rj - sum(Wj)))
        Wj.append(Rj - sum(Wj))
        W.append(Wj)
    print('Words in docs', W)

    L = [random.randint(0, X - 1) for i in range(N)]
    print('Labels', L)

    thetas = []
    Nc = []
    C = []
    for x in range(X):
        Cx = (np.nonzero(np.array(L) == x))[0].tolist()
        thetas.append(np.zeros(V).tolist())
        for c in Cx:
            for w in range(V):
                thetas[x][w] += W[c][w]
        s = sum(thetas[x])
        Nc.append(thetas[x])
        thetas[x] = [w / s if s != 0 else 0 for w in thetas[x]]
        C.append(Cx)
    print('Thetas', thetas)
    print('Word counts of labels', Nc)

    return W, L, thetas, Nc, C, gamma_theta


# TODO T=100
def gibbs(T=10, burn_in=5, V=5, N=3, X=2, R_MAX=500, gamma_pi=[1,1]):
    W, L, thetas, Nc, C, gamma_theta = inicjalizacja(V, N, X, R_MAX, gamma_pi)
    stats_thetas = []
    stats_ls = []
    for t in range(T):
        for j in range(N):  # po dokumentach
            label = L[j]
            Nc[label] = [Nc[label][i] - W[j][i] for i in range(len(Nc[label]))]
            # TODO ew zmienic
            L[j] = -1

            values = []
            for x in range(X):
                czynnik = (len(C[x]) + gamma_pi[0] - 1) / float(N + sum(gamma_pi) - 1)
                for v in range(V):
                    czynnik *= (thetas[x][v] ** W[j][v])
                values.append(czynnik)

            distribution = [val / float(sum(values)) for val in values]

            L[j] = np.random.binomial(1, distribution[0], 1)[0]
            Nc[L[j]] = [Nc[L[j]][i] + W[j][i] for i in range(len(Nc[L[j]]))]


        for x in range(X):
            tx=[]
            for v in range(V):
                tx.append(Nc[x][v] + gamma_theta[v])
            thetas[x] = np.random.dirichlet(tx, 1)[0].tolist()

        if (t > burn_in):
            stats_thetas.append(thetas)
            stats_ls.append(L)
            print('For t= ', t, thetas)
            print(' L: ', L)

if __name__ == '__main__':
    gibbs()
