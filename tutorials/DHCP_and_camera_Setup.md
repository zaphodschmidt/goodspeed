# DHCP Server and Camera Setup

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
3. Save this configuration and exit nano by doing CTRL+X, then pressing the y key, and pressing ENTER.
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
4. The output will be a list of devices connected to the network, with their ip addresses and MAC addresses. The camera's entry will likely say "unknown" next to it and have a MAC adress starting with f0:00.
```
Nmap scan report for 10.110.70.3
Host is up (0.00022s latency).
MAC Address: F0:00:00:B8:39:35 (Unknown)
```
5. Curl can be used too determine if an ip is the address of the camera. First, install curl:
```
sudo apt install curl
```
6. Then, do the following command with the suspected ip:
```
sudo curl 
```
7. If the result of this command is a bunch of HTML code for an IP Camera login, record the ip and associated MAC adress you used. If not, try using curl for the other ip's from step 4 in this section.

### 7. Set Static IP for Camera
1. Run the following command:
```
sudo nano /etc/dhcp/dhcpd.conf
```
2. Then, add an entry for the camera, using the MAC address found in the last step. Set the static IP with the subnet of the router and the fourth number within the range 3 to 256.
host cam_01 {
  option host-name "cam_01";
  #MAC address you found from nmap:
  hardware ethernet f0:00:00:b8:39:35;
  #Static IP you want to set for the camera. Make sure it is in the same subnet as the router.
  fixed-address 10.110.70.4;
}
3. Save this configuration and exit nano by doing CTRL+X, then pressing the y key, and pressing ENTER.

### 8. Clear DHCP Leases and Restart DHCP Server
1. Run the following terminal commands:
```bash
sudo rm /var/lib/dhcp/dhcpd.leases
sudo systemctl restart isc-dhcp-server
sudo reboot
```
### 9. Remotely Factory Reset Camera
1. Open another terminal window on your local machine (not SSH'd into the pi) and run the following command with the IP of your camera, the name of your raspberry pi, and the tailscale IP of the raspberry pi:
```
ssh -L 8080:CameraIPAdress:80 PiName@TailscaleIPAddress
```
For example:
```
ssh -L 8080:10.110.70.3:80 goodspeed4@100.107.148.66
```
2. Then, open an internet browser, and go to http://localhost:8080
3. A login page should show up. Login with the username as "admin" and the password as "123456".
4. At the top, click on the "Configuration" tab. Then, on the side, click the System tab, then go to the Factory Reset tab. Click "Restore to Factory."

### 10. Verify Camera DHCP Connection
1. Verify the DHCP server's status by running
```
sudo systemctl status isc-dhcp-server
```
2. Verify that the camera is connected to the DHCP server, by checking that it now has the static ip you specified in step 7. Use nmap:
```
sudo nmap -sP 10.110.70.1/24
```
3. Verify that the camera received a DHCP lease:
```
sudo cat /var/lib/dhcp/dhcpd.leases
```

### 11. Configure Camera settings
1. Open another terminal window on your local machine (not SSH'd into the pi) and run the following command with the IP of your camera, the name of your raspberry pi, and the tailscale IP of the raspberry pi:
```
ssh -L 8080:CameraIPAdress:80 PiName@TailscaleIPAddress
```
For example:
```
ssh -L 8080:10.110.70.3:80 goodspeed4@100.107.148.66
```
2. Then, open an internet browser, and go to http://localhost:8080
3. A login page should show up. Login with the username as "admin" and the password as "123456".
4. Go to the Configuration tab. Then, under the Camera section, go to Video tab. Make sure video compression is set to h264.

### 12. Take a Picture
1. In the raspberry pi's terminal, run:
```
sudo apt install ffmpeg
```
2. Then, run the following command, with the ip adress of your camera and the name of your raspberry pi:
```
ffmpeg -i "rtsp://CameraIPAdress/h264?username=admin&password=123456" -frames:v 1 /home/RaspberryPiName/camera_snapshot_$(date +%Y%m%d%H%M%S).jpg
```
For example:
```
ffmpeg -i "rtsp://10.110.70.3/h264?username=admin&password=123456" -frames:v 1 /home/goodspeed3/camera_snapshot_$(date +%Y%m%d%H%M%S).jpg
```
3. If there are any error messages, diagnose and fix.
4. Open another terminal window on your machine (not SSH'd into the Pi) and run the following command with the name of your pi, its Tailscale IP, and the directory on your machine where you want the picture to be transferred to. In the following example, my pi is goodspeed3@100.110.70.3, and I am transferring the photo to my desktop.
```
scp goodspeed3@100.110.70.3:/home/goodspeed3/camera_snapshot_20241014180343.jpg ~/Desktop/
```
5. Open the picture, and make sure it is not gray. If it is a gray box, then lower the framerate of the camera's video in step 11.
🥳