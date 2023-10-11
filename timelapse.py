"""_summary_
"""
import os

import cv2

RTDIR = os.getcwd()
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')

def gen_timelapse(img_dir, vid_path, fps, img_res):
    # Read in current directory of images
    print("Reading in Images...")
    images = [img for img in os.listdir(img_dir) if img.endswith(".jpg")]
    print(images)
    images.sort()
    # Compile image array into a video
    print("Compiling video...", vid_path)
    vid_writer = cv2.VideoWriter(vid_path, FOURCC, fps, img_res)
    for filename in images:
        img = cv2.imread(img_dir + filename)  # Read in Raw image
        vid_writer.write(img)              # writes out each frame to the video file
    vid_writer.release()
    print("Time-Lapse Released!\n")

if __name__ == "__main__":# Define Path names
    RTDIR = os.getcwd()
    IMGDIR = RTDIR + "/autocaps/"
    OUTDAT = RTDIR + "/data/"
    VID_DIR = RTDIR + "/Flask/static"

    # If autocaps or data don't exist, create them! They are gitignored...
    if not os.path.exists(IMGDIR):
        os.makedirs(IMGDIR)
    if not os.path.exists(OUTDAT):
        os.makedirs(OUTDAT)

    VID_NAME = f"{VID_DIR}/time-lapse.mp4"      # video name
    FOURCC = cv2.VideoWriter_fourcc(*'mp4v')    # video format
    FPS = 24                                    # video fps
    RAW_SIZE = (3280, 2465)                     # camera resolution
    IMG_SIZE = (1920, 1080)                     # video resolution

    gen_timelapse(img_dir=IMGDIR, vid_path=VID_NAME, fps=FPS, img_res=IMG_SIZE)