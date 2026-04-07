import cv2

def take_photo(filename='photo.jpg'):
    # 0 is usually the default built-in webcam on a laptop. 
    # If you have an external USB camera, you might need to change this to 1 or 2.
    cap = cv2.VideoCapture(0)

    # Professional safety check: Did the camera actually turn on?
    if not cap.isOpened():
        print("❌ ERROR: Could not open the webcam.")
        print("Mac Users: Make sure VS Code or your Terminal has 'Camera' permissions in System Settings!")
        return None

    print("📷 Webcam is active!")
    print("👉 Press the 'SPACEBAR' to take a photo.")
    print("👉 Press 'ESC' to cancel and close.")

    while True:
        # Read the current frame from the camera
        ret, frame = cap.read()
        
        if not ret:
            print("❌ ERROR: Failed to grab a frame from the camera.")
            break

        # Display the live feed in a window
        cv2.imshow("Webcam Feed - Press SPACE to Capture", frame)

        # Wait for a key press (refreshes every 1 millisecond)
        key = cv2.waitKey(1)

        # Logic for key presses
        if key % 256 == 27:
            # ESC pressed
            print("Escape hit, closing without saving...")
            break
        elif key % 256 == 32:
            # SPACE pressed
            cv2.imwrite(filename, frame)
            print(f"✅ Success! Photo saved to your folder as '{filename}'")
            break

    # Clean up: Release the camera hardware and close the window
    cap.release()
    cv2.destroyAllWindows()
    
    # We must call cv2.waitKey(1) one last time on Macs to force the window to actually close
    cv2.waitKey(1) 
    
    return filename