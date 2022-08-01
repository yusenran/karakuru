
import itertools

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

from data_store import DataStore
from humanoid import *

def get_bone_pos(bone: Bone)->Vec3d:
    # q_rot: Quaternion = bone.rotation * Quaternion( bone.position, 1.0) * bone.rotation.inverse()
    # return q_rot.image
    return bone.rotation.rotate(bone.position)

def draw_bone(ax, p_pos: Vec3d, c_pos: Vec3d):
    ax.plot([p_pos[0], c_pos[0]], [p_pos[1], c_pos[1]], [p_pos[2], c_pos[2]])

def draw_linked_bones(ax, parent: LinkedBone, stack_pos: Vec3d = vec3d(0,0,0)):
    for child in parent.children:
        parent_pos = get_bone_pos(parent.bone) + stack_pos
        child_pos = get_bone_pos(child.bone) + parent_pos
        draw_bone(ax, parent_pos, child_pos)
        draw_linked_bones(ax, child, parent_pos)

def draw_humanoid(ax, humanoid: VrmHumanoid):

    linked_bone = humanoid_to_linked_bone(humanoid)
    # print(linked_bone)
    draw_linked_bones(ax, linked_bone)

def update_view(frame, ax,_a):
    # print("update_view")
    """グラフを更新するための関数"""
    # 現在のグラフを消去する
    plt.cla()

    humanoid = DataStore.pop()
    if humanoid is None:
        return
    while DataStore.pop() is not None:
        pass

    # 描画
    draw_humanoid(ax, humanoid)

    ax.scatter(0.01 * np.cos(frame), 0.01 * np.sin(frame), 0)

    ax.set_xlim([-0.5, 0.5])
    ax.set_ylim([0.0, 0.5])
    ax.set_zlim([0.0, 0.5])

def draw_anime():
    # 描画領域
    fig = plt.figure(figsize = (8, 8))
    # 3DAxesを追加
    ax = fig.add_subplot(111, projection='3d')

    params = {
        'fig': fig,
        'func': update_view,  # グラフを更新する関数
        'fargs': (ax,0),  # 関数の引数 (フレーム番号を除く)
        'interval': 100,  # 更新間隔 (ミリ秒)
        'frames': itertools.count(0, 0.1),  # フレーム番号を無限に生成するイテレータ
    }
    anime = animation.FuncAnimation(**params)

    # グラフを表示する
    plt.show()


def shutdown_viewer():
    plt.clf()
    plt.close()