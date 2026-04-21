# Check the usb camera's resolution and fps.
# print out the result
# please use the output as the parameter to the main program

import cv2
import time

# ---------------------------------------------------------
# Measure FPS at the CURRENT resolution
# ---------------------------------------------------------
def measure_fps(cap, num_frames=120):
    # Warm-up
    for _ in range(10):
        cap.read()

    start = time.time()
    count = 0

    while count < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1

    end = time.time()
    elapsed = end - start

    if elapsed <= 0:
        return 0.0

    return count / elapsed


# ---------------------------------------------------------
# Test resolutions + FPS
# ---------------------------------------------------------
def test_camera_modes(cam_id=0):
    test_sizes = [
        (160, 120),
        (320, 240),
        (640, 480),
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1280, 960),
        (1600, 1200),
        (1920, 1080),
        (2560, 1440),
        (3840, 2160),
    ]

    cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Camera not found")
        return

    results = []

    print("\n=== Checking Supported Resolutions and FPS ===\n")

    for w, h in test_sizes:
        # Try setting resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

        # Read back actual resolution
        actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if actual_w == w and actual_h == h:
            print(f"✔ Supported: {w} x {h} — measuring FPS...")
            fps = measure_fps(cap)
            results.append((w, h, fps))
        else:
            print(f"✘ Not supported: {w} x {h} (camera returned {actual_w} x {actual_h})")

    cap.release()

    # ---------------------------------------------------------
    # Print summary table
    # ---------------------------------------------------------
    print("\n=== Summary: Supported Resolutions + Actual FPS ===\n")
    print(f"{'Resolution':<15} {'FPS':>8}")
    print("-" * 25)

    for w, h, fps in results:
        print(f"{w}x{h:<10} {fps:>8.2f}")

    print("\nDone.\n")


if __name__ == "__main__":
    test_camera_modes(0)
