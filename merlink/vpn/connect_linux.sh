#!/bin/bash
# Copyright 2018 Ross Jacobs All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


echo "Entering linux bash script..."
echo "\nVPN name: $1\nServer Address: $2\nPSK: $3\nUsername: $4\nPassword: $5\n"
# This bash file will create and connect an L2TP VPN connection on linux
# 5 required params to use this script
if [[ -z $1 ]] || [[ -z $2 ]] || [[ -z $3 ]] || [[ -z $4 ]] || [[ -z $5 ]];
    then
    echo "Incorrect number of arguments, expecting 5"
    echo "Correct usage:\n  bash ./connect_linux.sh 'MyVpnName' \
    'MyServerAddress' 'MyPsk' 'MyUsername' 'MyPassword'"
    sleep 5
    exit 5
fi

# Verify that we have required packages
# Verify that we have network-manager
if [ $(which nmcli) != '/usr/bin/nmcli' ]; then
    echo "ERROR: nmcli is not installed!"
    echo "Please install Network Manager. \
    (https://wiki.gnome.org/Projects/NetworkManager)"
    sleep 5
    exit 1
fi

# Each OS will have a <OS type>-release file in /etc
# Checking for deb and rpm because they come as prebuilt packages
# https://github.com/nm-l2tp/network-manager-l2tp/wiki/Prebuilt-Packages
# deb-based systems
# The presence of this file may be a cleaner indicator of l2tp plugin:
# /etc/NetworkManager/VPN/nm-l2tp-service.name
if [[ -f /etc/debian_version ]] &&
   [[ -z $(dpkg -l network-manager-l2tp 2>/dev/null) ]]; then
	echo "ERROR: network-manager-l2tp must be installed"
	sleep 5
	exit 2
# rpm-based systems
elif [[ -f /etc/redhat-release ]] &&
     [[ -z $(rpm -qa NetworkManager-l2tp 2>/dev/null) ]]; then
	echo "ERROR: NetworkManager-l2tp must be installed"
	sleep 5
	exit 3
fi

# Linux Mint doesn't come with strongswan-plugin-openssl, which is required.
if [[ $(cat /etc/os-release | grep Mint) ]] &&
   [[ -z $(dpkg -l strongswan-plugin-agent) ]]; then
	echo "ERROR: strongswan-plugin-openssl must be installed. Exiting..."
	sleep 5
	exit 4
fi

# Set variables from params
# Remove special characters [`!$'" ]
# vpn_name has max of 15 chars, so cut off vpn_name if longer.
vpn_name="$(echo $1 | sed 's/[\`\!\$\/'\''\"\ ]//g' | cut -c1-15)"
echo 'vpn_name: '${vpn_name}
# If the vpn_name is now empty due to these removals, name it l2tp
if [[ -z vpn_name ]]; then vpn_name='merlink-l2tp-vpn'; fi
mx_address=$2
psk=$3
username=$4
password=$5

# Generate NetworkManager VPN connection
nmcli con add type vpn ifname ${vpn_name} vpn-type l2tp

# Edit the connection that was just created
# Config is stored at /etc/NetworkManager/system-connections/$connection.id
# nmcli prepends connection.id with 'vpn-'; remove this
sudo nmcli con modify "vpn-${vpn_name}" \
	connection.id ${vpn_name} \
	connection.autoconnect yes \
	connection.permissions $(whoami) \
	vpn.data \
	    gateway=${mx_address},ipsec-enabled='yes',ipsec-esp='3des-sha1',\
ipsec-forceencaps='yes',ipsec-ike='3des-sha1-modp1024',ipsec-psk=${psk},\
password-flags='0',user=${username},service-type=\
'org.freedesktop.NetworkManager.l2tp' \
    vpn.secrets password=${password}

# Reload the connections
sudo nmcli con reload
# REQUIRED for network-manager-l2tpd to work (see description for
#   https://launchpad.net/~seriy-pr/+archive/ubuntu/network-manager-l2tp)
# networkmanage-l2tp spawns its own xl2tpd so if
#   one has already been started, it will interfere
sudo service xl2tpd stop
sudo systemctl disable xl2tpd 2>/dev/null

# Connect
sudo nmcli con up id ${vpn_name}

# Disconnect
#sudo nmcli con down id $vpn_name
