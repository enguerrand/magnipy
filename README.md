# magnipy
A digital magnification glass written in Python

## Motivation
This tool aims at helping visually impaired people to read. It is intended to be used in conjunction with a usb camera attached to a computer.

The usb camera should be positioned such that a book, newspaper or similar document can be placed under it and ideally be fully within the camera's angle of view.

The camera image is displayed in full screen and can be panned / zoomed using the keyboard.

## Installation
You need python3 and python3-venv to install magnipy.
Follow these steps to install magnipy:

```
# If not already present install python3 and python3-venv
# E.g. in Debian-based systems install it with:
# sudo apt install python3-venv
# 
# Navigate to a directory of your choice where you have write permissions. E.g:
mkdir -p ~/git
cd git
# Now clone this git repo
git clone https://github.com/enguerrand/magnipy.git
cd magnipy
# Create and activate a python virtual env
python3 -m venv venv
source ./venv/bin/activate
# Update pip
pip install -U pip
# Install magnipy's dependencies
pip install -r requirements.txt

# You can now run magnipy with the following command 
# (assuming that you installed it to the directory suggested above):
~/git/magnipy/run.sh
# This will use the first camera connected to your computer (i.e. /dev/video0)
# If you wish to use a different camera (e.g. /dev/video2) provide its device 
# name as a command line argument:
/path/to/magnipy/run.sh video2

# The following step is optional but useful if you would like magnipy to 
# run automatically when a certain device is connected. 
# Systemd is required to do this.
#
# Install magnipy as a systemd user service
~/git/magnipy/systemd/install.sh
# This script's output will provide further instructions
```
## Keyboard shortcuts
- Panning: Arrow Keys
- Zoom in: +
- Zoom out: -
- Invert colors: i
- Quit: q
