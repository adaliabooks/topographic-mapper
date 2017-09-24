import math
import random

def noise(freq, size):
	phase = random.uniform(0, 2*math.pi)
	return [math.sin(2*math.pi * freq*x/size + phase)
		for x in range(size)]

def weighted_sum(amplitudes, noises, size):
	output = [0.0] * size
	for k in range(len(noises)):
		for x in range(size):
			output[x] += amplitudes[k] * noises[k][x]
	return output

def random_ift(amplitude, size):
	frequencies = range(1, 31)
	output = []
	random.seed()
	amplitudes = [amplitude(f) for f in frequencies]
	noises = [noise(f, size) for f in frequencies]
	sum_of_noises = weighted_sum(amplitudes, noises, size)
	return sum_of_noises

def weighted_random(min, max):
	num = 0
	for i in range(min):
		num += random.uniform(1, max/min)
	return num
	
def lowest_roll(minimum, max, numberOfRolls):
	rolls = []
	for i in range(numberOfRolls):
		roll = weighted_random(minimum, max)
		rolls.append(roll)
	return min(rolls)