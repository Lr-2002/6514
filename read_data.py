import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai7")
    # for i in range(100):
    #     x= task.read()
    #     print(i, x)

    # 初始化数据和图形
    data = []
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    # ax.ylim([-10,10])


    # 初始化函数
    def init():
        line.set_data([-10, 10], [-10,10])
        return line,


    # 动画更新函数
    def update(frame):
        # 读取新数据
        new_data = task.read()
        # print(len(data), new_data)
        # if len(data) >150 :
            # data.pop()
            # del(data[0])
        data.append(new_data)

        # 更新图形
        line.set_data(range(len(data)), data)
        ax.relim()
        ax.autoscale_view()
        return line,


    # 配置动画
    ani = animation.FuncAnimation(fig, update, frames=np.arange(100),  # 这里的frames长度决定了动画的持续时间
                                  init_func=init, blit=True)

    plt.show()