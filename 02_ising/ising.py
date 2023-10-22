#!/usr/bin/env python3

import argparse
import numpy as np




N = 10
J = 0.5
beta = 1
B = 1

nsteps = 10

spindens = 0.5


material = np.zeros((N, N))

"""
Algorytm monte carlo symulacji modelu isinga
XXX: Czy to nie jest alg metropolisa?
1. Losujemy komórke w materiale
2. odwaracamy spin
3. Jeśli odwrócenie spinu zmniejsza energię, akceptujemy je
4. W przeciwnym wypadku ackeptujemy je z prawdopodobieństwem 
   P(dE) = exp(-beta*dE)

Energia komórki jest liczona na podstawie najbliższych czterech sąsiadów:

H = -J sum({i,j}, s_i*s_j) - B sum({i} s_i)

Gdzie j to zmieniana komórka a indeksy i to jej czterej sąsiedzi
"""


for i in range nsteps:
    for i in range(N**2):
        



