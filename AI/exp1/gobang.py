class ChessBoard:
    """棋盘的主体类，包括了所有核心操作"""

    NONE = 0
    MAX = 1
    MIN = 2
    FIVE_TYPE = 1
    SFOUR_TYPE = 2
    FOUR_TYPE = 3
    STHREE_TYPE = 4
    THREE_TYPE = 5
    STWO_TYPE = 6
    TWO_TYPE = 7
    MAX_VALUE = 100000
    MIN_VALUE = -100000
    FIVE_W = 100000
    SFOUR_W = 10000
    FOUR_W = 5000
    STHREE_W = 2000
    THREE_W = 1000
    STWO_W = 500
    TWO_W = 200
    ONE_W = 10

    def __init__(self, rows=11, cols=11):
        self.rows = rows
        self.cols = cols
        self.data = [[self.NONE for _ in range(cols)] for _ in range(rows)]
        self.wins = [[set() for _ in range(cols)] for _ in range(rows)]  # 存储不同的赢法
        self.count = 0  # 赢法的种数
        self.max_win = list()  # 记录最大化每一种赢法的达成棋子数
        self.min_win = list()  # 记录最小化每一种赢法的达成棋子数
        self.stack = []  # 模拟栈，存放下棋的记录
        self.ended = False
        # 初始化赢法数组
        # 横向寻找赢法
        for i in range(rows):
            for j in range(cols - 4):  # j <= cols - 5
                for k in range(5):
                    #  self.wins[i][j+k][self.count] = True
                    self.wins[i][j + k].add(self.count)
                self.count += 1
        # 纵向寻找赢法
        for i in range(cols):
            for j in range(rows - 4):
                for k in range(5):
                    # 同上
                    self.wins[j + k][i].add(self.count)
                self.count += 1
        # 右上斜向寻找赢法
        for i in range(rows - 4):
            for j in range(cols - 4):
                for k in range(5):
                    self.wins[i + k][j + k].add(self.count)
                self.count += 1
        # 左下斜向赢法
        for i in range(rows - 4):
            for j in range(cols - 4):
                for k in range(5):
                    self.wins[i + k][j - k].add(self.count)
                self.count += 1
        for i in range(self.count):
            self.max_win.append({'max': 0, 'min': 0})
            self.min_win.append({'min': 0, 'max': 0})

    def current(self):
        """返回最新下的一步棋"""
        if len(self.stack) > 0:
            return self.stack[-1]

    def put(self, row, col, dot_type):
        """
        下棋，这一步骤的主函数
        :param row: 将要下的行
        :param col: 将要下的列
        :param dot_type: 人类还是AI
        """
        assert self.is_valid(row, col), \
            '将要下的棋子超出棋盘的边界或者位置已有棋子！'
        self.data[row][col] = dot_type
        self.stack.append({
            'row': row,
            'col': col,
            'dot_type': dot_type
        })
        # 落子之后，更新每一种赢法
        for i in range(self.count):
            if i in self.wins[row][col]:
                if dot_type == self.MAX:
                    self.max_win[i]['max'] += 1
                    self.min_win[i]['max'] += 1
                else:
                    self.min_win[i]['min'] += 1
                    self.max_win[i]['min'] += 1
        if len(self.stack) == self.rows * self.cols:
            self.ended = True

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and \
               self.data[row][col] == self.NONE

    def get_near_points(self, point):
        pass
