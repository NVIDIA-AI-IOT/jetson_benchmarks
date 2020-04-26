#!/bin/sh
if [ "$#" -ne 1 ]; then
    echo "Usgae ./run_xavier_maxn.sh <Password>"
    echo " Example: ./run_xavier_maxn.sh "nvidia" "
    exit
else
   password=$1 
 
echo $password | sudo -S nvpmodel -m0
echo $password | sudo -S jetson_clocks
