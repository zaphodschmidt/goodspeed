#!/bin/bash

#This command takes a snapshot from each camera and uploads it to the Goodspeed backend.
#NOTE: There must be a file named ".env" in the same directory as this script, and it must have the lines:
#   CSV_FILE="../backend/data/HalleyRiseCutSheet.csv"
#   CAMERA_PASSWORD="<put the password used to sign into the cameras here.>"
#replace with the path of your CSV file for the cameras for the building this pi is in, and the correct password.

# Variables
# Load environment variables from the .env file
ENV_FILE="$(dirname "$0")/.env"  # Determine the directory of the script and load the .env file

if [[ -f "$ENV_FILE" ]]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)  # Export variables from the .env file
else
    echo "Error: .env file not found in the script directory." >&2
    exit 1
fi

SNAPSHOT_DIR="./snapshots"             

# Ensure snapshot directory exists and clear old snapshots
if [[ ! -d "$SNAPSHOT_DIR" ]]; then
    mkdir -p "$SNAPSHOT_DIR"
fi
rm -f "$SNAPSHOT_DIR"/*

# Variables
CSV_FILE="${CSV_FILE}"  # Default if not in .env
NO_IMAGE_FILE="./no_image.jpeg"  # Path to the default "no image" file
FFMPEG_PASSWORD="${CAMERA_PASSWORD}"
API_ENDPOINT="https://goodspeedbackend.fly.dev/api/upload/"

# Parse building name and subnet from the CSV file
BUILDING_NAME=$(grep -m 1 '^Building:' "$CSV_FILE" | awk -F',' '{print $2}' | xargs)
SUBNET=$(grep -m 1 '^Subnet:' "$CSV_FILE" | awk -F',' '{print $2}' | xargs)
# Remove any 'x' placeholders in the SUBNET value
SUBNET=${SUBNET%.*} 

if [[ -z "$BUILDING_NAME" || -z "$SUBNET" ]]; then
    echo "Error: Could not parse BUILDING_NAME or SUBNET from $CSV_FILE" >&2
    exit 1
fi

echo "Parsed BUILDING_NAME: $BUILDING_NAME"
echo "Parsed SUBNET: $SUBNET"

# Ensure snapshot directory exists and clear old snapshots
if [[ ! -d "$SNAPSHOT_DIR" ]]; then
    mkdir -p "$SNAPSHOT_DIR"
fi
rm -f "$SNAPSHOT_DIR"/*

# Function to take a snapshot
take_snapshot() {
    local cam_number=$1
    local cam_ip="$SUBNET.$cam_number"
    local output_file="$SNAPSHOT_DIR/camera_snapshot_$(date +%Y%m%d%H%M%S)_cam${cam_number}.jpg"

    echo "Taking snapshot for Camera $cam_number at $cam_ip..." >&2
    ffmpeg -i "rtsp://admin:${FFMPEG_PASSWORD}@${cam_ip}/Preview_01_sub" -frames:v 1 "$output_file" >/dev/null 2>&1

    if [[ -f "$output_file" ]]; then
        echo "$output_file"
    else
        echo ""
    fi
}

# Function to upload the snapshot
upload_snapshot() {
    local cam_number=$1
    local snapshot_file=$2

    if [[ -n "$snapshot_file" && -f "$snapshot_file" ]]; then
        echo "Uploading snapshot for Camera $cam_number..."
        upload_response=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
            -F "image=@${snapshot_file}" \
            -F "cam_num=$cam_number" \
            -F "building_name=$BUILDING_NAME" \
            "$API_ENDPOINT")

        if [[ "$upload_response" == "200" ]]; then
            echo "Successfully uploaded snapshot for Camera $cam_number"
        else
            echo "Failed to upload snapshot for Camera $cam_number - HTTP Status: $upload_response"
        fi
    else
        echo "Error: No snapshot file provided for upload or file does not exist."
    fi
}

# Main script
while IFS=, read -r camera_number mac; do
    if [[ "$camera_number" =~ ^[a-zA-Z]+$ || -z "$camera_number" || ! "$camera_number" =~ ^[0-9]+$ ]]; then
        continue
    fi

    echo "Starting snapshot for Camera $camera_number..."
    snapshot_file=$(take_snapshot "$camera_number")

    # If no snapshot was taken, use the default "no_image" file
    if [[ -z "$snapshot_file" || ! -f "$snapshot_file" ]]; then
        echo "Snapshot for Camera $camera_number was not created. Using default 'no_image' file."
        snapshot_file="$NO_IMAGE_FILE"
    fi

    echo "Debug: Snapshot file to upload: '$snapshot_file'"

    # Upload the snapshot (or the default file)
    if [[ -f "$snapshot_file" ]]; then
        upload_snapshot "$camera_number" "$snapshot_file"
    else
        echo "Error: Neither a snapshot nor the default 'no_image' file could be located."
    fi
done < <(grep -A 1000 '^Camera Number' "$CSV_FILE" | tail -n +2)  # Skip headers

echo "Processing complete!"