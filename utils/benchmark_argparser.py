import argparse

class benchmark_argparser():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='')
        self.parser.add_argument('--csv_file_path', dest='csv_file_path', help='csv for model download and parameters', type=str)
        self.parser.add_argument('--model_dir', dest='model_dir', help='path to downloaded path', type=str)
        benchmark_group = self.parser.add_mutually_exclusive_group()
        benchmark_group.add_argument('--model_name', dest='model_name', help='only specified models will be executed', type=str)
        benchmark_group.add_argument('--all', dest='all', help='all models from DropBox will be downloaded',
                                      action='store_true')
        self.parser.add_argument('--jetson_devkit', dest='jetson_devkit', default='xavier-nx', help='Input Jetson Devkit name', type=str)
        # For Jetson Xavier: set to 'xavier'
        # For Jetson TX2: set to 'tx2'
        # For Jetson Nano: set to 'nano'
        self.parser.add_argument('--power_mode', dest='power_mode', help='Jetson Power Mode', default=0, type=int)
        # For Jetson Xavier: set to 0 (MAXN)
        # For Jetson TX2: set to 3 (MAXP)
        # For Jetson Nano: set to 0 (MAXN)
        # For Jetson NX: for JP4.4 set to 0, JP4.6+ set to 8 (MAXN)
        self.parser.add_argument('--precision', dest='precision', default='int8',
                                 help='precision for model int8 or fp16', type=str)
        # For Jetson Xavier: set to int8
        # For Jetson TX2: set to 3 fp16
        # For Jetson Nano: set to fp16
        self.parser.add_argument('--jetson_clocks', dest='jetson_clocks', help='Set Clock Frequency to Max (jetson_clocks)',
                                      action='store_true')
        self.parser.add_argument('--gpu_freq', dest='gpu_freq', default=1109250000,help='set GPU frequency', type=int)
        # Default values are for Xavier-NX
        # For Xavier set gpu_freq to 1377000000: Find using  $sudo cat /sys/devices/17000000.gv11b/devfreq/17000000.gv11b/available_frequencies
        # For TX2 set gpu freq to 1300500000: Find using $sudo cat /sys/devices/gpu.0/devfreq/17000000.gp10b/available_frequencies
        # For Nano set gpu freq to 921600000: Find using $sudo cat /sys/devices/gpu.0/devfreq/57000000.gpu/available_frequencies
        self.parser.add_argument('--dla_freq', dest='dla_freq', default=1100800000, help='set DLA frequency', type=int)
        # Default values are for Xavier-NX
        # For Xavier set dla_freq to 1395200000 : Find using $sudo cat /sys/kernel/debug/bpmp/debug/clk/nafll_dla/max_rate
        self.parser.add_argument('--plot', dest='plot', help='Perf in Graph', action='store_true')
    def make_args(self):
        return self.parser.parse_args()
