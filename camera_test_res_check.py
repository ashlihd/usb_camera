import cv2

def check_resolutions(cam_id=0):
    # Common USB camera resolutions
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

    print("\nChecking supported resolutions...\n")

    supported = []

    for w, h in test_sizes:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

        # Read back what the camera actually set
        actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if actual_w == w and actual_h == h:
            print(f"✔ Supported: {w} x {h}")
            supported.append((w, h))
        else:
            print(f"✘ Not supported: {w} x {h} (got {actual_w} x {actual_h})")

    cap.release()

    print("\nSummary:")
    if supported:
        for s in supported:
            print(f"  - {s[0]} x {s[1]}")
    else:
        print("  No tested resolutions supported.")

    print("\nDone.\n")


if __name__ == "__main__":
    check_resolutions(0)
