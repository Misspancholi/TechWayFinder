import os 
import random

# List all files in the folder (ensure they are images)
image_files = [f for f in os.listdir('captcha') if f.endswith(('png',))] 
captcha_image = random.choice(image_files)

print(captcha_image)
captcha_image = "captcha/" + captcha_image
image= open(captcha_image, "rb")
print(image)