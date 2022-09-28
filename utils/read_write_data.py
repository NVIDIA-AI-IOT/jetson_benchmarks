import pandas as pd
import re
import os
import datetime
from datetime import timedelta
# Class for read csv and write to csv or panda or graph generate
class read_write_data():
    def __init__(self, csv_file_path, model_path):
        self.csv_file_path =csv_file_path
        self.model_path = model_path
        self.start_valid_time = 0
        self.end_valid_time = 0
    def benchmark_csv(self, read_index):
        data = pd.read_csv(self.csv_file_path)
        model_name = data['ModelName'][read_index]
        self.framework = data['FrameWork'][read_index]
        self.num_devices = data['Devices'][read_index]
        ws_gpu = data['WS_GPU'][read_index]
        ws_dla = data['WS_DLA'][read_index]
        model_input = data['input'][read_index]
        model_output = data['output'][read_index]
        batch_size_gpu = data['BatchSizeGPU'][read_index]
        batch_size_dla = int(data['BatchSizeDLA'][read_index])
        return model_name, self.framework, self.num_devices, ws_gpu, ws_dla, model_input, model_output, batch_size_gpu, batch_size_dla
    def __len__(self):
        return len(pd.read_csv(self.csv_file_path))
    def framework2ext(self):
        if self.framework == 'caffe':
            return str('prototxt')
        if self.framework == 'onnx':
            return str('onnx')
        if self.framework == 'tensorrt':
            return str('uff')

    def read_window_results(self, models):
        self.time_value_window = []
        lpd = [0]*3
        thread_start_time = [datetime.datetime(1940, 12, 1, 23, 59, 59)]*3
        thread_end_time = [datetime.datetime(2040, 12, 1, 23, 59, 59)] * 3
        for e_id in range(0, self.num_devices):
            read_file = os.path.join(self.model_path, str(models[e_id]) + '.txt')
            thread_start_time[e_id], thread_end_time[e_id], thread_time_stamps, thread_latency = self.read_perf_time(read_file)
            self.time_value_window.append([thread_time_stamps, thread_latency])
        try:
            self.late_start(gpu_st=thread_start_time[0], dla0_st=thread_start_time[1], dla1_st=thread_start_time[2])
            self.earliest_end(gpu_et=thread_end_time[0], dla0_et=thread_end_time[1], dla1_et=thread_end_time[2])
            valid_window_frame = self.end_valid_time - self.start_valid_time
            for e_id in range(0, len(self.time_value_window)):
                lpd[e_id] = self.calculate_avg_latency(self.time_value_window[e_id])
        except IndexError:
            pass
        print("----------------------", lpd[0], lpd[1], lpd[2])
        return lpd[0], lpd[1], lpd[2]

    def earliest_end(self, gpu_et, dla0_et, dla1_et):
        if (gpu_et < dla0_et) and (gpu_et < dla1_et):
            self.end_valid_time = gpu_et
        elif (dla0_et < gpu_et) and (dla0_et < dla1_et):
            self.end_valid_time = dla0_et
        else:
            self.end_valid_time = dla1_et

    def late_start(self, gpu_st, dla0_st, dla1_st):
        if (gpu_st > dla0_st) and (gpu_st > dla1_st):
            self.start_valid_time = gpu_st
        elif (dla0_st > gpu_st) and (dla0_st > dla1_st):
            self.start_valid_time = dla0_st
        else:
            self.start_valid_time = dla1_st

    def read_perf_time(self,read_file):
        time_stamps = []
        latencies = []
        add_time = 0
        start_time = datetime.datetime(1940, 12, 1, 23, 59, 59)
        end_time = datetime.datetime(2040, 12, 1, 23, 59, 59)
        with open(read_file, 'r') as f:
            for line in f:
                if "Starting" in line:
                    match_start = re.search(r'\d{2}/\d{2}/\d{4}-\d{2}:\d{2}:\d{2}', line)
                    if match_start:
                        start_time = datetime.datetime.strptime(match_start.group(), '%m/%d/%Y-%H:%M:%S')
                elif "Average on" in line:
                    # latency regex for trtexec 8.4+, end to end latency no longer exists
                    match_above_8_4 = re.search(
                        r'Average\s+on\s+(\d+)\s+runs.*?'
                        r'GPU\s+latency:\s+(\d+\.\d+)\s+.*?',
                        line,
                    )
                    # latency regex for trtexec 7.0 to 8.3
                    match_below_8_4 = re.search(
                        r'Average\s+on\s+(\d+)\s+runs.*?'
                        r'GPU\s+latency:\s+(\d+\.\d+)\s+.*?'
                        r'end\s+to\s+end\s+(\d+\.\d+)\s+ms',
                        line,
                    )
                    
                    if match_below_8_4:
                        add_time += float(match_below_8_4.group(1)) * float(match_below_8_4.group(3)) / 1000
                        time_thread = start_time + timedelta(seconds=add_time)
                        time_stamps.append(time_thread)
                        latencies.append(float(match_below_8_4.group(2)))
                    elif match_above_8_4:
                        add_time += float(match_above_8_4.group(1)) * float(match_above_8_4.group(2)) / 1000
                        time_thread = start_time + timedelta(seconds=add_time)
                        time_stamps.append(time_thread)
                        latencies.append(float(match_above_8_4.group(2)))
                else:
                    continue
        if time_stamps:
            end_time = time_stamps[len(time_stamps)-1]
        return start_time, end_time, time_stamps, latencies

    def calculate_avg_latency(self, time_list):
        _latency = 0
        count = 0
        for i in range(0, len(time_list[0])):
            if self.start_valid_time < time_list[0][i] < self.end_valid_time:
                _latency += time_list[1][i]
                count += 1
        try:
            return _latency / count
        except ZeroDivisionError:
            return 0


    def calculate_fps(self, models, batch_size_gpu, batch_size_dla):
        latency_device = [0] * 5
        FPS = 0
        error_read = 0
        latency_device[0], latency_device[1], latency_device[2] = self.read_window_results(models)
        for e_id in range(0, self.num_devices):
            if latency_device[e_id] != 0:
                if e_id ==0:
                    FPS += batch_size_gpu * (1000 / latency_device[e_id])
                elif e_id ==1 or e_id == 2:
                    FPS += batch_size_dla * (1000 / latency_device[e_id])
            else:
                print('Error in Build, Please check the log in: {}'.format(self.model_path))
                error_read = 1
                continue
        if any(latency == 0 for latency in latency_device[0:self.num_devices]):
            latency_device[len(latency_device) - 2] = 0
            print("We recommend to run benchmarking in headless mode")
        else:
            latency_device[len(latency_device)-2] = FPS
        return latency_device, error_read

    def plot_perf(self, latency_each_model):
        import matplotlib
        matplotlib.use('Gtk3Agg')
        import matplotlib.pyplot as plt
        name = []
        fps = []
        for models in range(0,len(latency_each_model)):
            fps.append(latency_each_model[models][len(latency_each_model[0]) - 2])
            name.append(latency_each_model[models][len(latency_each_model[0]) - 1])
        plt.bar(name, fps)
        plt.figure(figsize=(20, 7))
        plt.bar(name, fps, color='Green')
        plt.ylabel('FPS')
        plt.title('Benchmark Analysis on Jetson')
        plt.grid()
        plt.savefig(str(os.path.join(self.model_path, str('perf_results.png'))))
        print('Please find benchmark results in {}'.format(self.model_path)) 
