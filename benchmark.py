#!/usr/bin/python
from utils import utilities, read_write_data, benchmark_argparser, run_benchmark_models
import sys
import os
import pandas as pd
import gc
import warnings
warnings.simplefilter("ignore")

def main():
    # Set Parameters
    arg_parser = benchmark_argparser()
    args = arg_parser.make_args()
    csv_file_path = args.csv_file_path
    model_path = args.model_dir
    precision = args.precision

    # System Check
    system_check = utilities(jetson_devkit=args.jetson_devkit, gpu_freq=args.gpu_freq, dla_freq=args.dla_freq)
    system_check.close_all_apps()
    if system_check.check_trt():
        sys.exit()
    system_check.set_power_mode(args.power_mode, args.jetson_devkit)
    system_check.clear_ram_space()
    if args.jetson_clocks:
        system_check.set_jetson_clocks()
    else:
        system_check.run_set_clocks_withDVFS()
        system_check.set_jetson_fan(255)

    # Read CSV and Write Data
    benchmark_data = read_write_data(csv_file_path=csv_file_path, model_path=model_path)
    if args.all:
        latency_each_model =[]
        print("Running all benchmarks.. This will take at least 2 hours...")
        for read_index in range (0,len(benchmark_data)):
            gc.collect()
            model = run_benchmark_models(csv_file_path=csv_file_path, model_path=model_path, precision=precision, benchmark_data=benchmark_data)
            download_err = model.execute(read_index=read_index)
            if not download_err:
                # Reading Results
                latency_fps, error_log = model.report()
                latency_each_model.append(latency_fps)
                # Remove engine and txt files
                if not error_log:
                    model.remove()
            del gc.garbage[:]
            system_check.clear_ram_space()
        benchmark_table = pd.DataFrame(latency_each_model, columns=['GPU (ms)', 'DLA0 (ms)', 'DLA1 (ms)', 'FPS', 'Model Name'], dtype=float)
        # Note: GPU, DLA latencies are measured in miliseconds, FPS = Frames per Second
        print(benchmark_table[['Model Name', 'FPS']])
        if args.plot:
            benchmark_data.plot_perf(latency_each_model)

    elif args.model_name == 'inception_v4':
        model = run_benchmark_models(csv_file_path=csv_file_path, model_path=model_path, precision=precision, benchmark_data=benchmark_data)
        download_err = model.execute(read_index=0)
        if not download_err:
            _, error_log = model.report()
            if not error_log:
                model.remove()

    elif args.model_name == 'vgg19':
        model = run_benchmark_models(csv_file_path=csv_file_path, model_path=model_path, precision=precision, benchmark_data=benchmark_data)
        download_err = model.execute(read_index=1)
        if not download_err:
            _, error_log = model.report()
            if not error_log:
                model.remove()

    elif args.model_name == 'super_resolution':
        model = run_benchmark_models(csv_file_path=csv_file_path, model_path=model_path, precision=precision, benchmark_data=benchmark_data)
        download_err = model.execute(read_index=2)
        if not download_err:
            _, error_log = model.report()
            if not error_log:
                model.remove()

    elif args.model_name == 'unet':
        model = run_benchmark_models(csv_file_path=csv_file_path, model_path=model_path, precision=precision, benchmark_data=benchmark_data)
        download_err = model.execute(read_index=3)
        if not download_err:
            _, error_log = model.report()
            if not error_log:
                model.remove()

    elif args.model_name == 'pose_estimation':
        model = run_benchmark_models(csv_file_path=csv_file_path, model_path=model_path, precision=precision, benchmark_data=benchmark_data)
        download_err = model.execute(read_index=4)
        if not download_err:
            _, error_log = model.report()
            if not error_log:
                model.remove()

    elif args.model_name == 'tiny-yolov3':
        model = run_benchmark_models(csv_file_path=csv_file_path, model_path=model_path, precision=precision, benchmark_data=benchmark_data)
        download_err = model.execute(read_index=5)
        if not download_err:
            _, error_log = model.report()
            if not error_log:
                model.remove()

    elif args.model_name == 'resnet':
        model = run_benchmark_models(csv_file_path=csv_file_path, model_path=model_path, precision=precision, benchmark_data=benchmark_data)
        download_err = model.execute(read_index=6)
        if not download_err:
            _, error_log = model.report()
            if not error_log:
                model.remove()

    elif args.model_name == 'ssd-mobilenet-v1':
        model = run_benchmark_models(csv_file_path=csv_file_path, model_path=model_path, precision=precision, benchmark_data=benchmark_data)
        download_err = model.execute(read_index=7)
        if not download_err:
            _, error_log = model.report()
            if not error_log:
                model.remove()

    system_check.clear_ram_space()
if __name__ == "__main__":
    main()
