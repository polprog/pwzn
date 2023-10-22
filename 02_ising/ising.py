#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
import time
import os

def ham(material, i, j, v):
    """Return the hamiltionian of a cell
    given it's new value and neighbourhood"""
    
    H = 0
    # nearest 4 neighbours
    # XXX: handle material edge
    sh = material.shape
    if i < 1 or j < 1 or i > sh[0] -1 or j > sh[0] -1:
        return 0
    H = H + material[i-1, j  ] * v
    H = H + material[i  , j-1] * v
    H = H + material[i+1  , j] * v
    H = H + material[i  , j+1] * v

    # Jeśli hamiltionian jest bez minusa,
    # to domeny magnetyczne powstają "w kratkę" ;)
    return -H

def fill_material(material, N, spindens=0.5):
    for i in range(N):
        for j in range(N):
            if np.random.random() > spindens:
                material[i, j] = 1
            else:
                material[i, j] = -1
    return material

N = 100
J = 0.5
beta = 1
B = 1
nsteps = 100
spindens = 0.5


output_dir = f"images_{int(time.time())}/"
os.mkdir(output_dir)
print(f"Output dir is {output_dir}")

material = fill_material(np.zeros((N, N)), N)

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
prob = lambda dE: np.exp(-beta * dE)

for k in range(nsteps):
    plt.imshow(material)
    #plt.show()
    plt.savefig(output_dir + f"iter{k:04d}.png")

    for l in range(N**2):
        # XXX: Handle edges
        i = np.random.randint(1, N-1)
        j = np.random.randint(1, N-1)
        ham0 = ham(material, i, j, material[i, j])
        ham1 = ham(material, i, j, -material[i, j])
        #print(f"{i}, {j}: ham0 = {ham0}, ham1 = {ham1} ", end="")
        if ham1 < ham0:
            material[i, j] = -material[i, j]
            #print("swap (ham0 < ham1)", end="")
        elif prob(ham1-ham0) > np.random.random():
            material[i, j] = -material[i, j]
            #print("swap (probability)", end="")
        #print()
    print(f"Iteration {k} done.")
    
