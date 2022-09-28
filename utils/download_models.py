#!/usr/bin/python
import argparse
import pandas as pd
import subprocess
import shlex
import os

def download_models(url, save_dir):
    cmd = 'wget --quiet --content-disposition --show-progress --progress=bar:force:noscroll --auth-no-challenge --no-check-certificate'+ " "+ url+ " "+'-P'+ save_dir
    args = shlex.split(cmd)
    subprocess.call(args)

def unzip_model_files(model_name,save_dir):
    model_file_path = os.path.join(save_dir,model_name+'.zip')
    cmd = 'unzip -qq'+" " +str(model_file_path)+" "+'-d'+" "+save_dir
    args = shlex.split(cmd)
    subprocess.call(args)
    cmd_rm = 'rm -rf'+" "+model_file_path
    args_rm = shlex.split(cmd_rm)
    subprocess.call(args_rm)

def download_argparser():
    parser = argparse.ArgumentParser(description='Download Models from DropBox')
    parser.add_argument('--save_dir', dest='save_dir', help='downloaded files will be stored here', type=str)
    parser.add_argument('--csv_file_path', dest='csv_file_path', default='./orin-benchmarks.csv', help='csv contains url to download model', type=str)
    downloader_group = parser.add_mutually_exclusive_group()
    downloader_group.add_argument('--all', dest='all', help='all models from DropBox will be downloaded', action='store_true')
    downloader_group.add_argument('--model_name', dest='model_name', help='only specified models will be downloaded', type=str)
    args = parser.parse_args()
    return args

def main():
    downloader_args = download_argparser()
    csv_file = downloader_args.csv_file_path
    save_dir = downloader_args.save_dir
    if downloader_args.all:
        len_csv = len(pd.read_csv(csv_file))
        for read_index in range (0,len_csv):
            url = pd.read_csv(csv_file)['URL'][read_index]
            framework = pd.read_csv(csv_file)['FrameWork'][read_index]
            model_name = pd.read_csv(csv_file)['ModelName'][read_index]
            if framework == 'onnx':
                download_models(str(url), save_dir)
                unzip_model_files(model_name=model_name, save_dir=save_dir)
            else:
                download_models(str(url), save_dir)
    elif downloader_args.model_name == 'inception_v4':
        url = pd.read_csv(csv_file)['URL'][0]
        download_models(url, save_dir)
    elif downloader_args.model_name == 'vgg19':
        url = pd.read_csv(csv_file)['URL'][1]
        download_models(url, save_dir)
    elif downloader_args.model_name == 'super_resolution':
        url = pd.read_csv(csv_file)['URL'][2]
        model_name = pd.read_csv(csv_file)['ModelName'][2]
        download_models(str(url), save_dir)
        unzip_model_files(model_name=model_name, save_dir=save_dir)
    elif downloader_args.model_name == 'unet':
        url = pd.read_csv(csv_file)['URL'][3]
        download_models(url, save_dir)
    elif downloader_args.model_name == 'pose_estimation':
        url = pd.read_csv(csv_file)['URL'][4]
        download_models(url, save_dir)
    elif downloader_args.model_name == 'tiny-yolov3':
        url = pd.read_csv(csv_file)['URL'][5]
        model_name = pd.read_csv(csv_file)['ModelName'][5]
        download_models(str(url), save_dir)
        unzip_model_files(model_name=model_name, save_dir=save_dir)
    elif downloader_args.model_name == 'resnet':
        url = pd.read_csv(csv_file)['URL'][6]
        download_models(url, save_dir)
    elif downloader_args.model_name == 'ssd-mobilenet-v1':
        url = pd.read_csv(csv_file)['URL'][7]
        model_name = pd.read_csv(csv_file)['ModelName'][7]
        download_models(str(url), save_dir)
        unzip_model_files(model_name=model_name, save_dir=save_dir)

if __name__ == '__main__':
    main()

        

