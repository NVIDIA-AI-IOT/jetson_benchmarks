import os
import subprocess
import sys
import time
FNULL = open(os.devnull, 'w')
# Class for Utilities (TRT check, Power mode switching)
# https://docs.nvidia.com/jetson/l4t/index.html#page/Tegra%2520Linux%2520Driver%2520Package%2520Development%2520Guide%2Fpower_management_jetson_xavier.html%23wwpID0E0KD0HA
class utilities():
    def __init__(self, jetson_devkit, gpu_freq, dla_freq):
        self.jetson_devkit = jetson_devkit
        self.gpu_freq = gpu_freq
        self.dla_freq = dla_freq
    def set_power_mode(self, power_mode, jetson_devkit):
        power_cmd0 = 'nvpmodel'
        power_cmd1 = str('-m'+str(power_mode))
        subprocess.call('sudo {} {}'.format(power_cmd0, power_cmd1), shell=True,
                        stdout=FNULL)
        print('Setting Jetson {} in max performance mode'.format(jetson_devkit))

    def set_jetson_clocks(self):
        clocks_cmd = 'jetson_clocks'
        subprocess.call('sudo {}'.format(clocks_cmd), shell=True,
                        stdout=FNULL)
        print("Jetson clocks are Set")

    def set_jetson_fan(self, switch_opt):
        fan_cmd = "sh" + " " + "-c" + " " + "'echo" + " " + str(
            switch_opt) + " " + ">" + " " + "/sys/devices/pwm-fan/target_pwm'"
        subprocess.call('sudo {}'.format(fan_cmd), shell=True, stdout=FNULL)

    def run_set_clocks_withDVFS(self):
        if self.jetson_devkit == 'tx2':
            self.set_user_clock(device='gpu')
            self.set_clocks_withDVFS(frequency=self.gpu_freq, device='gpu')
        if self.jetson_devkit == 'nano':
            self.set_user_clock(device='gpu')
            self.set_clocks_withDVFS(frequency=self.gpu_freq, device='gpu')
        if self.jetson_devkit == 'xavier' or self.jetson_devkit == 'xavier-nx':
            self.set_user_clock(device='gpu')
            self.set_clocks_withDVFS(frequency=self.gpu_freq, device='gpu')
            self.set_user_clock(device='dla')
            self.set_clocks_withDVFS(frequency=self.dla_freq, device='dla')
        if self.jetson_devkit == 'orin':
            self.set_user_clock(device='gpu')
            self.set_clocks_withDVFS(frequency=self.gpu_freq, device='gpu')
            self.set_user_clock(device='dla')
            self.set_clocks_withDVFS(frequency=self.dla_freq, device='dla')

    def set_user_clock(self, device):
        if self.jetson_devkit == 'tx2':
            self.enable_register = "/sys/devices/gpu.0/aelpg_enable"
            self.freq_register = "/sys/devices/gpu.0/devfreq/17000000.gp10b"
        if self.jetson_devkit == 'nano':
            self.enable_register = "/sys/devices/gpu.0/aelpg_enable"
            self.freq_register = "/sys/devices/gpu.0/devfreq/57000000.gpu"
        if self.jetson_devkit == 'xavier' or self.jetson_devkit == 'xavier-nx':
            if device == 'gpu':
                self.enable_register = "/sys/devices/gpu.0/aelpg_enable"
                self.freq_register = "/sys/devices/gpu.0/devfreq/17000000.gv11b"
            elif device == 'dla':
                base_register_dir = "/sys/kernel/debug/bpmp/debug/clk"
                self.enable_register = base_register_dir + "/nafll_dla/mrq_rate_locked"
                self.freq_register = base_register_dir + "/nafll_dla/rate"
        if self.jetson_devkit == 'orin':
            self.freq_register = "/sys/kernel/debug/bpmp/debug/clk/"
            self.enable_register = ""   
                
    def set_clocks_withDVFS(self, frequency, device):
        if device == 'gpu':
            freq_register_ = self.freq_register+"nafll_gpc0/rate"
        if device == "dla":
            freq_register_ = self.freq_register+"/nafll_dla0_core/rate"
            
        from_freq = self.read_internal_register(register=freq_register_, device=device)
        self.set_frequency(device=device, enable_register=self.enable_register, freq_register=self.freq_register, frequency=frequency, from_freq=from_freq)
        time.sleep(1)
        to_freq = self.read_internal_register(register=freq_register_, device=device)
        print('{} frequency is set from {} Hz --> to {} Hz'.format(device, from_freq, to_freq))

    def set_frequency(self, device, enable_register, freq_register, frequency, from_freq):
        
        if device == 'gpu':
            freq_register0 = freq_register+"nafll_gpc0/rate"
            freq_register1 = freq_register+"nafll_gpc1/rate"
            self.write_internal_register(freq_register0, frequency)
            self.write_internal_register(freq_register1, frequency)
        elif device =='dla':
            # DLA0 
            enable_register_dla0 = freq_register+"/nafll_dla0_core/mrq_rate_locked"
            freq_register_dla0 = freq_register+"/nafll_dla0_core/rate"
            self.write_internal_register(enable_register_dla0, 1)
            self.write_internal_register(freq_register_dla0, frequency)
            # DLA1
            enable_register_dla1 = freq_register+"/nafll_dla1_core/mrq_rate_locked"
            freq_register_dla1 = freq_register+"/nafll_dla1_core/rate"
            self.write_internal_register(enable_register_dla1, 1)
            self.write_internal_register(freq_register_dla1, frequency)

    def read_internal_register(self, register, device):            
        reg_read = open(register, "r")
        reg_value = reg_read.read().rstrip("\n")
        reg_read.close()
        return reg_value

    def write_internal_register(self, register, value):
        reg_write = open(register, "w")
        reg_write.write("%s" % value)
        reg_write.close()

    def clear_ram_space(self):
        cmd_0 = str("sh" + " " + "-c")
        cmd_1 = str("'echo") + " " + "2" + " " + " >" + " " + "/proc/sys/vm/drop_caches'"
        cmd = cmd_0 + " " + cmd_1
        subprocess.call('sudo {}'.format(cmd), shell=True)

    def close_all_apps(self):
        input("Please close all other applications and Press Enter to continue...")

    def check_trt(self):
        if not os.path.isfile('/usr/src/tensorrt/bin/trtexec'):  # Check if TensorRT is installed
            print("Exiting. Check if TensorRT is installed \n Use ``dpkg -l | grep nvinfer`` ")
            return True
        return False
