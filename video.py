import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import artdaq
from Reader import Reader
import threading
import queue
from artdaq.constants import  TerminalConfiguration, AcquisitionType
task = artdaq.Task()
task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.NRSE)   # 端口号
task.timing.cfg_samp_clk_timing(
    rate=20000, sample_mode=AcquisitionType.CONTINUOUS)
reader = Reader(task)

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")
        self.videos_list = ['./1.mp4', './2.mp4', './3.mp4']
        self.video_cnt = 0
        self.video_source = self.videos_list[self.video_cnt]
        self.cap = cv2.VideoCapture(self.video_source)

        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = 360
        self.height = 640
        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()

        self.btn_play = ttk.Button(root, text="Play", command=self.play_video)
        self.btn_play.pack(pady=10)

        self.btn_stop = ttk.Button(root, text="Stop", command=self.stop_video)
        self.btn_stop.pack(pady=10)
        self.img = None
        self.flag = False
        self.threshold = 30
        self.cnt = 0
        self.drift = 0
        self.max_num = 0
        self.is_playing = True
        self.update()
        self.root.mainloop()

    def play_video(self):
        self.is_playing = True

    def stop_video(self):
        self.is_playing = False

    def update(self):
         tmp = reader.now()
         # tmp = task.read()
         # tmp  = abs(tmp)
         # tmp = abs(tmp - self.drift) # 清除误差

         # tmp *= 1000
         # self.drift = min(tmpba, self.drift)
         # tmp = tmp - self.drift
         # self.max_num = max(self.max_num, tmp)
         # print(self.cnt ,tmp, self.max_num)

         base1 = 0.25 # 播放、暂停 切换起点
         base2 = 1 # 切换下一个
         # if tmp<base1:
         #     # 多少以下是暂停
         #     # self.is_playing = False if self.is_playing == True else True
         #    self.is_playing = False
         #    print('stop')
         # tmp  = abs(tmp)
         self.cnt += 1
         if self.cnt >= 50:
            self.flag = False
         if tmp >base1 and tmp < base2 and self.cnt>self.threshold:
             # 多少区间内是播放/暂停的切换
            if self.is_playing == True:
                self.is_playing = False
            else:
                self.is_playing = True
            self.cnt = 0
            # self.flag = False
            print("switch mode ")
         if tmp >base2 and not self.flag:
             # 超过多少是切换到下一个视频
            self.video_cnt +=1
            self.video_cnt = 0 if self.video_cnt ==3 else self.video_cnt
            self.cap = cv2.VideoCapture(self.videos_list[self.video_cnt])
            print('switch to next video ')
            # self.video = ''
            # self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            # self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            # self.canvas = tk.Canvas(root, width=self.width, height=self.height)
            # self.canvas.pack()
            self.flag = True
            self.cnt = 0
            print("switch video")
         if self.is_playing:
            print(self.is_playing)
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pilImage = Image.fromarray(frame)
                pilImage = pilImage.resize((360, 640), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image=pilImage)
                self.img = img
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
                # print('111')
                self.root.update_idletasks()
                # self.update()
                # except Exception as e:
                #     self.is_playing = False
                #     self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

                # self.root.after(10, self.update)
            else:
                self.is_playing = False
                print('视频播放完成')
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # else:
         self.root.after(20, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)  # Replace with your video file path
