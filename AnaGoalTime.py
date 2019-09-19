#!/usr/bin/env python -B
# -*- coding: utf-8 -*-

import TeamProgressModel as TPM

import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm

num_member = 5
freq_meeting = 10
num_team = 1000

goal_data = [0] * num_team

pbar = tqdm(range(len(goal_data)))
for i in pbar:
    goal_data[i] = TPM.ProjectLocus(num_member, freq_meeting)._goal_time

sns.set()

plt.title('{} members, {} meetings/time'.format(num_member, freq_meeting))
plt.xlabel('Goal time',fontsize=18)
plt.ylabel('Frequency',fontsize=18)

plt.xlim(0.5, 100.5)

plt.hist(goal_data, bins=100, range=[0.5, 100.5])
plt.savefig('Result_AnaGoalTime.png')
