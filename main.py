import math
import cv2
import mediapipe as mp
import pyautogui

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
MIN_DETECTION_CONFIDENCE = 0.8
MIN_TRACKING_CONFIDENCE = 0.5
CLICK_DISTANCE_THRESHOLD = 0.05
SCREENSHOT_DISTANCE_THRESHOLD = 0.07
SCROLL_SENSITIVITY = 30

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


class VirtualMouse:
    """
    A class to handle virtual mouse functionalities based on hand gestures.
    """

    def __init__(self):
        """
        Initializes the VirtualMouse object.
        Sets up screen dimensions and initial state flags for actions like
        clicking and scrolling.
        """
        self.screen_width, self.screen_height = pyautogui.size()
        self.is_clicking = False
        self.is_take_screenshot = False
        self.is_scrolling = False
        self.last_y = 0

    def move(self, index_tip):
        """
        Moves the mouse cursor across the screen.

        Maps the index finger's coordinates from the camera frame to the
        screen resolution and moves the cursor to that position.

        Args:
            index_tip: The landmark corresponding to the tip of the index finger.
        """
        screen_x = int(self._map_value(index_tip.x, 0, 1, 0, self.screen_width))
        screen_y = int(self._map_value(index_tip.y, 0, 1, 0, self.screen_height))
        pyautogui.moveTo(screen_x, screen_y)

    def click(self, image, index_tip):
        """
        Performs a single left-click action.

        Uses a state flag `is_clicking` to prevent continuous clicks.
        Draws a red circle on the image for visual feedback.

        Args:
            image: The camera frame to draw on.
            index_tip: The landmark for the index finger tip.
        """
        if not self.is_clicking:
            pyautogui.click()
            self.is_clicking = True
        x = int(index_tip.x * CAMERA_WIDTH)
        y = int(index_tip.y * CAMERA_HEIGHT)
        cv2.circle(image, (x, y), 15, (0, 0, 255), -1)

    def take_screenshot(self):
        """
        Captures a screenshot of the entire screen.

        Saves the image as 'screenshot.png' in the root directory. Uses a
        state flag to ensure only one screenshot is taken per gesture.
        """
        if not self.is_take_screenshot:
            self.is_take_screenshot = True
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            print("Screenshot saved as screenshot.png")

    def scroll(self, hand_landmarks):
        """
        Handles the vertical scrolling action.

        Tracks the vertical movement of the hand (wrist) to scroll up or down.
        A sensitivity threshold prevents accidental scrolls from minor movements.

        Args:
            hand_landmarks: The detected landmarks for the entire hand.
        """
        current_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * CAMERA_HEIGHT
        if not self.is_scrolling:
            self.is_scrolling = True
            self.last_y = current_y
            return
        delta_y = current_y - self.last_y
        if abs(delta_y) > SCROLL_SENSITIVITY:
            if delta_y > 0:
                pyautogui.scroll(-1)
            else:
                pyautogui.scroll(1)
            self.last_y = current_y

    def update(self, image, hand_landmarks):
        """
        The main control hub that processes hand landmarks in each frame.

        It analyzes the hand's posture to detect gestures for moving, clicking,
        scrolling, or taking a screenshot, then calls the appropriate method.

        Args:
            image: The current camera frame.
            hand_landmarks: The detected landmarks for the hand.
        """
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_FINGER_TIP]
        index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
        middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
        ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
        pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_FINGER_MCP]

        dist_index = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)
        dist_middle = math.hypot(middle_tip.x - thumb_tip.x, middle_tip.y - thumb_tip.y)
        dist_ring = math.hypot(ring_tip.x - thumb_tip.x, ring_tip.y - thumb_tip.y)
        dist_pinky = math.hypot(pinky_tip.x - thumb_tip.x, pinky_tip.y - thumb_tip.y)

        is_index_up = index_tip.y < index_pip.y
        is_middle_up = middle_tip.y < middle_pip.y
        is_ring_down = ring_tip.y > ring_mcp.y
        is_pinky_down = pinky_tip.y > pinky_mcp.y

        if (dist_index < SCREENSHOT_DISTANCE_THRESHOLD and
                dist_middle < SCREENSHOT_DISTANCE_THRESHOLD and
                dist_ring < SCREENSHOT_DISTANCE_THRESHOLD and
                dist_pinky < SCREENSHOT_DISTANCE_THRESHOLD):
            self.take_screenshot()
            x = int(thumb_tip.x * CAMERA_WIDTH);
            y = int(thumb_tip.y * CAMERA_HEIGHT)
            cv2.circle(image, (x, y), 15, (255, 0, 0), -1)
            self.is_scrolling = False
        elif is_index_up and is_middle_up and is_ring_down and is_pinky_down:
            self.scroll(hand_landmarks)
            x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * CAMERA_WIDTH)
            y = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * CAMERA_HEIGHT)
            cv2.circle(image, (x, y), 15, (255, 0, 255), -1)
        elif dist_index < CLICK_DISTANCE_THRESHOLD:
            self.click(image, index_tip)
            self.is_scrolling = False
        elif index_tip.y < middle_tip.y:
            self.move(index_tip)
            x = int(index_tip.x * CAMERA_WIDTH);
            y = int(index_tip.y * CAMERA_HEIGHT)
            cv2.circle(image, (x, y), 15, (0, 255, 0), -1)
            self.is_scrolling = False
        else:
            # Reset all flags when no gesture is detected
            self.is_clicking = False
            self.is_take_screenshot = False
            self.is_scrolling = False

    def _map_value(self, value, in_min, in_max, out_min, out_max):
        """
        A helper utility to map a value from one range to another.

        Used to convert normalized camera coordinates (0 to 1) to
        screen pixel coordinates (e.g., 0 to 1920).
        """
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def main():
    """
    The main function that initializes and runs the application.

    It sets up the video capture, creates the VirtualMouse instance, and runs
    the main loop to process camera frames until the user presses 'q' to quit.
    """

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    mouse = VirtualMouse()

    with mp_hands.Hands(min_detection_confidence=MIN_DETECTION_CONFIDENCE,
                        min_tracking_confidence=MIN_TRACKING_CONFIDENCE) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Ignoring empty camera frame.")
                continue

            frame = cv2.flip(frame, 1)

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mouse.update(image, hand_landmarks)
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.imshow('Virtual Mouse - Press "q" to exit', image)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
