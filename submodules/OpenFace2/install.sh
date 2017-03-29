#!/bin/bash
#==============================================================================
# Title: install.sh
# Description: Install everything necessary for OpenFace to compile.
# Author: Daniyal Shahrokhian <daniyal@kth.se>
# Date: 20170310
# Version : 1.0
# Usage: bash install.sh <directory in which you want the project to be installed>
# NOTES: There are certain steps to be taken in the system before installing 
#        via this script (refer to README): Run 
#        `sudo gedit /etc/apt/sources.list` and change the line 
#        `deb http://us.archive.ubuntu.com/ubuntu/ xenial main restricted` to 
#        `deb http://us.archive.ubuntu.com/ubuntu/ xenial main universe`
#==============================================================================

# Exit script if any command fails
set -e 
set -o pipefail

if [ $# -ne 1 ]
  then
    echo "Usage: install.sh <directory in which you want the project to be installed>"
    exit 1
fi

DIRECTORY="$1"
cd "$DIRECTORY"
echo "Installation under ${DIRECTORY}"

# Essential Dependencies
echo "Installing Essential dependencies..."
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install llvm

sudo apt-get update
sudo apt-get install clang-3.7 libc++-dev libc++abi-dev
sudo apt-get install cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev checkinstall
echo "Essential dependencies installed."

# OpenCV Dependency
echo "Downloading OpenCV..."
if [ -d "opencv-3.1.0" ]; then
  sudo rm -r "opencv-3.1.0"
fi

wget https://github.com/Itseez/opencv/archive/3.1.0.zip
unzip 3.1.0.zip
rm 3.1.0.zip
cd opencv-3.1.0
mkdir build
cd build
echo "Installing OpenCV..."
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=ON -D BUILD_SHARED_LIBS=OFF ..
make -j4
sudo make install
cd "../.."
echo "OpenCV installed."

# Boost C++ Dependency
echo "Installing Boost..."
sudo apt-get install libboost-all-dev
echo "Boost installed."

# OpenFace installation
echo "Downloading OpenFace..."
if [ -d "OpenFace" ]; then
  sudo rm -r "OpenFace"
fi

git clone https://github.com/TadasBaltrusaitis/OpenFace.git
cd OpenFace
mkdir build
cd build
echo "Installing OpenFace..."
cmake -D CMAKE_BUILD_TYPE=RELEASE ..
make
echo "OpenFace installed."

# Installation test
echo "Testing installation..."
./bin/FaceLandmarkVid -f "../videos/changeLighting.wmv"
echo "Installation tested."
