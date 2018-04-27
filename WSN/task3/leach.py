import random
import enum
import math
from matplotlib import pyplot as plt

NODE_NUM = 150  # 节点数
PROB_AS_HEAD = 0.05  # 成为簇头的概率
ORIGIN_ENERGY = 300  # 原始的能量
MAX_ROUND = 6  # 最大的轮数

cluster_heads = []


class NodeType(enum.Enum):
    NORMAL = 1
    HEAD = 2


class Node:
    """用于表示节点"""

    def __init__(self, x=None, y=None, node_type=None, flag=None, energy=None):
        self.x = x or random.random()
        self.y = y or random.random()
        self.type = node_type or NodeType.NORMAL
        self.flag = flag or False  # 标记是否曾担任过簇头
        self.energy = energy or ORIGIN_ENERGY


class ClusterHead:
    """用于记录簇头节点"""

    def __init__(self, x, y, round_id):
        self.x = x
        self.y = y
        self.id = round_id


def build_wsn(num=NODE_NUM):
    return [Node() for _ in range(num)]


def check_and_set_state(nodes):
    """检查并更新节点的状态"""
    dead = False
    for node in nodes:
        if node.energy <= 0:
            dead = True
        else:
            node.type = NodeType.NORMAL
    return dead


def draw_clusters(nodes, heads, rnd):
    for head in heads:
        if nodes[head.id].type == NodeType.HEAD:
            plt.scatter(head.x, head.y, color='g')
    for node in nodes:
        if node.type == NodeType.NORMAL:
            plt.scatter(node.x, node.y, color='b')
    min_dist_head = None
    for node in nodes:
        if node.type == NodeType.NORMAL and node.energy > 0:  # 普通节点
            min_dist = 1 << 31
            if len(heads) > 0:  # 存在某簇头
                for head in heads:
                    tmp_dist = math.sqrt(pow(node.x - head.x, 2) + pow(node.y - head.y, 2))
                    if tmp_dist < min_dist:
                        min_dist = tmp_dist
                        min_dist_head = head
            plt.plot([node.x, nodes[min_dist_head.id].x], [node.y, nodes[min_dist_head.id].y], '-')
    plt.savefig('{rnd}.svg'.format(rnd=rnd))
    plt.show()


def elect_head_and_comm(nodes, rnd):
    """通过节点内部选举簇头，并且在节点内部进行通信"""
    heads = []
    for idx, node in enumerate(nodes):
        if node.energy > 0:
            prob = random.random()
            if not node.flag and PROB_AS_HEAD / (1 - PROB_AS_HEAD * (rnd % round(1 / PROB_AS_HEAD))) >= prob:
                node.type = NodeType.HEAD
                node.flag = True
                heads.append(ClusterHead(node.x, node.y, idx))
    cluster_heads.append(heads)
    min_dist_head = None
    for node in nodes:
        if node.type == NodeType.NORMAL and node.energy > 0:  # 普通节点
            min_dist = 1 << 31
            if len(heads) > 0:  # 存在某簇头
                for head in heads:
                    tmp_dist = math.sqrt(pow(node.x - head.x, 2) + pow(node.y - head.y, 2))
                    if tmp_dist < min_dist:
                        min_dist = tmp_dist
                        min_dist_head = head
                    node.energy -= 1  # 选举过程中，广播消息的能量损耗
                node.energy -= 2  # 接受簇头广播过程中的消耗
                nodes[min_dist_head.id].energy -= 1  # 被通知成为簇头
            nodes[min_dist_head.id].energy -= 2  # 发送信息
    # 进入正常通信阶段
    for node in nodes:
        if node.type == NodeType.NORMAL and node.energy > 0:
            node.energy -= 20  # 每轮通信10次，每次损耗2单位能量
        else:
            nodes[min_dist_head.id].energy -= 10
    draw_clusters(nodes, heads, rnd)


wsn_nodes = build_wsn(NODE_NUM)


def simulate_main(rounds):
    first_node_dead = None
    for i in range(rounds):
        if check_and_set_state(wsn_nodes) and not first_node_dead:  # 记录第一个节点死亡的轮数
            first_node_dead = i
        elect_head_and_comm(wsn_nodes, i)
    return first_node_dead


if __name__ == '__main__':
    first_dead = simulate_main(MAX_ROUND)
    print('First node dead in round {rnd}'.format(rnd=first_dead))
