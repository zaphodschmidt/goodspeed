#!/bin/bash

# Variables
ENV_FILE="$(dirname "$0")/.env"

if [[ -f "$ENV_FILE" ]]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "Error: .env file not found in the script directory." >&2
    exit 1
fi

CSV_FILE="${CSV_FILE}"
SNAPSHOT_DIR="./snapshots"
CAMERA_PASSWORD="${CAMERA_PASSWORD}"
API_ENDPOINT="https://goodspeedbackend.fly.dev/api/upload/"

BUILDING_NAME=$(grep -m 1 '^Building:' "$CSV_FILE" | awk -F',' '{print $2}' | xargs)
SUBNET=$(grep -m 1 '^Subnet:' "$CSV_FILE" | awk -F',' '{print $2}' | xargs)
SUBNET=${SUBNET%.*}

if [[ -z "$BUILDING_NAME" || -z "$SUBNET" ]]; then
    echo "Error: Could not parse BUILDING_NAME or SUBNET from $CSV_FILE" >&2
    exit 1
fi

if [[ ! -d "$SNAPSHOT_DIR" ]]; then
    mkdir -p "$SNAPSHOT_DIR"
fi
rm -f "$SNAPSHOT_DIR"/*

# Function to take a snapshot via HTTP API
take_snapshot() {
    local cam_number=$1
    local cam_ip="$SUBNET.$cam_number"
    local rs=$(date +%s | md5sum | head -c 8)  # Random string for `rs` parameter
    local output_file="$SNAPSHOT_DIR/camera_snapshot_$(date +%Y%m%d%H%M%S)_cam${cam_number}.jpeg"
    local timeout=10  # Timeout in seconds
    local max_width=3840  # Replace with your camera's maximum width
    local max_height=2160  # Replace with your camera's maximum height
    local placeholder_image="./no_image.jpeg"  # Path to your placeholder image

    echo "Taking snapshot for Camera $cam_number at $cam_ip..." >&2
    curl -s --max-time "$timeout" -o "$output_file" \
        "http://$cam_ip/cgi-bin/api.cgi?cmd=Snap&channel=0&rs=$rs&user=admin&password=$CAMERA_PASSWORD&width=$max_width&height=$max_height"

    # Check if the file was created and is not empty
    if [[ -f "$output_file" && -s "$output_file" ]]; then
        # Validate the file type to ensure it's a JPEG
        if file "$output_file" | grep -q "JPEG image data"; then
            echo "$output_file"
        else
            echo "Warning: Snapshot for Camera $cam_number is not a valid JPEG. Using placeholder image instead." >&2
            cp "$placeholder_image" "$output_file"
            echo "$output_file"
        fi
    else
        echo "Warning: Snapshot for Camera $cam_number timed out or failed. Using placeholder image instead." >&2
        cp "$placeholder_image" "$output_file"
        echo "$output_file"
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

    if [[ -n "$snapshot_file" && -f "$snapshot_file" ]]; then
        upload_snapshot "$camera_number" "$snapshot_file"
    else
        echo "Error: Snapshot for Camera $camera_number was not created or could not be located."
    fi
done < <(grep -A 1000 '^Camera Number' "$CSV_FILE" | tail -n +2)

echo "Processing complete!"
