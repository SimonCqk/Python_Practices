import random
import time
from multiprocessing import Process

ROUND_UPPER = 10
EXECUTE_TIME_UPPER = 10

processes = []
process_index = 1


def work(sleep_time: int):
    """模拟进程活动，输入参数为运行的时间"""
    time.sleep(sleep_time)


class PCB:
    """模拟PCB，实验中只需要设置进程轮转时间片，执行时间和已占用时间"""

    def __init__(self, round_time, cpu_time):
        self.round_time = round_time
        self.time = cpu_time
        self.occupied_time = 0
        self.process = Process(target=work, args=(self.time,))
        global process_index
        self._index = process_index
        process_index += 1

    def run(self):
        print('Process Index:{index}, round:{prior}, time:{time}, occupied:{occupied}'.format(index=self._index,
                                                                                              prior=self.round_time,
                                                                                              time=self.time,
                                                                                              occupied=self.occupied_time))
        self.process.start()
        self.process.join()
        self.time -= 1
        self.occupied_time += 1
        self.process = Process(target=work, args=(self.time,))


def main():
    p_num = int(input('Input the number of process:'))
    for i in range(p_num):
        processes.append(
            PCB(random.randrange(1, ROUND_UPPER), random.randrange(1, EXECUTE_TIME_UPPER))
        )
    while True:
        if len(processes) > 0:
            for p in processes:
                p.run()
                if p.time == 0:
                    processes.remove(p)
                if p.occupied_time == p.round_time and p in processes:
                    p.occupied_time = 0
                    processes.remove(p)
                    processes.append(p)
        else:
            break


if __name__ == '__main__':
    main()
