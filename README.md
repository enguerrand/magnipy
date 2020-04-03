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
For the grabbing of touch devices you also need gcc and the linux headers.
Follow these steps to install magnipy:

```bash
## If not already present install python3 python3-dev, python3-venv, gcc and linux headers
## E.g. in Debian-based systems install it with:
# sudo apt install python3 python3-dev python3-venv gcc linux-headers-$(uname -r)
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

## Add user to the input group (name of this group may vary based on distro)
## You may have to log out and log back in for this change to become active 
sudo usermod -a -G input $USER

## You can now run magnipy with the following command 
## (assuming that you installed it to the directory suggested above):
~/git/magnipy/run.sh

## This will use the first camera connected to your computer (i.e. /dev/video0)
## If you wish to use a different camera (e.g. /dev/video2) provide its device name as a command line argument:
~/git/magnipy/run.sh video2

## However, device names in /dev are not predictable. 
## To detect the correct camera in a more reliable way you can use its id as listed by the symlinks in 
## /dev/v4l/by-id/.
## E.g. on my laptop, these devices look like this:
~$ ls -l /dev/v4l/by-id/
total 0
lrwxrwxrwx 1 root root 12 Mar 22 17:27 usb-Chicony_Electronics_Co._Ltd._HD_WebCam-video-index0 -> ../../video0
lrwxrwxrwx 1 root root 12 Mar 22 17:27 usb-Chicony_Electronics_Co._Ltd._HD_WebCam-video-index1 -> ../../video1

## The name of one of these symlinks can be provided as command line argument to magnipy in the same way as the 
## kernel device names (replace the name parameter below by the id as shown in the output of the above command on
## your own computer):
~/git/magnipy/run.sh usb-Chicony_Electronics_Co._Ltd._HD_WebCam-video-index0
```

## Running magnipy as a systemd user service
This step is optional but useful if you would like magnipy to run automatically when a certain device is connected. 
Systemd is required to do this.
```bash
## Install magnipy as a systemd user service
~/git/magnipy/systemd/install.sh
## Once the user service is installed, you can start / enable it with the following commands:
systemctl --user enable magnipy@video0.service  # Start service automatically after login
systemctl --user start magnipy@video0.service   # Start service now

## Use the following commands to stop / disable it:
systemctl --user stop magnipy@video0.service    # Stop service now
systemctl --user disable magnipy@video0.service # Do not start service automatically at login

## In order to address device video0 by its unique id as explained before you can start/enable the service with
systemctl --user start magnipy@usb-Chicony_Electronics_Co._Ltd._HD_WebCam-video-index0.service
```
## Configuration
Certain aspects of the application are configurable.

In order to change the defaults, copy the file config.json from this git repository to $HOME/.magnipy/ (create the
directory if needed or let magnipy create it by running it at least once.)

Then change the content as needed. The parameter names in the json file are reasonably self explanatory. You may have
to check your camera to identify appropriate values.

After running magnipy at least once, a file named runtime.json will also be created in $HOME/magnipy.

This file stores settings such as the zoom level or focus modified by the user at runtime. It is used at the next
startup to restore the previous settings. You can safely delete it if you want to reset these settings to the defaults.

## Keyboard shortcuts
- Panning: Arrow Keys or Touch Input
- Zoom in: + or Enter
- Zoom out: - or Backspace
- Invert colors: i or Space
- Quit: Escape
- Autofocus: f
- Reduce focus: q (implicitly disables autofocus)
- Increase focus: w (implicitly disables autofocus)
