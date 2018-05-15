import random
import time
from multiprocessing import Process

PRIORITY_UPPER = 100
EXECUTE_TIME_UPPER = 15

processes = []
process_index = 1


def work(sleep_time: int):
    """模拟进程活动，输入参数为运行的时间"""
    time.sleep(sleep_time)


class PCB:
    """模拟PCB，实验中只需要设置进程优先级和执行时间"""

    def __init__(self, prior, cpu_time):
        self.prior = prior
        self.time = cpu_time
        self.process = Process(target=work, args=(self.time,))
        global process_index
        self._index = process_index
        process_index += 1

    def run(self):
        print('Process Index:{index}, priority:{prior}, time:{time}'.format(index=self._index, prior=self.prior,
                                                                            time=self.time))
        self.process.start()
        self.process.join()
        self.prior -= 1
        self.time -= 3
        self.process = Process(target=work, args=(self.time,))


def main():
    p_num = int(input('Input the number of process:'))
    for i in range(p_num):
        processes.append(
            PCB(random.randrange(0, PRIORITY_UPPER), random.randrange(0, EXECUTE_TIME_UPPER))
        )
    processes.sort(key=lambda p: p.prior, reverse=True)
    while True:
        if len(processes) > 0:
            cur = processes[0]
            cur.run()
            if cur.time <= 3:
                processes.pop(0)
            processes.sort(key=lambda p: p.prior, reverse=True)
        else:
            break


if __name__ == '__main__':
    main()
