### 1. Download Raspberry Pi Imager onto SD Card
Please download here:
[Raspberry Pi Imager](https://www.raspberrypi.com/software/)

### 2. Flash the ISO on the Pi
Open raspberry pi imager and configure the settings based on the list below:  
Raspberry Pi 5 - Ubuntu 24.04 Desktop 64bit  
Raspberry Pi 4 - Ubuntu 22.04 Desktop 64bit  
Once the flash is done put the SD back into the Pi  

### 3. Setting up Ubuntu
Select English  
Time Zone - Whatever time zone the Pi will be in  
About you:  
Full Name - goodspeedXX  
Username - goodspeedXX  


### 4. Update the OS

sudo apt upgrade
sudo apt update

This will download firefox on the Pi

### 5. Add the device to tailscale
[Tailscale](https://login.tailscale.com/admin/machines)

curl -fsSL https://tailscale.com/install.sh | sh

# 6. Add OpenSSH
