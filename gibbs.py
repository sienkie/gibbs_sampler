#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random

# TODO V=10 N=20

def inicjalizacja(V=2,N=3,X=2,R_MAX=500,gamma_pi_1=1, gamma_pi_0=1):

    #R_MAX: maksymalna liczba słów w dokumencie
    #X: liczba labels

    gamma_theta = np.ones(V)

    R = [random.randint(1,R_MAX) for i in range(N)]
    # wszystkie słowa

    W = []
    for Rj in R:
        Wj = []
        for i in range(V-1):
            Wj.append(random.randint(0,Rj-sum(Wj)))
        Wj.append(Rj - sum(Wj))
        W.append(Wj)
    print('Words in docs', W)

    L=[random.randint(0,X-1) for i in range(N)]
    print('Labels',L)

    thetas = []
    Nc = []
    for x in range(X):
        Cx = (np.nonzero(np.array(L)==x))[0].tolist()
        thetas.append(np.zeros(V).tolist())
        for c in Cx:
            for w in range(V):
                thetas[x][w] += W[c][w]
        s = sum(thetas[x])
        Nc.append(thetas[x])
        thetas[x] = [w/s if s!= 0 else 0 for w in thetas[x]]
    print('Thetas', thetas)
    print('Word counts of labels', Nc)

    return W, L, thetas, Nc

# TODO T=100
def gibbs(T=1,burn_in=5,V=2,N=3,X=2,R_MAX=500,gamma_pi_1=1, gamma_pi_0=1):

    W,L,thetas,Nc = inicjalizacja(V=2,N=3,X=2,R_MAX=500,gamma_pi_1=1, gamma_pi_0=1)
    for t in range(T):
        for j in range(N): # po dokumentach
            label = L[j]
            Nc[label] = [Nc[label][i] - W[j][i] for i in range(len(Nc[label]))]
            print(Nc[label])
if __name__ == '__main__':
    gibbs()
