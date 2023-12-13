#!/usr/bin/env python3
# Model epidemii SIR

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

# dS/dt = -bSI
# dI/dt = bSI - gI
# dR/dt = gI


def sir_eqn(y, t, beta, g):
    s, i, r = y
    return [-beta*s*i, beta*s*i - g*i, g*i]


def run_pandemic(y0, beta, g, filename):
    t = np.linspace(0, 10, 101)
    sol = odeint(sir_eqn, y0, t, args=(beta, g))
    plt.clf()
    plt.plot(t, sol[:, 0], 'b', label='S')
    plt.plot(t, sol[:, 1], 'g', label='I')
    plt.plot(t, sol[:, 2], 'r', label='R')
    plt.title(f"SIR: y0={y0}, beta={beta}, g={g}")
    plt.legend()
    plt.savefig(filename)
    

y0 = [95, 5, 0]


try:
    os.mkdir("obr/")
except:
    pass

for g in np.linspace(0, 1, 11):
    run_pandemic(y0, 0.1, g, f"obr/g{g}.png")
