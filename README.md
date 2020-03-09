# magnipy
A digital magnification glass written in Python

## Motivation
This tool aims at helping visually impaired people to read. It is intended to be used in conjunction with a usb camera attached to a computer.

The usb camera should be positioned such that a book, newspaper or similar document can be placed under it and ideally be fully within the camera's angle of view.

The camera image is displayed in full screen and can be panned / zoomed using the keyboard.

Once started magnipy will grab exclusive access to all touch devices it finds and will use movement gestures to pan the zoomed image.
All multitouch features such as two-fingers scrolling etc. will be disabled to prevent non-tech-savvy users from producing unexpected results.

## Installation
The installation instructions below are applicable for GNU/Linux. Necessary steps on other operating systems may vary.
Especially taking over touch input devices will only work on linux and the user running magnipy must be in the group "input".
(Group name may vary based on distro).

You need python3, python3-dev and python3-venv to install magnipy.
Follow these steps to install magnipy:

```
## If not already present install python3 python3-dev and python3-venv
## E.g. in Debian-based systems install it with:
# sudo apt install python3 python3-dev python3-venv
## 
## Navigate to a directory of your choice where you have write permissions. E.g:
mkdir -p ~/git
cd git
## Now clone this git repo
git clone https://github.com/enguerrand/magnipy.git
cd magnipy
## Create and activate a python virtual env
python3 -m venv venv
source ./venv/bin/activate
## Update pip
pip install -U pip
## Install magnipy's python dependencies
pip install -r requirements.txt

## You can now run magnipy with the following command 
## (assuming that you installed it to the directory suggested above):
#~/git/magnipy/run.sh

## This will use the first camera connected to your computer (i.e. /dev/video0)
## If you wish to use a different camera (e.g. /dev/video2) provide its device 
## name as a command line argument:
#~/git/magnipy/run.sh video2

## Add user to the input group (name of this group may vary based on distro)
## You may have to log out and log back in for this change to become active 
sudo usermod -a -G input $USER

## The following step is optional but useful if you would like magnipy to 
## run automatically when a certain device is connected. 
## Systemd is required to do this.
##
## Install magnipy as a systemd user service
~/git/magnipy/systemd/install.sh
## This script's output will provide further instructions
```
## Keyboard shortcuts
- Panning: Arrow Keys or Touch Input
- Zoom in: + or Enter
- Zoom out: - or Backspace
- Invert colors: i or Space
- Quit: Escape
- Autofocus: f
- Reduce focus: q (implicitly disables autofocus)
- Increase focus: w (implicitly disables autofocus)
