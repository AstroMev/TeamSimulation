#!/usr/bin/env python -B
# -*- coding: utf-8 -*-

"""
チームプロジェクト作業進捗トイモデル
"""

import numpy as np
from tqdm import tqdm

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import seaborn as sns

class ProjectLocus:
    
    def __init__(self, num_member, num_meeting):
        self._num_member = num_member # チームメンバー数
        self._num_meeting = num_meeting # 開催会議回数

        self._g = 1. # 後戻りの力

        self._deltaT = 1.
        self._tt = np.arange(0., 100., self._deltaT) # 描画するための時間設定
    
        self._r = 5. # メンバー１人の力
        self._theta_all = np.full((self._tt.size, self._num_member), np.pi/2) # 各時間の各メンバーの作業ベクトル角度
        
        self._u_all = np.zeros((self._tt.size, self._num_member))    # 各メンバーの作業ベクトルx軸
        self._v_all = np.full((self._tt.size, self._num_member), self._r) # 各メンバーの作業ベクトルy軸
        
        self._x_all = [0.] # 各時間のチーム進捗位置X軸
        self._y_all = [0.] # 各時間のチーム進捗位置Y軸

        self._goal_time = 100. # ゴール時刻
        
        self.calc_locus() # 軌跡を計算する        
        del self._theta_all
    
    def calc_locus(self):
        
        for i in range(len(self._tt)):
            if(i == 0):
                continue

            self._next_flag = True
            for m in range(self._num_member):

                self._theta_all[i][m] = self._theta_all[i-1][m] + (np.random.randn() * np.pi/12)
                
                self._u_all[i][m] = self._r * np.cos(self._theta_all[i-1][m])
                self._v_all[i][m] = self._r * np.sin(self._theta_all[i-1][m])

                if(abs(self._x_all[i-1]) >= 100): # グラフ外に出た場合
                    self._theta_all[i][m] = np.pi - self._theta_all[i][m]
                    self._u_all[i][m] = -1 * self._u_all[i][m]
                
                if(i % self._num_meeting == 0): # 会議開催の場合
                    self._theta_all[i][m] = np.pi / 2.
                    self._u_all[i][m] = 0
                    self._v_all[i][m] = self._r
                    self._next_flag = False
                    
                if(self._y_all[i-1] >= 100.): # プロジェクト完了の場合
                    self._u_all[i][m] = 0
                    self._v_all[i][m] = 0
                    self._next_flag = False
                    
                    if(self._goal_time > self._tt[i]): # ゴール時刻の記録
                        self._goal_time = self._tt[i]

            self._x = self._u_all[i][m]*self._deltaT + self._x_all[i-1]  # x(t)の記述
            self._y = ( -(self._g/2)*self._deltaT**2 + self._v_all[i][m]*self._deltaT ) * self._next_flag + self._y_all[i-1] # y(t)の記述
            
            self._x_all.append(self._x) # xの時々刻々データを格納
            self._y_all.append(self._y) # yの時々刻々データを格納

            
def MakeProgressAnim(fig, each_team_num_member, each_team_num_meeting):

    num_team = len(each_team_num_member)
    
    Progress = []
    goal_time_list = [100.] * num_team
    
    for team_i in range(num_team):
        Progress.append(ProjectLocus(each_team_num_member[team_i], each_team_num_meeting[team_i]))

    ims_all = []
    flag_legend = True
    pbar = tqdm(range(len(Progress[0]._tt)))
    for t_i in pbar:

        ims_sum = []
        stop_flag = True
        
        for team_i in range(num_team):
            # 時刻tにおける質点と，時刻tに至るまでの運動の軌跡の二つの絵を作成し， アニメーション用のリストに格納する。
            #im_p = plt.plot(Progress[team_i]._x_all[t_i], Progress[team_i]._y_all[t_i], 'o',
            #                Progress[team_i]._x_all, Progress[team_i]._y_all,
            #                '--', label='MTG:{} G:{}'.format(each_team_num_meeting[team_i], Progress[team_i]._goal_time),
            #                color=cmap(team_i),markersize=10, linewidth = 2, aa=True)
            
            im_p = plt.plot(Progress[team_i]._x_all[t_i], Progress[team_i]._y_all[t_i], marker='o',
                            label='MTG:{}\nGOAL:{}'.format(each_team_num_meeting[team_i], Progress[team_i]._goal_time),
                            color=cmap(team_i), markersize=10, aa=True)
            
            im_l = plt.plot(Progress[team_i]._x_all, Progress[team_i]._y_all, '--',
                            #label='GOAL:{}'.format(Progress[team_i]._goal_time),
                            color=cmap(team_i), linewidth=2, aa=True)
            
            im_q = plt.quiver(Progress[team_i]._x_all[t_i], Progress[team_i]._y_all[t_i],
                              Progress[team_i]._u_all[t_i] * 2.5, Progress[team_i]._v_all[t_i] * 2.5,
                              color=cmap(team_i), angles='xy',scale_units='xy',scale=1)

            # タイトルテキスト
            title = plt.text(xmin, xmax, 
                             'Time : {:.1f}'.format(Progress[0]._tt[t_i] + 1),
                             ha='left', va='bottom',fontsize=10)

            stop_flag = stop_flag and (Progress[team_i]._y_all[t_i] >= 100.)
            
            ims_sum += im_p + [im_q] + [title]

        if flag_legend: # 一回のみ凡例を描画
            plt.legend(bbox_to_anchor=(1.04, 1), loc='upper left', borderaxespad=0)
            flag_legend = False

        ims_all.append(ims_sum)
        
        if stop_flag: # 全てのグループがゴールしていたらアニメーション終了
            break

    del Progress
    # 右側の余白を調整
    plt.subplots_adjust(right=0.7)
    anim = ArtistAnimation(fig, ims_all) # アニメーション作成
    return anim


if __name__ == '__main__':

    anim = [] #アニメーション用に描くパラパラ図のデータを格納するためのリスト

    #deltaT = 1.
    #tt = np.arange(0., 100., deltaT) # 描画するための時間設定
    
    #V0 = 5. # メンバー１人の力
    #g= 1. # 重力定数
    each_team_num_member = [10, 10, 10] # 各チームメンバー数
    each_team_num_meeting = [5., 12., 20.] # 各チーム会議回数

    # 描画のカスタマイズ    
    sns.set()    
    fig = plt.figure()
    cmap = plt.get_cmap("tab10")
    
    xmin = -100.
    xmax = 100.

    plt.title('{} members'.format(each_team_num_member[0]))
    plt.ylabel('Progress [%]',fontsize=18)

    plt.xlim(xmin, xmax)
    plt.ylim(-10, 110)
    
    plt.hlines([0], xmin, xmax, linestyles="-")  # y=0に線を描く。
    plt.hlines([100], xmin, xmax, colors='r', linestyles="dashed")  # y=0に線を描く。
    
    anim = MakeProgressAnim(fig, each_team_num_member, each_team_num_meeting)
    
    anim.save("Result.gif", writer='imagemagick')   # gifアニメーションファイルを作成する
