# 🔦 Real-Time Bright Spot Detection (Active Headlights Emulator)

This Python + OpenCV project simulates how adaptive headlights decide to dim when they detect oncoming cars using no deep learning, just slicing and adaptive thresholding. The system processes webcam video, detects bright spots below a certain horizon line (e.g. where headlights appear), and dynamically draws bounding boxes around them.

## ✨ Features
- 📸 Real-time webcam processing
- 🧠 Adaptive thresholding using mean + k × std deviation
- 📦 Frame slicing to process regions independently
- 🚫 Streetlamp exclusion line (ignores top of the image)
- 🟩 Green bounding boxes for detected bright slices
- ⏱️ Real-time logging of bright spot timestamps
- 🧪 Minimal dependencies, fast setup, and runs on CPU

## 📹 Demo
A live demo showing a phone flashlight being detected in real time will be shown here.

- ![Demo](images/ActiveHeadlightsDemo_1.gif)

## 🧰 How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/baileyarzate/active-headlights.git
    cd active-headlights
    ```
2.  **Create and activate a fresh environment (optional):**

3.  **Install requirements:**
    Make sure you have Python 3 installed. Then, install the required libraries from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```
    Press 'q' to quit the application.

## 🧠 How It Works
- Converts frame to grayscale → normalizes → light blur
- Slices image into vertical segments (user-defined density)
- Ignores top pixels (avoids false positives from ceiling/streetlights)
- Calculates adaptive threshold from remaining frame
- Flags slices above threshold as bright spots
- Recalculates threshold dynamically if many slices are very bright (robust to outliers)

## 🤖 Why No Deep Learning?
I could’ve used YOLO or fine-tuned a detection model, but:
- I didn’t have labeled data
- I didn’t have a GPU
- I did have a working brain, a webcam, and some time 😄
This is a reminder that traditional computer vision can still go a long way.

## 🐛 Known Bug(s)
- When given two light sources on the ends of the image, it detects only one most of the time. 

## 🚘 Origin Story
While driving my Tesla to the airport with my wife being sleep-deprived and observant, we noticed how the high beams intelligently turned off sections in certain conditions. We discussed whether Tesla used deep learning or traditional computer vision to handle this.

With no labeled data, limited compute, and curiosity burning, I prototyped this traditional CV approach using dynamic thresholding, no ML required.

## 📣 Connect
Built by Jesse Arzate: data scientist, applied mathematician, and engineer as a civil servant for the U.S. Air Force. Passionate about real-time AI systems, signal processing, and solving fun problems that matter.
