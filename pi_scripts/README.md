# Pi Scripts

This directory contains the Raspberry Pi scripts to automate the process of taking snapshots from cameras and uploading them to the Goodspeed backend, as well as generate a dchpd configuration. 
These scripts use a cut sheet located at /backend/data. The cut sheet must be a CSV file in this format:
```
Building:,Halley Rise,
Subnet:,10.110.70.x,
Camera Number,MAC,
2,ec:71:db:68:e0:9e,
3,ec:71:db:04:22:c1,
4,ec:71:db:7d:e4:d4,
...
```

## Requirements

1. **Environment File (`.env`)**:
   - A `.env` file must exist in the same directory as the script.
   - The `.env` file must include the following lines:
     ```
     CSV_FILE="../backend/data/HalleyRiseCutSheet.csv"
     CAMERA_PASSWORD="<password_for_cameras>"
     ```
   - Replace `CSV_FILE` with the path to your CSV file containing camera details and `CAMERA_PASSWORD` with the password used to access the cameras.

2. **Executable Permissions**:
   - Ensure the script has executable permissions. Use the following command:
     ```bash
     chmod +x <script_name>.sh
     ```

3. **Default "No Image" File**:
   - The `no_image` file must be present in the same directory as the script. This file is uploaded if a snapshot cannot be taken.

---

## Usage

### `take_snapshots.sh`

1. **Run the Script Manually**:
   - To take snapshots and upload them to the backend:
     ```bash
     ./take_snapshots.sh
     ```

2. **Set Up Cron Job**:
   - Automate the script to run at regular intervals using `crontab`:
     ```bash
     crontab -e
     ```
   - Add the following line to execute the script every 20 minutes:
     ```bash
     */20 * * * * /path/to/your/script/take_snapshots.sh
     ```

   - Save and exit. The script will now run automatically as per the schedule.

---

### `generate_dhcp_config.sh`

This script generates a `.txt` file containing DHCP configuration for the cameras and subnet specified in the cut sheet CSV. The contents of the generated file can be copied into `/etc/dhcp/dhcpd.conf`.

1. **Run the Script**:
Ensure that the .env file is present in the same directory (instructions at the top of this README)
   ```bash
   ./generate_dhcp_config.sh

2. **Output**:
The script generates a file named dhcp_config_generated.txt in the same directory (ignored by git.)

3. **Copy to DHCP Configuration:**
Copy the contents of dhcp_config_generated.txt into your /etc/dhcp/dhcpd.conf file to configure the DHCP server for the cameras.