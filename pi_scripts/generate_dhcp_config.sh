#!/bin/bash

# This command generates a .txt file containing camera and subnet configuration for /etc/dhcp/dhcpd.conf. 
# The contents of this txt file can be copied into the dhcpd.conf.
# NOTE: there must be a .env file in this directory that has the line: CSV_FILE='../backend/data/HalleyRiseCutSheet.csv'

# Load environment variables from the .env file
ENV_FILE="$(dirname "$0")/.env"

if [[ -f "$ENV_FILE" ]]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)  # Export variables from the .env file
else
    echo "Error: .env file not found in the script directory." >&2
    exit 1
fi

# Input CSV file
INPUT_FILE="${CSV_FILE}"
SUBNET=$(grep -m 1 '^Subnet:' "$CSV_FILE" | awk -F',' '{print $2}' | xargs)
# Remove any 'x' placeholders in the SUBNET value
SUBNET=${SUBNET%.*} 

# Output DHCP configuration file
OUTPUT_FILE="dhcp_config_generated.txt"

# Header for the DHCP config
cat <<EOF > $OUTPUT_FILE
option domain-name "example.org";
option domain-name-servers ns1.example.org, ns2.example.org;

default-lease-time 600;
max-lease-time 7200;

authoritative;

subnet ${SUBNET}.0 netmask 255.255.255.0 {
    range ${SUBNET}.200 ${SUBNET}.250;
    option routers ${SUBNET}.254;
    option subnet-mask 255.255.255.0;
    option broadcast-address ${SUBNET}.255;

    # Group for fixed-address hosts
    group {
        option subnet-mask 255.255.255.0;
        option domain-name-servers 1.1.1.1, 8.8.8.8;  # Overriding global domain-name-servers
EOF

# Process the CSV file and append to the output file
awk -F',' 'NR>3 && NF>=2 {gsub(/ /, "", $0); print $1, $2}' "$INPUT_FILE" | while read -r CAMERA_NUMBER MAC_ADDRESS; do
    # Skip empty lines or invalid data
    [[ -z "$CAMERA_NUMBER" || -z "$MAC_ADDRESS" ]] && continue

    # Generate host entry
    cat <<EOL >> $OUTPUT_FILE

        host cam_$(printf "%03d" "$CAMERA_NUMBER") {
            hardware ethernet $MAC_ADDRESS;
            fixed-address ${SUBNET}.$CAMERA_NUMBER;
        }
EOL
done

# Close the group and subnet blocks
cat <<EOF >> $OUTPUT_FILE
    }
}
EOF

# Notify user
echo "DHCP configuration generated in $OUTPUT_FILE"
