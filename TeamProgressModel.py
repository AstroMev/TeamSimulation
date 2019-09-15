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
        
        self._r = V0
        self._theta_all = np.full((tt.size, self._num_member), np.pi/4) # 各時間の各メンバーの作業ベクトル角度
        
        self._u_all = np.zeros((tt.size, self._num_member))    # 各メンバーの作業ベクトルx軸
        self._v_all = np.full((tt.size, self._num_member), V0) # 各メンバーの作業ベクトルy軸
        
        self._x_all = [0.] # 各時間のチーム進捗位置X軸
        self._y_all = [0.] # 各時間のチーム進捗位置Y軸

        self._goal_time = 100. # ゴール時刻
        
        self.calc_locus() # 軌跡を計算する        
        del self._theta_all
    
    def calc_locus(self):
        
        for i in range(len(tt)):
            if(i == 0):
                continue

            self.next_flag = True
            for m in range(self._num_member):

                self._theta_all[i][m] = self._theta_all[i-1][m] + (np.random.randn() * np.pi/12)
                
                self._u_all[i][m] = self._r * np.cos(self._theta_all[i-1][m])
                self._v_all[i][m] = self._r * np.sin(self._theta_all[i-1][m])

                if(i % self._num_meeting == 0): # 会議開催の場合
                    self._u_all[i][m] = 0
                    self._v_all[i][m] = V0
                    self.next_flag = False
                    
                if(self._y_all[i-1] >= 100.): # プロジェクト完了の場合
                    self._u_all[i][m] = 0
                    self._v_all[i][m] = 0
                    self.next_flag = False
                    
                    if(self._goal_time > tt[i]): # ゴール時刻の記録
                        self._goal_time = tt[i]

            self._x = self._u_all[i][m]*deltaT + self._x_all[i-1]  # x(t)の記述
            self._y = ( -(g/2)*deltaT**2 + self._v_all[i][m]*deltaT ) * self.next_flag + self._y_all[i-1] # y(t)の記述
            
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
    pbar = tqdm(range(len(tt)))
    for t_i in pbar:

        ims_sum = []
        for team_i in range(num_team):
            # 時刻tにおける質点と，時刻tに至るまでの運動の軌跡の二つの絵を作成し， アニメーション用のリストに格納する。
            im_p = plt.plot(Progress[team_i]._x_all[t_i], Progress[team_i]._y_all[t_i], 'o',
                            Progress[team_i]._x_all, Progress[team_i]._y_all,
                            '--', label='MTG:{} G:{}'.format(each_team_num_meeting[team_i], Progress[team_i]._goal_time),
                            color=cmap(team_i),markersize=10, linewidth = 2, aa=True)
            
            im_q = plt.quiver(Progress[team_i]._x_all[t_i], Progress[team_i]._y_all[t_i],
                              Progress[team_i]._u_all[t_i], Progress[team_i]._v_all[t_i],
                              color=cmap(team_i), angles='xy',scale_units='xy',scale=1)

            # タイトルテキスト
            title = plt.text((xmin+xmax) /2 , xmax, 
                             'Time : {:f}'.format(tt[t_i]+1),
                             ha='center', va='bottom',fontsize=10)
            
            ims_sum += im_p + [im_q] + [title]

        if flag_legend:#一回のみ凡例を描画
            plt.legend()
            flag_legend = False
        
        ims_all.append(ims_sum)

    del Progress
    anim = ArtistAnimation(fig, ims_all) # アニメーション作成
    return anim


if __name__ == '__main__':

    anim = [] #アニメーション用に描くパラパラ図のデータを格納するためのリスト

    deltaT = 1.
    tt = np.arange(0., 100., deltaT) # 描画するための時間設定
    
    V0 = 10. # 初速度の大きさ
    g= 9.8 / 4 # 重力定数
    each_team_num_member = [4, 4, 4] # 各チームメンバー数
    each_team_num_meeting = [5., 12., 20.] # 各チーム会議回数

    # 描画のカスタマイズ    
    sns.set()    
    fig = plt.figure()
    cmap = plt.get_cmap("tab10")
    
    xmin = -100.
    xmax = 100.
    anim = MakeProgressAnim(fig, each_team_num_member, each_team_num_meeting)
    
    plt.ylabel('Progress',fontsize=18)
    plt.xlim(xmin, xmax)
    plt.ylim(-10, 110)
    plt.hlines([0], xmin, xmax, linestyles="-")  # y=0に線を描く。
    
    anim.save("Result.gif", writer='imagemagick')   # gifアニメーションファイルを作成する
