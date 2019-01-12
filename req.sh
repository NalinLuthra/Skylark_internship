#!/usr/bin/env bash

echo "Running apt-get update"
sudo apt-get update

echo "Installing pip for python3"
sudo apt install python3-pip


echo "Installing pysrt to read srt video data files"
pip install pysrt

echo "Installing simplekml to draw KML path from video and mark important points"
pip install simplekml

echo "Installing piexif to read EXIF from jpeg"
pip install piexif