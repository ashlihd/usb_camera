# usb_camera with python

## Overview

- Run the usb camera on windown terminal
- Tune the camera brightness, contrast, toggle auto exposure, and resolution
- Save the picture or record the video

## Compatible camera

- Sanwa supply CMS-V53BK

I haven't try other camera, but most usb camera might be usable.

## Usage example

```
Check your camera available resolution
C:\[your file location]>python camera_test_res_check.py

After you know what resolution is allowed in your camera,
modify the camera_test_usbcam.py program and change the resolution of the camera
then save it.

Run the program
C:\[your file location]>python camera_test_usbcam.py

Adjust the brightness, contrast, etc.
Make sure that active windows is selecting the camera windows,
So that the keyboard input can be read.

To quit the program, press q on camera windows
or ctrl+c in your terminal windows.
```

## Feedback

Please kindly send your feedback/comments. Thank you!
