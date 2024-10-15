#!/bin/bash
#put this file in /home/user/remote_cam_upload

DATETIME=`date +%Y%m%d%H%M%S`

dest='ubuntu@18.214.141.78:/mnt/data/copi/images_and_timestamps/.'

LOCALDIR='/home/zaphod/remote_cam_upload/outputs/'

# All cam ips start at 101 and go up from there
ip_base='10.10.110.10'
n_cams=1

##############

sp="  "
es="';"

for (( i=1; i<$n_cams+1; i++ )); do
    ip=$(printf "%s%02d\n" $ip_base $i)
    echo "$ip"
    

    url='http://admin:admin@'$ip'/tmpfs/auto.jpg'

    echo "Fetching snap from $ip"
    echo "... $url"
    full_pic_name="$LOCALDIR"cam$i.jpg
    wget $url -O $full_pic_name
    
    DATE=`date +%F`
    TIME=`date +%T`
    ss="let text$i = '"

    full_ts_name="$LOCALDIR"ts$i.js
    echo $ss$DATE$sp$TIME$es > $full_ts_name
   
    scp -i "/home/zaphod/aws/ggp1.pem" $full_pic_name $full_ts_name $dest
done

##rtsp_port='554'
##rurl='rtsp://'$ip':'$rtsp_port'/live0.264'
##ffmpeg -r 25 -y -i $rurl -updatefirst 1 -r 2 cam.bmp

