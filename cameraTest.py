import cv2

# RTSP URL of the Reolink camera
url = "rtsp://admin:cuhyperloop1!@10.0.0.212:554/h264Preview_01_main"


cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame from BGR to RGB (OpenCV uses BGR by default)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Example: Get RGB values of a specific pixel (e.g., at position (100, 200))
    x, y = 100, 200
    r, g, b = frame_rgb[y, x]
    print(f"RGB values at ({x}, {y}): Red={r}, Green={g}, Blue={b}")
    
    # Display the frame (for testing)
    cv2.imshow("Reolink Stream", frame)

    # Press 'q' to quit the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()