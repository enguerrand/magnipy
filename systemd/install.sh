#!/bin/bash
set -e
if [[ $(id -u) -eq 0 ]]; then
       echo "Do not run as root"
       exit 255
fi       
cd "$(dirname "$0")"/..
install_dir=$(pwd)
systemd_user_dir=${HOME}/.config/systemd/user
mkdir -p "${systemd_user_dir}"
sed -e "s#/path/to/install/dir/magnipy/#${install_dir}/#g" ./systemd/magnipy@.service  > "${systemd_user_dir}"/magnipy@.service
systemctl --user daemon-reload
echo "Systemd service file installed. See ${install_dir}/README.md for further instructions."

