# Import necessary libraries
import cv2
import mediapipe as mp
import pyautogui

# Set up the video capture using the default camera (camera index 0)
cap = cv2.VideoCapture(0)

# Initialize the hand detection module from Mediapipe
hand_detector = mp.solutions.hands.Hands(
    static_image_mode=False, 
    model_complexity=1,
    min_detection_confidence=0.75, 
    min_tracking_confidence=0.75, 
    max_num_hands=1
)

# Import the drawing utilities from Mediapipe
drawing_utils = mp.solutions.drawing_utils

# Get the screen width and height using PyAutoGUI
screen_width, screen_height = pyautogui.size()

# Initialize the initial index finger y-coordinate
index_y = 0
# Main loop for capturing video frames
while True:
    # Read a frame from the camera
    _, frame = cap.read()

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Get the height, width, and channels of the frame
    frame_height, frame_width, _ = frame.shape

    # Convert the BGR frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame using the hand detection module
    output = hand_detector.process(rgb_frame)

    # Get the detected hand landmarks
    hands = output.multi_hand_landmarks

    # Check if hands are detected
    if hands:
        # Loop over each detected hand
        for hand in hands:
            # Draw landmarks on the frame
            drawing_utils.draw_landmarks(frame, hand)

            # Get the landmarks of the hand
            landmarks = hand.landmark

            # Loop over each landmark
            for id, landmark in enumerate(landmarks):
                # Get the x and y coordinates of the landmark
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # Check if the landmark is the index finger tip (id == 8)
                if id == 8:
                    # Draw a circle around the index finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))

                    # Convert the coordinates to screen coordinates
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                    # Move the cursor to the index finger tip position
                    pyautogui.moveTo(index_x, index_y)

                # Check if the landmark is the thumb tip (id == 4)
                if id == 4:
                    # Draw a circle around the thumb tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))

                    # Convert the coordinates to screen coordinates
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    # Check the vertical distance between index and thumb
                    if abs(index_y - thumb_y) < 60:
                        # Perform a single click if the distance is small
                        pyautogui.click()
                        print('click')
                        pyautogui.sleep(1)

                # Check if the landmark is the middle finger tip (id == 12)
                if id == 12:
                    # Draw a circle around the middle finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 120, 255))

                    # Convert the coordinates to screen coordinates
                    mid_x = screen_width / frame_width * x
                    mid_y = screen_height / frame_height * y

                    # Check the vertical distance between index and middle finger
                    if abs(index_y - mid_y) < 60:
                        # # scroll down 10 "clicks"
                        pyautogui.scroll(10)
                        print('Scroll Up')
                        pyautogui.sleep(0.5)
                if id == 5:
                    # Get the coordinates of the root of the index finger
                    indroot_x = screen_width / frame_width * x
                    indroot_y = screen_height / frame_height * y

                    # Calculate the vertical distance between tip and root
                    distance = index_y - indroot_y

                    # Scroll down if index tip is below the root
                    if distance > 0:
                        pyautogui.scroll(-10)
                        print('Scroll Down')
    # Display the frame in the OpenCV window
    cv2.imshow('googoogaga', frame)
    cv2.setWindowProperty('googoogaga', cv2.WND_PROP_TOPMOST, 1)
    # Check for the 'Esc' key to exit the loop
    if cv2.waitKey(1) == 27:
        break

# Release the video capture object and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
