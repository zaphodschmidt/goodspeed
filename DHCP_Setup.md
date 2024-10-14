# DHCP Server Setup

### 1. Create Netplan Configuration and Backup
In the terminal, run the following commands:
```bash
sudo touch /etc/netplan/00-installer-config.yaml
sudo cp /etc/netplan/00-installer-config.yaml /etc/netplan/00-installer-config.yaml.bak
```
### 2. Find Router's IP
1. In the terminal, run the command:
```bash
arp -a
```
2. In the resulting list, find an entry that starts with "_gateway" and has an ip address of the form x.x.x.1:
```bash
_gateway (10.110.70.1) at d4:01:c3:54:58:6b [ether] on eth0 
```
3. Record the ip address and its subnet. In this case, the ip adress of the router is 10.110.70.1 and the subnet is 10.110.70.x.

### 3. Configure Netplan
1. In the terminal, run:
```bash
sudo nano /etc/netplan/00-installer-config.yaml
```
2. Using the nano text editor, paste in the following:
```yaml
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    eth0:
      dhcp4: false
      addresses:
#The following line must use the subnet of the router with the fourth number as 2.
        - 10.110.70.2/24
      routes:
        - to: 0.0.0.0/0
#The following line must be the IP of the router.
          via: 10.110.70.1
      nameservers: 
         addresses:
          - 8.8.8.8
          - 8.8.4.4
```
3. Then, edit the lines with comments above them to use the proper subnets.
4. Save this configuration and exit nano by doing CTRL+X, then pressing the y key, and pressing ENTER.
### 4. Apply Netplan configurations
1. Run the following terminal command:
```bash
sudo netplan try
```
2. If the resulting output looks like this:
```bash
Do you want to keep these settings?


Press ENTER before the timeout to accept the new configuration


Changes will revert in 100 seconds
```
Then the configuration is valid and working. Press enter.
If the output indicates there are errors with the netplan, there is no output at all, or connection to the pi is lost, revisit step 3 and ensure all information is correctly entered with proper indentation.
### 5. Install and configure isc-dhcp-server
1. In the terminal, run:
```bash
sudo apt install isc-dhcp-server
```
2. Once installed, run:
```bash
sudo nano /etc/dhcp/dhcpd.conf
```
3. Using the nano text editor, add these lines to the bottom of the file, but with the subnet of your router. For this example, the subnet 10.110.70.x was used.
```conf
subnet 10.110.70.0 netmask 255.255.255.0 {
  interface eth0;
  range 10.110.70.3 10.110.70.50;
  option routers 10.110.70.1;
  option subnet-mask 255.255.255.0;
  option broadcast-address 10.110.70.255; 
}

host cam_01 {
  option host-name "cam_01";
  hardware ethernet f0:00:00:b8:39:35;
  fixed-address 10.110.70.4;
}
```
4. Save this configuration and exit nano by doing CTRL+X, then pressing the y key, and pressing ENTER.

### 5. Configure default interface 
1. Run the command:
```bash
sudo nano /etc/default/isc-dhcp-server
```
2. Using nano, change the line
```
INTERFACESv4=""
```
to
```
INTERFACESv4="eth0"
```
### 6. Enable and Start isc-dhcp-server
Run the following commands in the terminal:
```
sudo systemctl enable isc-dhcp-server
sudo systemctl start isc-dhcp-server
sudo systemctl status isc-dhcp-server
```

### 6. Find MAC address of camera
1. Make sure camera is plugged into the same ethernet switch the camera is plugged into, and ensure there is a green light on the camera's cord indicating it is powered on and transmitting.
2. Run the following command:
```
sudo apt install nmap
```
3. Run the following command with the ip of your router:
```
sudo nmap -sP 10.110.70.1/24
```
4. 
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
