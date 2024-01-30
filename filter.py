import numpy as np

def generate_data(length=None, baseline=None, noise_amplitude=None, peak_amplitude=None, peak_width=None, num_peaks=None):
    # 生成基线数据

    length = length or np.random.randint(1000, 1500)
    baseline = baseline or np.random.uniform(25, 35)
    noise_amplitude = noise_amplitude or np.random.uniform(0.005, 0.02)
    peak_amplitude = peak_amplitude or np.random.uniform(3, 7)
    peak_width = peak_width or np.random.randint(15, 25)
    num_peaks = num_peaks or np.random.randint(3, 7)

    baseline_data = np.ones(length) * baseline

    for _ in range(num_peaks):
        # 随机生成峰值
        peak_start = np.random.randint(0, length - peak_width)
        peak_end = peak_start + peak_width
        peak_values = np.linspace(0, peak_amplitude, peak_width)

        # 在峰值之前的部分
        yield from baseline_data[:peak_start] + np.random.uniform(-noise_amplitude, noise_amplitude, peak_start)

        # 在峰值范围内的部分
        yield from baseline_data[peak_start:peak_end] + np.random.uniform(-noise_amplitude, noise_amplitude, peak_width) + peak_values

        # 在峰值之后的部分
        yield from baseline_data[peak_end:] + np.random.uniform(-noise_amplitude, noise_amplitude, length - peak_end)

# 使用生成器
generator = generate_data()

# 生成数据
generated_data = np.array(list(generator))

# 绘制图形
import matplotlib.pyplot as plt
plt.plot(generated_data)
plt.title("Generated Data with Peaks")
plt.xlabel("Index")
plt.ylabel("Value")
plt.show()

class PeakCounterFilter:
    def __init__(self, window_size=100, threshold_factor=3):
        self.window_size = window_size
        self.data_window = []
        self.threshold_factor = threshold_factor

    def process_frame(self, frame):
        # 将新帧添加到窗口
        self.data_window.append(frame)

        # 保持窗口大小不超过指定的大小
        if len(self.data_window) > self.window_size:
            self.data_window.pop(0)

        # 统计窗口内的峰值数量
        peak_count = self.count_peaks()

        return peak_count

    def count_peaks(self):
        # 从窗口数据中获取最后一个窗口的数据
        recent_data = np.array(self.data_window[-self.window_size:])

        # 通过均值和标准差估计峰值和基线的范围
        mean_value = np.mean(recent_data)
        std_dev = np.std(recent_data)

        # 使用均值和标准差计算峰值和基线的阈值
        peak_threshold = mean_value + self.threshold_factor * std_dev
        baseline_threshold = mean_value - self.threshold_factor * std_dev

        # 通过阈值判断峰值的数量
        peak_count = np.sum(recent_data > peak_threshold)

        return peak_count


# 使用 PeakCounterFilter
filter_instance = PeakCounterFilter()

import matplotlib.pyplot as plt



# 处理生成的数据并记录峰值数量
peak_counts = []

for data_point in generated_data:
    peak_count = filter_instance.process_frame(data_point)
    peak_counts.append(peak_count)

# 绘制峰值数量随时间变化的图形
plt.plot(peak_counts)
plt.title("Number of Peaks in the Last 100 Frames")
plt.xlabel("Frame Index")
plt.ylabel("Number of Peaks")
plt.show()
