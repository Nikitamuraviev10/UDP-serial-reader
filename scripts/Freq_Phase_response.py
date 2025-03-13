import sys
import os

# Добавляем путь к папке support в sys.path
support_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "support"))
if support_path not in sys.path:
    sys.path.append(support_path)

import c_deserial
#from bench import data_struct
import matplotlib.pyplot as plt
import numpy as np
import enum

# Мои определения
############################################
import argparse
from scipy.interpolate import interp1d
from scipy.fft import fft, next_fast_len
# Создаём парсер аргументов
parser = argparse.ArgumentParser(description="Открываем файл, переданный из консоли")
# Добавляем аргумент filename (позиционный, обязателен)
parser.add_argument("filename", type=str, help="Имя файла для открытия")
# Разбираем аргументы
args = parser.parse_args()
############################################

data_struct = '''
struct Pack{
	f32 time;
	f32 power_voltage;
	f32 power_current;
	f32 signal_voltage;
	f32 signal_current;
	f32 angle;
	f32 target_angle;
};
'''

class Data():
    def __init__(self):
        self.data = {}

    def set(self, field, data):
        self.data[field] = data

    def get(self, field):
        return np.array(self.data[field])

    def slice(self, start_event, stop_event):
        data = Data()
        b = start_event.index
        if stop_event == None:
            e = len(self.get('time'))
        else:
            e = stop_event.index

        for key in self.data.keys():
            data.set(key, self.get(key)[b:e])

        return data


class Analysis():
    def __init__(self):
        self.deserial = c_deserial.Deserial(data_struct)
        self.data = Data()

    def open(self, fn):
        f = open(fn, 'rb')

        tmp = []
        while(True):
            data = f.read(self.deserial.size())

            if(len(data) != self.deserial.size()):
                break
            tmp.append(self.deserial.to_struct(data))

        tmp = sorted(tmp, key=lambda x: x.time)

        fields = tmp[0].fields()
        for field_name in fields:
            field_arr = [ getattr(d, field_name) for d in tmp ]
            self.data.set(field_name, field_arr)


a = Analysis()
#a.open('2025-02-26 15-46-26_1_30.bin')
a.open(args.filename)

time = a.data.get('time')
target_angle = a.data.get('target_angle')
ang = a.data.get('angle')
cur = a.data.get('power_current')

#plt.plot(np.diff(time))
#plt.show()


# мой код:
#############################################################################################################################################################################################################################
#############################################################################################################################################################################################################################
def moving_average_smoothing(signal, window_size):
    kernel = np.ones(window_size) / window_size
    return np.convolve(signal, kernel, mode='same')

def FFT(dt, y):
    L = len(y)
    m = 5 # Симметричное расширение сигнала с кратным двойке количеством нулей
    N = (2**m) * next_fast_len(L)  # Найти ближайшую степень двойки
    padding = (N - L) // 2
    y_padded = np.pad(y, (padding, N - L - padding), 'constant')
    Y = fft(y_padded)
    LL = len(y_padded)
    f = np.fft.fftfreq(LL, d=dt)  # Частотная шкала
    amplitude_spectrum = np.abs(Y) / len(y)
    return amplitude_spectrum,f,Y,LL

def main():
    t = np.linspace(time.min(), time.max(), len(time))
    dt = t[-1] - t[-2]
    # Если временной дискретизации не хватает, провести интерполяцию на большей временной сетке.
    # Также можно сгладить отработанный сигнал (выходной (angle)).
    # Пока реализована только интерполяция:
    # Создает структуру интерполируемой функции, чтобы иметь возможность подставлять любые значения времени:
    interp_func_s1 = interp1d(time, target_angle, kind='linear', fill_value="extrapolate")
    interp_func_s2 = interp1d(time, ang, kind='linear', fill_value="extrapolate")
    s1 = interp_func_s1(t)
    s2 = interp_func_s2(t)

    '''
    # Посмотреть на исходные интерполированные сигналы:
    plt.plot(t, s1, label="Исходный сигнал") #
    plt.plot(t, s2, label="Сглаженный исходный сигнал") #
    plt.legend()
    plt.grid()
    plt.show()
    '''

    S1 = np.abs(s1)
    window_size = 100 # надо как то вычислить это значение либо полностью изменить способ детектирования границ импульсов
    smoothed_S1 = moving_average_smoothing(S1, window_size)

    '''
    # Посмотреть на моуль target_angle и на его сглаживание
    plt.plot(t, S1, label="Модуль исходного сигнала")
    plt.plot(t, smoothed_S1, label="Сглаженный исходный сигнал")
    plt.legend()
    plt.grid()
    plt.show()
    '''

    # Метод вычисления границ импульсов
    threshold = 0
    impulse_region = smoothed_S1 > threshold
    impulse_start = np.where(np.diff(np.concatenate(([0], impulse_region.astype(int), [0]))) == 1)[0]
    impulse_end = np.where(np.diff(np.concatenate(([0], impulse_region.astype(int), [0]))) == -1)[0]

    #############################
    freq_stor = []
    delta_stor = []
    freq_stor_s2 = []
    std_stor = []
    #############################

    for start, end in zip(impulse_start, impulse_end):
        s1_win = s1[start:end]
        s2_win = s2[start:end]
        corr = np.correlate(s1_win,s2_win,"full")
        max_ind_corr = np.argmax(corr)
        mid = len(corr)/2
        delta = dt*(max_ind_corr-mid)
        delta_stor.append(delta)

        #plt.plot(corr)
        #plt.show()

        '''
        # Посмотреть на импульсы:
        plt.plot(t[start:end], s1_win, label="Импульс target_angle")
        plt.plot(t[start:end], s2_win, label="Импульс angle")
        plt.legend()
        plt.grid()
        plt.show()
        '''

        # FFT target_angle:
        amplitudes_s1,freqs_s1,fft_s1,LL = FFT(dt, s1_win)
        max_ind_s1 = np.argmax(amplitudes_s1)
        freq_stor.append(np.ceil(freqs_s1[max_ind_s1]))


        # FFT angle:
        amplitudes_s2,freqs_s2,fft_s2,LL = FFT(dt, s2_win)
        max_ind_s2 = np.argmax(amplitudes_s2)
        freq_stor_s2.append(np.ceil(freqs_s2[max_ind_s2]))

        # АЧХ:
        #std_stor.append(np.std(s2_win) / np.std(s1_win))
        std_stor.append(    abs( np.max(amplitudes_s2) / np.max(amplitudes_s1) )  )


    freq_stor = np.array(freq_stor)
    freq_stor_s2 = np.array(freq_stor_s2)
    std_stor = np.array(std_stor)
    delta_stor = np.array(delta_stor)

    ############################################################################
    # Проверка коректности сигналов:
    #print(delta_stor) # Может проверкой корректности сигнала т.к. эти значения должы быть примено равными
    try:
        if np.array_equal(freq_stor, freq_stor_s2):
            print("Частоты задающего и отработанного сигналов идентичны")
        else:
            print("Частоты задающего и отработанного сигналов разные")
    except Exception as e:
        print(f"Ошибка при сравнении массивов: {e}")
    ############################################################################

    print('Частоты основных гармоник target angle:')
    print(freq_stor)
    print('Частоты основных гармоник angle:')
    print(freq_stor_s2)

    plt.plot(freq_stor, std_stor, 'o-')
    plt.xlabel('Частота (Гц)')
    plt.title('АЧХ')
    plt.grid()
    plt.show()

    # ФЧХ:
    plt.plot(freq_stor, (180/np.pi)*(-2*np.pi)*(freq_stor)*(delta_stor), 'o-')
    plt.xlabel(r'Угол$^\circ$')
    plt.title('ФЧХ')
    plt.grid()
    plt.show()
################################################################################################################




main()