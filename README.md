# AI Virtual Mouse using Hand Gestures

Control your computer's cursor using hand gestures in real-time. This project leverages the power of OpenCV and
MediaPipe to create a virtual mouse that responds to your hand movements, providing a touchless way to interact with
your screen.


---

## ✨ Features

- **Cursor Control**: Move the mouse pointer by raising your index finger.
- **Left Click**: Perform a click by pinching your thumb and index finger together.
- **Scrolling**: Scroll vertically by raising your index and middle fingers and moving your hand up or down.
- **Take Screenshot**: Capture your screen by pinching all your fingertips together.
- **Real-time Visual Feedback**: The camera feed displays your hand landmarks and visual cues for actions (e.g., green
  for movement, red for click, purple for scrolling).
- **Efficient & Optimized**: Written in an object-oriented structure for clean, readable, and efficient code.

---

## 🖐️ Gestures

The control system is simple and intuitive:

| Gesture | Action |
| :--- | :--- |
| **Raise Index Finger** 👍 | Move the mouse cursor. |
| **Pinch Thumb & Index** 👌 | Perform a left click. |
| **Raise Index & Middle** ✌️ | Scroll vertically up/down. |
| **Pinch all Fingers** ✊ | Take a screenshot (saved as `screenshot.png`). |

---

## 🛠️ Setup and Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

- Python 3.7+
- A webcam connected to your computer.

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/49mg/touchless-control-system.git](https://github.com/49mg/touchless-control-system.git)
   cd touchless-control-system
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # For Windows
   python -m venv venv
   venv\Scripts\activate

   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages:**
   All dependencies are listed in the `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
   ```
   > **Note for Linux users**: You may need to install a screenshot utility like `scrot`.
   > `sudo apt install scrot`

---

## 🚀 How to Run

Once the setup is complete, run the main script from your terminal:

```bash
python main.py
```

A window will open showing your webcam feed. Position your hand in the frame and start controlling the mouse. To stop
the program, press the **'q'** key.

---

## 📦 Dependencies

This project relies on the following major libraries:

- **OpenCV (`opencv-python`)**: For capturing and processing video from the webcam.
- **MediaPipe**: For high-fidelity hand and finger tracking.
- **PyAutoGUI**: For programmatically controlling the mouse and keyboard.

A full list of dependencies can be found in `requirements.txt`.

---

## 💡 Future Improvements

This project provides a solid foundation. Future enhancements could include:

-   [x] ~~Scrolling: Adding a gesture for vertical and horizontal scrolling.~~ (Done!)
-   [ ] **Right Click & Double Click**: Implementing new gestures for more mouse functions.
-   [ ] **Customizable Gestures**: Allowing users to define their own gestures for actions.
-   [ ] **GUI for Settings**: Creating a simple graphical interface to adjust sensitivity and other settings.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.