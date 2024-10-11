# DHCP Server Setup

sudo route del default gw 10.0.0.1 wlan0
sudo ip route del default via 10.10.110.1 dev eth0
E10ADC3949BA59ABBE56E057F20F883E sudo ip -s -s neigh flush all
cat /var/lib/dhcp/dhcpd.leases
ffmpeg -i "rtsp://10.0.0.117:554/h264?username=admin&password=123456" -frames:v 1 /home/goodspeed4/camera_pictures/camera_snapshot_$(date +%Y%m%d%H%M%S).jpg ssh -L 8080:10.10.110.10:80 goodspeed4@100.107.148.66 Camera settings:q change username and password
Camera->video->set video compression to H264, set framerate to 5fps, set quality to best
Network->TCP/IP->Mode->Static  _gateway (10.0.0.1) at 3c:b7:4b:83:65:cc [ether] on wlan0

F0:00:00:B8:39:35
 Two terminals
Outside of range doesn’t matter

* Install Ubuntu on to SD card using Raspberry Pi imager
    * https://www.raspberrypi.com/software/
* Disable ivp6
    * Ubuntu settings -> network -> disable ipv4
* Enable SSH
    * sudo apt update 
    * sudo apt install openssh-server
    * sudo systemctl enable ssh
    * sudo systemctl start ssh
* sudo apt install isc-dhcp-server
* sudo touch /etc/netplan/00-installer-config.yaml
*  sudo cp /etc/netplan/00-installer-config.yaml /etc/netplan/00-installer-config.yaml.bak
*   sudo nano /etc/netplan/00-installer-config.yaml
    * network:
    *   version: 2
    *   renderer: networkd
    *   ethernets:
    *     eth0:
    *       addresses:
    *         - 10.10.110.1/24
    *       dhcp4: no
    *       routes:
    *         - to: default
    *           via: 10.0.0.1                                                                                                                                
    *       nameservers:                                                                                                                                          
    *         addresses:                                                                                                                                         
    *           - 8.8.8.8
    *           - 8.8.4.4
    *     wlan0:                                                                                                                                                  
    *       dhcp4: yes  
*  Sudo netplan try, see if ssh works, Tailscale works, no issues
* Sudo netplan apply
* sudo nano /etc/dhcp/dhcpd.conf
    * subnet 10.10.110.0 netmask 255.255.255.0 { 
    * interface eth0; 
    * range 10.10.110.2 
    * 10.10.110.50; 
    * option subnet-mask 255.255.255.0; 
    * option broadcast-address 10.10.110.255; 
    * }
* sudo nano /etc/default/isc-dhcp-server
    * Edit line INTERFACESv4="" to INTERFACESv4="eth0"
* sudo systemctl restart isc-dhcp-server
* sudo systemctl enable isc-dhcp-server
* sudo systemctl status isc-dhcp-server
* sudo apt install nmap
* sudo nmap -sP 192.168.0.1/24 (address of router)
* Curl ip of suspected camera
    * keep track of MAC address
* sudo nano /etc/dhcp/dhcpd.conf
    * host cam_01 {
    *     option host-name "Camera01";
    *     hardware ethernet 00:fc:01:fd:a6:61; #MAC ADDRESS OF WHAT YOU JUST FOUND
    *     fixed-address 10.10.110.101;
    * }
* In another terminal:
    * ssh -L 8080:10.10.110.10:80 goodspeed4@100.107.148.66
* Then, in a browser, go to http://localhost:8080
    * Then, login with admin and 123456, then go to system ->factory reset
* Clear leases
* Reset dhcp 
* Sudo reboot
* Set camera to have lowest frame rate and h264 instead of h265, and best quality, and set time and date
* sudo apt install ffmpeg
