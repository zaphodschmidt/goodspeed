#!/bin/bash

# Set the IP address of the camera
camera_ip="10.10.110.10"

# RTSP URL to fetch the snapshot (assuming basic auth with admin:admin credentials)
rtsp_url="rtsp://admin:admin@$camera_ip:554/stream0"

# Directory to save the picture
LOCALDIR="/home/zaphod/camera_pictures"

# Create the directory if it doesn't exist
mkdir -p $LOCALDIR

# Get the current date and time to create a unique filename
DATETIME=$(date +%Y%m%d%H%M%S)

# File name to save the picture with a timestamp
file_name="$LOCALDIR/camera_snapshot_$DATETIME.jpg"

# Use ffmpeg to fetch the image from the RTSP stream and save it locally
ffmpeg -rtsp_transport tcp -i "$rtsp_url" -frames:v 1 -update 1 $file_name

# Print confirmation message
echo "Image saved as $file_name"
