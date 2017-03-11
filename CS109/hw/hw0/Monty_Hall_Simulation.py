#!/Users/dimon//anaconda2/bin/python
# -*- coding: utf-8 -*-

#Monty Hall problem

import matplotlib.pyplot as plt
import numpy as np

#generate a random array of 0s, 1s, 2s
def simulate_prizedoor(nsim):
	return np.random.randint(0, 3, nsim)

#simluate the contestant's guesses,  so I choose the first door(0) 
def simulate_guess(nsim):
	return np.zeros(nsim, dtype = np.int)

#simulate the opening of "goat door" that does not contain the prize
#模拟主持人的行为，选取“羊门”

def goat_door(prizedoors, guesses):
	result = np.random.randint(0, 3, prizedoors.size)
	while True:
		bad = (result == prizedoors) | (result == guesses)
		if not bad.any():
			return result
		result[bad] = np.random.randint(0, 3, bad.sum())

def switch_guess(guesses, goatdoors):
    result = np.random.randint(0, 3, guesses.size)
    while True:
        bad = (result == guesses) | (result == goatdoors)
        if not bad.any():
            return result
        result[bad] = np.random.randint(0, 3, bad.sum())

def win_percentage(prizedoors, guesses):
	return 100 * (prizedoors == guesses).mean()

nsim = 100000

print "Win percentage when keeping original door"
print win_percentage(simulate_prizedoor(nsim), simulate_guess(nsim))

pd = simulate_prizedoor(nsim)
guess = simulate_guess(nsim)
goats = goat_door(pd, guess)
guess = switch_guess(guess, goats)

print "Win percentage when switching doors"
print win_percentage(pd, guess).mean()


