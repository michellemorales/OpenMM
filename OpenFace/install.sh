#!/bin/bash
#==============================================================================
# Title: install.sh
# Description: Install everything necessary for OpenFace to compile.
# Author: Daniyal Shahrokhian <daniyal@kth.se>
# Date: 20170428
# Version : 1.01
# Usage: bash install.sh
# NOTES: There are certain steps to be taken in the system before installing 
#        via this script (refer to README): Run 
#        `sudo gedit /etc/apt/sources.list` and change the line 
#        `deb http://us.archive.ubuntu.com/ubuntu/ xenial main restricted` to 
#        `deb http://us.archive.ubuntu.com/ubuntu/ xenial main universe`
#==============================================================================

# Exit script if any command fails
set -e 
set -o pipefail

if [ $# -ne 0 ]
  then
    echo "Usage: install.sh"
    exit 1
fi

# Essential Dependencies
echo "Installing Essential dependencies..."
sudo apt-get -y update
sudo apt-get -y install build-essential
sudo apt-get -y install llvm
sudo apt-get -y install clang-3.7 libc++-dev libc++abi-dev
sudo apt-get -y install cmake
sudo apt-get -y install libopenblas-dev liblapack-dev
sudo apt-get -y install git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get -y install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev checkinstall
echo "Essential dependencies installed."

# OpenCV Dependency
echo "Downloading OpenCV..."
wget https://github.com/Itseez/opencv/archive/3.1.0.zip
unzip 3.1.0.zip
cd opencv-3.1.0
mkdir -p build
cd build
echo "Installing OpenCV..."
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=ON -D BUILD_SHARED_LIBS=OFF ..
make -j4
sudo make install
cd ../..
rm 3.1.0.zip
sudo rm -r opencv-3.1.0
echo "OpenCV installed."

# Boost C++ Dependency
echo "Installing Boost..."
sudo apt-get install libboost-all-dev
echo "Boost installed."

# OpenFace installation
echo "Installing OpenFace..."
mkdir -p build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE ..
make
cd ..
echo "OpenFace successfully installed."