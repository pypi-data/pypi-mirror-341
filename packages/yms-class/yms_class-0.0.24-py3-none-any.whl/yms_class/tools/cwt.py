import os.path
import re

import numpy as np
import matplotlib.pyplot as plt
import pywt
import scipy.io as sio
from tqdm import tqdm

'''
num: 图片保存时防止名字重复，通过末尾数字区分
total: 保存的图片总量
start_num: 从csv表格的第几行开始读取（一般从第二行读取，0代表第二行）
space: 读取间隔（我这里是每1024个采样点作为一个样本）
sampling_period: 采样率（根据数据集实际情况设置，比如数据集采样率为12kHz，则sampling_period = 1.0 / 10000）
totalscal: 小波变换尺度（我这里是256）
wavename: 小波基函数（morl用的比较多，还有很多如：cagu8，cmor1-1等等）
'''


def img_time_freq(data, start_num, end_num, space, sampling_period, totalscal, wavename):
    n = data.shape[1]
    # for i in range(0, n):
    bar_format = '{percentage:.1f}%| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
    for i in tqdm(range(0, n), bar_format=bar_format):
        signals = data[:, i]
        total = int(signals.shape[0] / space)
        start = start_num
        end = end_num
        for j in range(0, total):
            signal = signals[start:end]
            start += space
            end += space
            # 计算小波基函数的中心频率fc,然后根据totalscal 计算参数cparam
            # 通过除以np.arange(totalscal, 0, -1) 来生成一系列尺度值，并存储在scales中
            fc = pywt.central_frequency(wavename)
            cparam = 2 * fc * totalscal
            scales = cparam / np.arange(totalscal, 0, -1)
            # 连续小波变换函数
            coefficients, frequencies = pywt.cwt(signal, scales, wavename, sampling_period)
            # 计算变换系数的幅度
            amp = abs(coefficients)
            # frequencies.max()
            # 根据采样周期生成时间轴
            t = np.linspace(1, sampling_period, 1024, endpoint=False)
            # 绘制时频图
            plt.figure(figsize=(42 / 100, 42 / 100))
            plt.contourf(t, frequencies, amp, cmap='jet')
            plt.axis('off')  # 去坐标轴
            plt.xticks([])  # 去x轴刻度
            plt.yticks([])  # 去y轴刻度
            image_name = r"D:\Code\0-data\2-滚刀磨损数据集\工况2(2db)"
            image_name = os.path.join(image_name, str(i) + '_' + str(j))
            plt.savefig("{}_resized.jpg".format(image_name.split(".jpg")[0]), bbox_inches='tight', pad_inches=0)
            plt.close()


def time_freq(data, num, total, start_num, end_num, space, sampling_period, totalscal, wavename, image_path):
    for i in tqdm(range(0, total)):
        # for i in range(0, total):
        # data = data.loc[start_num:end_num, 'data']
        signals = data[start_num:end_num]
        # 计算小波基函数的中心频率fc,然后根据totalscal 计算参数 cparam
        # 通过除以np.arange(totalscal, 0, -1) 来生成一系列尺度值，并存储在scales中
        fc = pywt.central_frequency(wavename)
        cparam = 2 * fc * totalscal
        scales = cparam / np.arange(totalscal, 0, -1)

        # 连续小波变换函数
        coefficients, frequencies = pywt.cwt(signals, scales, wavename, sampling_period)

        # 计算变换系数的幅度
        amp = abs(coefficients)
        # frequencies.max()

        # 根据采样周期生成时间轴
        t = np.linspace(1, sampling_period, 1024, endpoint=False)

        # 绘制时频图
        image_name = os.path.join(image_path, str(num) + '.jpg')
        plt.figure(figsize=(42 / 100, 42 / 100))
        plt.contourf(t, frequencies, amp, cmap='jet')
        plt.axis('off')  # 去坐标轴
        plt.xticks([])  # 去x轴刻度
        plt.yticks([])  # 去y轴刻度
        # 去白边
        plt.savefig(image_name, bbox_inches='tight', pad_inches=0)
        plt.close()
        start_num += space
        end_num += space
        num += 1


def read_data(path):
    mat = sio.loadmat(path)
    # pattern = r'X\d+_DE_time'
    # matches = re.findall(pattern, str(mat.keys()))[0]
    # return mat[matches]
    return mat['VibrationData2']


if __name__ == '__main__':
    # path = r'F:\BaiduNetdiskDownload\CRWU'
    # listdir_1 = os.listdir(path)
    # for dir_1 in listdir_1:
    #     listdir_2 = os.listdir(os.path.join(path, dir_1))
    #     for dir_2 in listdir_2:
    #         listdir_3 = os.listdir(os.path.join(path, dir_1, dir_2))
    #         for dir_3 in listdir_3:
    #             filename, _ = os.path.splitext(dir_3)
    #             mat_path = os.path.join(path, dir_1, dir_2, dir_3)
    #             image_path = os.path.join(r'D:\Code\deep-learning-algorithms\KAN\CRWU', dir_1, dir_2, filename)
    #             if not os.path.exists(image_path):
    #                 os.makedirs(image_path)
    #             data = read_data(mat_path)[:, 0]
    #             time_freq(data=data, num=1, start_num=0, end_num=1024, space=240, sampling_period=1 / 12000,
    #                       totalscal=256, wavename='morl', total=500, image_path=image_path)

    mat_path = r'D:\YMS\code\tr\VibrationData2(2db).mat'
    # image_path = r"D:\Code\deep-learning-algorithms\KAN\CRWU\Ball\0007\B007_0"
    # if not os.path.exists(image_path):
    #     os.makedirs(image_path)
    data = read_data(mat_path)
    img_time_freq(data=data, start_num=0, end_num=1024, space=1024, sampling_period=1.0 / 12000,
                  totalscal=256, wavename='morl')
    # time_freq(data=data, num=1, start_num=0, end_num=1024, space=240, sampling_period=1 / 12000,
    #           totalscal=256, wavename='morl', total=500, image_path=image_path)
