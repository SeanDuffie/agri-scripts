import os
import cv2
from time import sleep
if os.name.find("64"):
    from picamera2 import Picamera2, Preview        # For 64-bit OS
else:
    from picamera import PiCamera                   # For 32-bit OS

def acq_img(IMG_NAME:str,H:int,RAW_SIZE,IMG_SIZE,):
    """
    Temp Docstring
    """
    # If during inactive hours, do nothing
    if int(H) >= 7 or int(H) == 0:
        print("Starting Camera...\n")
        if os.name.find("64"):
            ## If 64 bit system
            picam2 = Picamera2()
            capture_config = picam2.create_still_configuration(main={"size": RAW_SIZE, "format": "RGB888"})
            picam2.start(config=capture_config)
            sleep(3) # wait for camera to focus

            ## Capture image and stop
            # metadata = picam2.capture_metadata()
            cur_img = picam2.capture_array()
            cur_img = cv2.resize(cur_img, IMG_SIZE)
        else:
            ## If 32 bit system
            with PiCamera() as camera:
                camera.start_preview()
                sleep(3) # wait for camera to focus

                ## Capture image and stop
                camera.capture(IMG_NAME)
                camera.stop_preview()

        ### Start Post Processing Current Image ###
        print("\nProcessing Image...")
        # Add Timestamp
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 255, 255)
        thickness = 2
        cv2.putText(cur_img, NAME, (50,50), font, fontScale, color, thickness, cv2.LINE_AA)

        # TODO: Append Sensor data somehow

        #### End Post Processing Current Image ####
        print("Picture Acquired!\n")
    else:
        print("Inactive hours\n")
    return cur_img