import os

img_dir = "../autocaps"
images = [img for img in os.listdir(img_dir) if img.endswith(".jpg") and ":00" in img]
print(images)
print(len(images))

for im in images:
    mod_name = im.replace(":00", "h")
    os.rename(f"{img_dir}/{im}", f"{img_dir}/{mod_name}")
