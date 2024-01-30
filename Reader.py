import threading
import queue
import pprint
from collections import deque
import artdaq
from artdaq.constants import AcquisitionType
class Reader:
    def __init__(self, task):
        # self.queue = queue.Queue()
        self.queue = deque(maxlen=1000)
        self.queue.append(0)
        self.task = task
        self.task.start()
        self.thread = threading.Thread(target=self.read_data)
        self.thread.start()

    def read_data(self):

        while True:
            data = self.task.read()
            data = abs(data)
            # print(data)
            if len(self.queue) == 0 :
                self.queue.append(0)
            if data >=5 :
                print(data)
                self.queue.append(self.queue[-1] + 1)
            else:
                self.queue.append(self.queue[-1])

    def now(self):
        # max_re = max(self.queue)
        max_re = self.queue[-1]
        self.queue.clear()
        self.queue.append(0)
        return max_re
        # return self.queue.get()

# pp = pprint.PrettyPrinter(indent=4)

if __name__ == '__main__':
    task = artdaq.Task()
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=artdaq.constants.TerminalConfiguration.NRSE)
    task.timing.cfg_samp_clk_timing(
        rate=10000, sample_mode=AcquisitionType.CONTINUOUS)

    reader = Reader(task)
    maaxx = 0
    import time
    # reader.read_data()
    for i in range(10000):
        time.sleep(0.1)
        print(reader.now(), '---')
    # task.stop()
    # task.close()
