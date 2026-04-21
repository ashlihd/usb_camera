import cv2
import time

class StableUSBCamera:
    def __init__(self, camera_id=0, width=1280, height=720):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            raise RuntimeError("Failed to open USB camera.")

        # Set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Reduce buffering (helps stability)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Optional: disable auto exposure (some cameras freeze with auto)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

        # Warm-up frames
        for _ in range(5):
            self.cap.read()
            time.sleep(0.03)

    def set_brightness(self, value):
        """
        Adjust brightness of the camera.
        value: float (0.0 to 1.0) depending on camera driver support
        """
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def read_frame(self):
        """Read a single frame from the camera."""
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame from camera.")
        return frame

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()


def main():
    cam = StableUSBCamera(camera_id=0)

    cam.set_brightness(50)

    while True:
        frame = cam.read_frame()
        cv2.imshow("Stable USB Camera (No Threading)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()


if __name__ == "__main__":
    main()
