from collections import defaultdict


def read_wine_data():
    """逐行从wine.data读取样本数据"""
    with open('wine.data', 'r') as fp:
        data = fp.readline()
        while data and data != '\n':
            yield data
            data = fp.readline()


def build_iris_group():
    """每一行样本数据，对不同的class进行group by"""
    records = defaultdict(list)
    for each in read_wine_data():
        splits = each.split(',')
        records[splits[0]].append([float(s) for s in splits[1:]])  # 将数据从字符串还原为float类型并加入总集合
    return records
