#!/bin/bash
set -e
if [ $(id -u) -eq 0 ]; then
       echo "Do not run as root"
       exit -1
fi       
cd $(dirname "$0") 
install_dir=$(pwd)
systemd_user_dir=${HOME}/.config/systemd/user
mkdir -p ${systemd_user_dir}
sed -e "s#/path/to/install/dir/magnipy/#${install_dir}/#g" ./systemd/magnipy@.service  > ${systemd_user_dir}/magnipy@.service
systemctl --user daemon-reload

cat << EOF
Systemd service file installed
To start the daemon on camera "/dev/video0" run:

    systemctl --user start magnipy@video0.service

To make it start automatically upon login run:

    systemctl --user enable magnipy@video0.service"

EOF

