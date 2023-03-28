# Benchmarks Targeted for Jetson (Using GPU+2DLA)

The script will run following Benchmarks:
- Names : Input Image Resolution <br />
- Inception V4 : 299x299 <br />
- ResNet-50 : 224x224 <br />
- OpenPose : 256x456<br />
- VGG-19  : 224x224<br />
- YOLO-V3 : 608x608<br />
- Super Resolution  : 481x321<br />
- Unet : 256x256 <br />

For benchmark results on all NVIDIA Jetson Products; please have a look at [NVIDIA jetson_benchmark webpage](https://developer.nvidia.com/embedded/jetson-benchmarks)

Following scripts are included:
1. Installation requirements for running benchmark script (install_requirements.sh)
2. CSV files containing parameters (benchmark_csv folder)
3. Download Model (utils/download_models.py)
4. Running Benchmark Script (benchmarks.py)


### Version Dependencies:
- JetPack 4.4+ <br />
- TensorRT 7+ <br />

### Set up instructions
``` git clone https://github.com/NVIDIA-AI-IOT/jetson_benchmarks.git``` <br />
``` cd jetson_benchmarks ``` <br />
``` mkdir models ``` # Open folder to store models (Optional) <br />

### Install Requirements
``` sudo sh install_requirements.sh```<br />
Note: All libraries will be installed for ```python3```

# For Jetson Xavier NX
### Download Models
``` python3 utils/download_models.py --all --csv_file_path <path-to>/benchmark_csv/nx-benchmarks.csv --save_dir <absolute-path-to-downloaded-models>```

### Running Benchmarks
#### Running All Benchmark Models at Once
``` sudo python3 benchmark.py --all --csv_file_path <path-to>/benchmark_csv/nx-benchmarks.csv --model_dir <absolute-path-to-downloaded-models>```  <br />

#### Sample Output
|  **Model Name** | **FPS** |
| :--- | :--- |
|  inception_v4 | 311.73 |
|  vgg19_N2 | 66.43 |
|  super_resolution_bsd500 | 150.46 |
|  unet-segmentation | 145.42 |
|  pose_estimation | 237.1 |
|  yolov3-tiny-416 | 546.69 |
|  ResNet50_224x224 | 824.02 |
|  ssd-mobilenet-v1 | 887.6 |
#### Running an Individual Benchmark Model
1. For Inception V4 <br/>
``` sudo python3 benchmark.py --model_name inception_v4 --csv_file_path <path-to>/benchmark_csv/nx-benchmarks.csv --model_dir <absolute-path-to-downloaded-models>```  <br />

2. For VGG19<br/>
``` sudo python3 benchmark.py --model_name vgg19 --csv_file_path <path-to>/benchmark_csv/nx-benchmarks.csv --model_dir <absolute-path-to-downloaded-models>```  <br />

3. For Super Resolution<br/>
``` sudo python3 benchmark.py --model_name super_resolution --csv_file_path <path-to>/benchmark_csv/nx-benchmarks.csv --model_dir <absolute-path-to-downloaded-models>```  <br />

4. For UNET Segmentation<br/>
``` sudo python3 benchmark.py --model_name unet --csv_file_path <path-to>/benchmark_csv/nx-benchmarks.csv --model_dir <absolute-path-to-downloaded-models>```  <br />

5. For Pose Estimation<br/>
``` sudo python3 benchmark.py --model_name pose_estimation --csv_file_path <path-to>/benchmark_csv/nx-benchmarks.csv --model_dir <absolute-path-to-downloaded-models>```  <br />

6. For Tiny-YOLO-V3<br/>
``` sudo python3 benchmark.py --model_name tiny-yolov3 --csv_file_path <path-to>/benchmark_csv/nx-benchmarks.csv --model_dir <absolute-path-to-downloaded-models>```  <br />

7. For ResNet-50<br/>
``` sudo python3 benchmark.py --model_name resnet --csv_file_path <path-to>/benchmark_csv/nx-benchmarks.csv --model_dir <absolute-path-to-downloaded-models>```  <br />

8. For SSD-MobileNet-V1 Segmentation<br/>
``` sudo python3 benchmark.py --model_name ssd-mobilenet-v1 --csv_file_path <path-to>/benchmark_csv/nx-benchmarks.csv --model_dir <absolute-path-to-downloaded-models>```  <br />

# For Jetson AGX Xavier
Please follow setup and installation requirements. <br/>

### Download Models
``` python3 utils/download_models.py --all --csv_file_path <path-to>/benchmark_csv/xavier-benchmarks.csv --save_dir <absolute-path-to-downloaded-models>```

### Running All Benchmark Models at Once on Jetson AGX Xavier <br/>
```
sudo python3 benchmark.py --all --csv_file_path <path-to>/benchmark_csv/xavier-benchmarks.csv \
                          --model_dir <absolute-path-to-downloaded-models> \
                          --jetson_devkit xavier \
                          --gpu_freq 1377000000 --dla_freq 1395200000 --power_mode 0 --jetson_clocks
```

# For Jetson TX2 and Jetson Nano
Please follow setup and installation requirements. <br/>

### Download Models
``` python3 utils/download_models.py --all --csv_file_path <path-to>/benchmark_csv/tx2-nano-benchmarks.csv --save_dir <absolute-path-to-downloaded-models>```

### Running All Benchmark Models at Once on Jetson TX2
```
sudo python3 benchmark.py --all --csv_file_path <path-to>/benchmark_csv/tx2-nano-benchmarks.csv \
                            --model_dir <absolute-path-to-downloaded-models> \
                            --jetson_devkit tx2 \
                            --gpu_freq 1122000000 --power_mode 3 --precision fp16
```

### Running All Benchmark Models at Once on Jetson Nano
```
sudo python3 benchmark.py --all --csv_file_path <path-to>/benchmark_csv/tx2-nano-benchmarks.csv \
                            --model_dir <absolute-path-to-downloaded-models> \
                            --jetson_devkit nano \
                            --gpu_freq 921600000 --power_mode 0 --precision fp16
```

# For Jetson Orin
Please follow setup and installation requirements. <br/>

### Download Models
``` python3 utils/download_models.py --all --csv_file_path <path-to>/benchmark_csv/orin-benchmarks.csv --save_dir <absolute-path-to-downloaded-models>```

### Running All Benchmark Models at Once on Orin <br/>

Please check if Orin is in MAX power mode:
`nvpmodel -q` <br />
It should say:
```
NV Power Mode: MAXN
0
```

If it isn't, set it to MAX power mode:
`sudo nvpmodel -m 0`. Then run:

```
sudo python3 benchmark.py --all --csv_file_path <path-to>/benchmark_csv/orin-benchmarks.csv \
                          --model_dir <absolute-path-to-downloaded-models>
```

For Jetson Orin Nano
Please follow setup and installation requirements. <br/>

### Download Models
``` python3 utils/download_models.py --all --csv_file_path <path-to>/benchmark_csv/orin-nano-benchmarks.csv --save_dir <absolute-path-to-downloaded-models>```

### Running All Benchmark Models at Once on Orin Nano<br/>

```
sudo python3 benchmark.py --all --csv_file_path <path-to>/benchmark_csv/orin-nano-benchmarks.csv \
                          --model_dir <absolute-path-to-downloaded-models> --jetson_clocks
```
