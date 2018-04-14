import numpy as np
from matplotlib import pyplot as plt


def generate_rdn_wsn(n: int, r: float):
    """生成给定网络规模数量为n 通信半径为r的WSN"""
    orig = np.matrix(np.random.random((n, n)))
    orig[orig > r] = 0  # 距离大于通信半径的都为不连通
    return orig


def is_connect(m: np.matrix):
    """判断矩阵在hop跳范围内是否联通"""
    final = np.zeros(m.shape)
    hop = max(m.shape[0], m.shape[1])
    for i in range(hop):
        final += m
        m *= m
    return final.all()


def range_r_fix_n(ns: tuple):
    """每次1000次仿真 给定不同节点规模n 通信半径r在变化 生成连通率实验图"""
    simulate_times = 1000
    percentages = list()
    rs = [r / 100 for r in range(0, 100, 3)]
    for n in ns:
        for radius in rs:
            total_con = 0
            for i in range(simulate_times):
                mat = generate_rdn_wsn(n, radius)
                if is_connect(mat):
                    total_con += 1
            percentages.append(total_con / simulate_times)
        plt.plot(rs, percentages, label='n={}'.format(n))
        percentages.clear()
    plt.xlabel('communication radius')
    plt.ylabel('Pr [network is connected]')
    plt.grid(True)
    plt.savefig('range_r_fix_n.svg', format='svg')
    plt.show()


def test_one_range_r_with_n(n):
    simulate_times = 1000
    percentages = list()
    rs = [r / 100 for r in range(0, 100, 3)]
    for radius in rs:
        total_con = 0
        for i in range(simulate_times):
            mat = generate_rdn_wsn(n, radius)
            if is_connect(mat):
                total_con += 1
        percentages.append(total_con / simulate_times)
    plt.plot(rs, percentages, label='n={}'.format(n))
    plt.xlabel('communication radius')
    plt.ylabel('Pr [network is connected]')
    plt.grid(True)
    plt.savefig('test1.svg', format='svg')
    plt.show()


def range_n_fix_r(rs: tuple):
    """每次1000次仿真 给定不同的通信半径r 节点数目在变化 生成连通率实验图"""
    simulate_times = 1000
    percentages = list()
    nodes = [n for n in range(0, 101, 5)]
    for r in rs:
        for n in nodes:
            if n == 0:
                percentages.append(0)
                continue
            total_con = 0
            for i in range(simulate_times):
                mat = generate_rdn_wsn(n, r)
                if is_connect(mat):
                    total_con += 1
            percentages.append(total_con / simulate_times)
        plt.plot(nodes, percentages, label='r={}'.format(r))
        percentages.clear()
    plt.xlabel('number of nodes')
    plt.ylabel('Pr [network is connected]')
    plt.grid(True)
    plt.savefig('range_n_fix_r.svg', format='svg')
    plt.show()


def test_one_range_n_with_r(r):
    simulate_times = 1000
    percentages = list()
    nodes = [n for n in range(0, 101, 5)]
    for n in nodes:
        if n == 0:
            percentages.append(0)
            continue
        total_con = 0
        for i in range(simulate_times):
            mat = generate_rdn_wsn(n, r)
            if is_connect(mat):
                total_con += 1
        percentages.append(total_con / simulate_times)
    plt.plot(nodes, percentages, 'x-', label='r={}'.format(r))
    plt.xlabel('number of nodes')
    plt.ylabel('Pr [network is connected]')
    plt.grid(True)
    plt.savefig('test2.svg')
    plt.show()


if __name__ == '__main__':
    # range_r_fix_n((10, 20, 50, 100))
    # range_n_fix_r((0.05, 0.15, 0.25, 0.35, 0.45))
    # test_one_range_r_with_n(10)
    # test_one_range_n_with_r(0.45)
    import networkx as nx
    G = nx.Graph()
    matrix = generate_rdn_wsn(20, 0.1)
    matrix[matrix > 0] = 1
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            G.add_edge(i, j)

    nx.draw(G)
    plt.savefig('matrix.svg')
    plt.show()
