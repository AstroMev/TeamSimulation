#!/usr/bin/env python -B
# -*- coding: utf-8 -*-

import TeamProgressModel as TPM

import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm

"""
モデルを使用してゴール時刻のヒストグラムを作成
"""

if __name__ == '__main__':
    num_member = 5
    num_team = 5000
    
    goal_data1 = [0] * num_team
    goal_data2 = [0] * num_team

    freq_meeting1 = 5
    pbar = tqdm(range(len(goal_data1)))
    for i in pbar:
        goal_data1[i] = TPM.ProjectLocus(num_member, freq_meeting1)._goal_time

    freq_meeting2 = 20
    pbar = tqdm(range(len(goal_data1)))
    for i in pbar:
        goal_data2[i] = TPM.ProjectLocus(num_member, freq_meeting2)._goal_time
    
    sns.set()
    
    plt.title('{} members'.format(num_member))
    plt.xlabel('Goal time',fontsize=18)
    plt.ylabel('Frequency',fontsize=18)
    plt.xlim(0.5, 100.5)

    plt.hist(goal_data1, bins=20, alpha=0.6, histtype='stepfilled', color='r', label='MTG:{}'.format(freq_meeting1), range=(0.5, 100.5))
    plt.hist(goal_data2, bins=20, alpha=0.6, histtype='stepfilled', color='g', label='MTG:{}'.format(freq_meeting2), range=(0.5, 100.5))
    
    plt.legend()
    plt.savefig('Result_AnaGoalTime.png')
