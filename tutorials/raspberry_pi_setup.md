## Step-by-Step Guide: Setting Up Ubuntu on Raspberry Pi

### 1. Download Raspberry Pi Imager

1. Visit the official [Raspberry Pi Imager page](https://www.raspberrypi.com/software/) and download the tool to your computer.
2. Insert your SD card into your computer and open the Raspberry Pi Imager.

### 2. Flash the OS onto the SD Card

1. Open Raspberry Pi Imager and select the appropriate OS version:
   - **Raspberry Pi 5**: Select **Ubuntu 24.04 Desktop (64-bit)**.
   - **Raspberry Pi 4**: Select **Ubuntu 22.04 Desktop (64-bit)**.
2. Configure any other necessary settings (such as hostname, Wi-Fi, and SSH options if required).
3. Click **Write** to flash the OS onto your SD card.
4. Once the flashing is complete, eject the SD card and insert it into the Raspberry Pi.

### 3. Initial Setup of Ubuntu on Raspberry Pi

1. Power on your Raspberry Pi.
2. Follow the on-screen prompts to configure the basic system settings:
   - **Language**: Select **English** (or your preferred language).
   - **Time Zone**: Set the time zone based on the Pi’s location.
   - **About You**:
     - **Full Name**: Enter **goodspeedXX**.
     - **Username**: Set **goodspeedXX** as the username.

### 4. Update the Operating System

Open a terminal and run the following commands to update and upgrade the OS:

```bash
sudo apt update
sudo apt upgrade
```
This will also install Firefox on the Raspberry Pi.

### 5. Set Up Tailscale

To add the Raspberry Pi to your Tailscale network:

1. Open a terminal and run the following commands to install Tailscale:

```bash
sudo apt install curl
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

2. Follow the instructions to log into your Tailscale account and connect the device. You can access your machine list via the Tailscale Admin Console.

3. Then, enter in this command again:
   
```bash
sudo apt install curl
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

### 6. Install OpenSSH

To enable remote access to your Raspberry Pi, install the OpenSSH server and client:

```bash
sudo apt install openssh-server
sudo apt install openssh-client
sudo systemctl enable ssh
sudo systemctl start ssh
```

Once installed, your Pi will be ready for SSH connections.



