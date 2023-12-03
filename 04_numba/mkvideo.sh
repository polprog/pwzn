#!/bin/bash


if [ $# -lt 2 ]; then
    echo "Usage: $0 directory/ videoname"
    exit 1
fi


ffmpeg -framerate 10 -pattern_type glob -i $1/'*.png' \
       -c:v libx264 -r 30 -pix_fmt yuv420p $2
