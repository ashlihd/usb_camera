# Program to run the usb camera from python
# It has several feature such as brightness adjustment, autoexposure, resolution selection, save picture and record video.
# The program was generated from zero using gen AI, and finally adjusment manually
# By: Ashlih Dameitry
# Ver: 2026/04/21
# Tested usb camera:
# Sanwa Supply CMS-V53BK
# <more to add>

import cv2
import os
import time
from datetime import datetime

class CameraController:
    def __init__(self, cam_id=0, width=640, height=480):
        self.cam_id = cam_id
        self.width = width
        self.height = height

        self.cap = cv2.VideoCapture(self.cam_id, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open USB camera.")

        self.set_resolution(width, height)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Video recording
        self.recording = False
        self.video_writer = None

        # Warm-up
        for _ in range(5):
            self.cap.read()
            time.sleep(0.03)

        # Print initial values for debugging
        print("Initial brightness:", self.cap.get(cv2.CAP_PROP_BRIGHTNESS))
        print("Initial contrast:", self.cap.get(cv2.CAP_PROP_CONTRAST))
        print("Initial auto exposure:", self.cap.get(cv2.CAP_PROP_AUTO_EXPOSURE))
        print("Initial exposure:", self.cap.get(cv2.CAP_PROP_EXPOSURE))

    # -----------------------------
    # Camera Controls
    # -----------------------------
    def set_resolution(self, w, h):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

    def toggle_auto_exposure(self):
        """
        For DirectShow backend (Windows):
          - 0.25 ≈ auto exposure
          - 0.75 ≈ manual exposure
        """
        current = self.cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
        if current >= 0.5:
            # currently manual → switch to auto
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            print("Auto exposure: ON")
        else:
            # currently auto → switch to manual
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
            print("Auto exposure: OFF (manual)")

        print("AUTO_EXPOSURE now:", self.cap.get(cv2.CAP_PROP_AUTO_EXPOSURE))

    def set_exposure(self, value):
        # Ensure manual mode before setting exposure
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, float(value))
        print(f"Exposure set to {value}")
        print("AUTO_EXPOSURE now:", self.cap.get(cv2.CAP_PROP_AUTO_EXPOSURE))
        print("EXPOSURE now:", self.cap.get(cv2.CAP_PROP_EXPOSURE))

    def adjust_brightness(self, delta=5):
        cur = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        if cur < 0:
            cur = 128  # fallback default
        new = max(0, min(255, cur + delta))
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, new)
        print(f"Brightness: {new} (prev {cur})")

    def adjust_contrast(self, delta=5):
        cur = self.cap.get(cv2.CAP_PROP_CONTRAST)
        if cur < 0:
            cur = 128  # fallback default
        new = max(0, min(255, cur + delta))
        self.cap.set(cv2.CAP_PROP_CONTRAST, new)
        print(f"Contrast: {new} (prev {cur})")

    # -----------------------------
    # Capture
    # -----------------------------
    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame.")
        return frame

    # -----------------------------
    # Save Image
    # -----------------------------
    def save_image(self, frame):
        os.makedirs("captures", exist_ok=True)
        filename = datetime.now().strftime("captures/img_%Y%m%d_%H%M%S.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved image: {filename}")

    # -----------------------------
    # Video Recording
    # -----------------------------
    def start_recording(self):
        os.makedirs("videos", exist_ok=True)
        filename = datetime.now().strftime("videos/vid_%Y%m%d_%H%M%S.avi")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.video_writer = cv2.VideoWriter(filename, fourcc, 30.0, (self.width, self.height))
        self.recording = True
        print(f"Recording started: {filename}")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.video_writer.release()
            print("Recording stopped")

    # -----------------------------
    # Cleanup
    # -----------------------------
    def release(self):
        if self.recording:
            self.stop_recording()
        self.cap.release()
        cv2.destroyAllWindows()


# ----------------------------------------------------
# Main Program
# ----------------------------------------------------
def main():
    cam = CameraController(0, 640, 480)

    print("""
Keyboard Controls:
  b = brightness +5     n = brightness -5
  c = contrast +5       x = contrast -5
  r = change resolution (cycles)
  a = toggle auto exposure
  e = set manual exposure (numeric input)
  s = save image
  v = start/stop video recording
  q = quit
""")

    resolutions = [(640,480), (640,480), (800,600), (1280,720), (1280,960), (1920,1080)]
    res_index = 0

    while True:
        frame = cam.read()

        if cam.recording:
            cam.video_writer.write(frame)

        cv2.imshow("USB Camera Control", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        # Brightness
        if key == ord('b'):
            cam.adjust_brightness(+5)
        if key == ord('n'):
            cam.adjust_brightness(-5)

        # Contrast
        if key == ord('c'):
            cam.adjust_contrast(+5)
        if key == ord('x'):
            cam.adjust_contrast(-5)

        # Resolution cycle
        if key == ord('r'):
            res_index = (res_index + 1) % len(resolutions)
            w, h = resolutions[res_index]
            cam.set_resolution(w, h)
            cam.width, cam.height = w, h
            print(f"Resolution set to {w}x{h}")

        # Auto exposure toggle
        if key == ord('a'):
            cam.toggle_auto_exposure()

        # Manual exposure input
        if key == ord('e'):
            val = input("Enter exposure value (try around -6 to -2, depending on camera): ")
            try:
                cam.set_exposure(float(val))
            except ValueError:
                print("Invalid exposure value")

        # Save image
        if key == ord('s'):
            cam.save_image(frame)

        # Video recording toggle
        if key == ord('v'):
            if cam.recording:
                cam.stop_recording()
            else:
                cam.start_recording()

    cam.release()


if __name__ == "__main__":
    main()
