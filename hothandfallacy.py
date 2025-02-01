# Hot Hand Fallacy: Monte Carlo Simulations
#
# This program will simulate 10,000 60-shot shooting sequences of a basketball 
# player with a field goal percentage of 31%, where each shot is independent of 
# the other. Then, it will compute the probability of hitting a shot following a 
# streak of three successful hits. 
#

import random
import statistics
import numpy as np
import math
import matplotlib.pyplot as plt

#
# Generate a nested array of 10,000 60-shot sequences. if there are no 3-shot streaks, 
# disregard the sequence and generate a new one. 
#
# array[i][j] --> i = 10,000, j = 60
# 

def generate_sequences(): 
    added = 0
    simulation = []
    while added < 10000: 
        p = 0.31 # 31% success rate
        sequence = []
        for i in range(60): 
            float = random.random() # generate a random float between 0 and 1
            if float > 0.31: 
                shot = 0
            else: 
                shot = 1
            sequence.append(shot)

        if has_streak(sequence): 
            simulation.append(sequence)
            added += 1
    
    return simulation


def has_streak(sequence): 
    for i in range(2, len(sequence) - 1): 
        if sequence[i] == 1 and sequence[i-1] == 1 and sequence[i-2] == 1: # there is a 3-shot streak 
            return True 
    return False
    

#
# For each sequence, count number of shots scored following a 3-shot streak.
#
probabilities = []
streak_count = [] # to get avg number of streaks per sequence
sequences = generate_sequences()

for i in range(10000): 
    sequence = sequences[i]
    count = 0 # number of streaks
    hothands = 0 # number of hits right after a streak
    for i in range(2, len(sequence) - 1): 
        if sequence[i] == 1 and sequence[i-1] == 1 and sequence[i-2] == 1: # there is a 3-shot streak 
            count += 1
            if sequence[i+1] == 1: # successful hot hand
                hothands += 1
    probability = hothands/count
    # print("hothands: " + str(hothands))
    # print("count: " + str(count))
    streak_count.append(count)
    probabilities.append(probability)

print("Average value: " + str(statistics.mean([i for row in sequences for i in row])))
print("Total number of streaks: " + str(sum(streak_count)))
print("Average number of streaks per sequence: " + str(statistics.mean(streak_count)))

print("\nAverage probability: " + str(statistics.mean(probabilities)))

# calculating 1st and 3rd quartile 
sorted_prob = sorted(probabilities)
q1_pos = 0.25 * 10001
if isinstance(q1_pos, int): 
    q1 = sorted_prob[q1_pos-1]
else: 
    q1 = sorted_prob[math.floor(q1_pos)-1] + (q1_pos%1)*(sorted_prob[math.ceil(q1_pos)-1] - sorted_prob[math.floor(q1_pos)-1])

q2_pos = 0.5 * 10001
if isinstance(q2_pos, int): 
    q2 = sorted_prob[q2_pos-1]
else: 
    q2 = (sorted_prob[math.floor(q2_pos)-1] + sorted_prob[math.floor(q1_pos)-1]) / 2

q3_pos = 0.75 * 10001
if isinstance(q3_pos, int): 
    q3 = sorted_prob[q3_pos-1]
else: 
    q3 = sorted_prob[math.floor(q3_pos)-1] + (q3_pos%1)*(sorted_prob[math.ceil(q3_pos)-1] - sorted_prob[math.floor(q3_pos)-1])

print("Min: " + str(min(probabilities)))
print("Max: " + str(max(probabilities)))
print("1st Quartile: " + str(q1))
print("Median: " + str(q2))
print("3rd Quartile: " + str(q3))
print("Standard Deviation: " + str(np.std(probabilities)))

#
# Generate a figure that represents the sample distribution of probabilities 
#
plt.figure(figsize=(10, 6))
plt.hist(probabilities, bins=15, edgecolor='black', color='blue')  
plt.title('Sample Distribution of Probabilities of Hot-Hand Shot', fontsize=16)
plt.xlabel('Probability of a Hit After a 3-Hit Streak', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.axvline(statistics.mean(probabilities), color='red', linestyle='dashed', linewidth=2, label=f"Mean: {statistics.mean(probabilities):.4f}")
# plt.axvline(q1, color='orange', linestyle='dotted', linewidth=2, label=f"Q1: {q1:.4f}")
# plt.axvline(q2, color='yellow', linestyle='dotted', linewidth=2, label=f"Q2: {q2:.4f}")
# plt.axvline(q3, color='green', linestyle='dotted', linewidth=2, label=f"Q3: {q3:.4f}")
plt.legend(fontsize=12)
plt.grid(alpha=0.3)
plt.show() 
