
# Hand Sign to Alphabets (OpenCV)

This project uses computer vision (OpenCV) to recognize hand signs and convert them into English alphabets (A–V), as well as backspace and space, by detecting the number of fingers shown in two regions of the camera feed. The detected character is automatically typed into Notepad (on Windows) using simulated keyboard input.

## Features

- Real-time hand sign detection using your webcam
- Converts finger counts into alphabets (A–V), space, and backspace
- Types the detected character directly into Notepad
- Visual feedback with bounding boxes and contours

## Limitations

- Only detects the number of fingers shown, not complex hand gestures
- Only supports alphabets A–V, space, and backspace
- Designed for Windows (uses Notepad and Windows-specific commands)

## Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- numpy
- pynput
- pyautogui

Install dependencies with:

```bash
pip install opencv-python numpy pynput pyautogui
```

## Usage

1. **Connect your webcam.**
2. **Run the script:**
   ```bash
   python Hand-sign-to-alphabets-OPENCV.py
   ```
3. **Enter the camera number** when prompted (usually `0` for the default webcam).
4. **Place your hands inside the two colored rectangles** shown on the video window.
5. **Show different numbers of fingers** in each box to type different letters. The corresponding character will be typed into Notepad automatically.
6. **Press `q` or `Esc` to exit.**

## How It Works

- The script draws two rectangles on the webcam feed for left and right hands.
- It counts the number of fingers detected in each region using contour and convexity defect analysis.
- Based on the combination of finger counts, it maps to a specific alphabet, space, or backspace.
- The character is typed into Notepad using the `pynput` library.

## Notes

- For best results, use a plain background and good lighting.
- The script is designed for Windows (uses Notepad and `TASKKILL`). For other OS, you may need to modify the code.

## License

This project is for educational purposes. Feel free to modify and use it as needed.
