from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import matplotlib.pyplot as plt

def adjust_image(image_path):
    image = Image.open(image_path)
    
    bc_ratio = 5/3 
    
    # Convert image to grayscale to calculate metrics
    gray_image = image.convert('L')
    image_array = np.array(gray_image)

    # Calculate current metrics
    current_brightness = np.mean(image_array)
    current_contrast = np.std(image_array)
    
    # Calculate correct brightness/contrast ratio
    list = [current_brightness, current_contrast]
    bc_compare = np.std(list)
    bc_list = [-1/6, -1/3, -2/3, -5/6, 0, 5/6, 2/3, 1/3, 1/6]
    bc_index = 4
    try:
        bc_ratio += bc_list[bc_index + int((round(bc_compare) - 20) / 5)]
    except(IndexError):
        print("Brightness/Contrast ratio is absurd\n")
    
    print(round(bc_compare), bc_ratio)
    print(current_brightness)
    print(current_contrast)
    
    # Calculate target brightness based on the desired ratio
    target_brightness = bc_ratio * current_contrast

    # Calculate brightness adjustment factor
    brightness_adjustment = target_brightness / current_brightness
    brightness_enhancer = ImageEnhance.Brightness(image)
    adjusted_image = brightness_enhancer.enhance(brightness_adjustment)

    # Calculate target contrast based on the desired ratio
    target_contrast = target_brightness / bc_ratio
    
    # Calculate contrast adjustment factor
    contrast_adjustment = target_contrast / current_contrast
    contrast_enhancer = ImageEnhance.Contrast(adjusted_image)
    adjusted_image = contrast_enhancer.enhance(contrast_adjustment)

    # Calculate sharpness using the FIND_EDGES filter for adjustment
    laplacian = adjusted_image.filter(ImageFilter.FIND_EDGES)
    laplacian_array = np.array(laplacian)
    current_sharpness = laplacian_array.var()
    print(current_sharpness)

    # Calculate sharpness adjustment factor
    list = [current_brightness, current_contrast, current_sharpness]
    diff = np.std(list)
    print(diff)
    target_sharpness = 5
    increment = 0
    while diff > 0:
        decrease = (-20 / (increment + 4)) + target_sharpness
        increment += 1
        diff -= (current_brightness + current_contrast)
    print(decrease)
    decrease = round(decrease, 2)
    sharpness_adjustment = 3#target_sharpness - decrease ############################### fix
    print(sharpness_adjustment)
    sharpness_enhancer = ImageEnhance.Sharpness(adjusted_image)
    adjusted_image = sharpness_enhancer.enhance(sharpness_adjustment)

    return(adjusted_image)

image_path = (r"C:\Users\arnav\Downloads\ALC-bottles.jpg") ################################################
original_image = Image.open(image_path)
adjusted_image = adjust_image(image_path)

fig, axes = plt.subplots(1, 2, figsize=(15, 5))
axes[0].imshow(original_image)
axes[0].set_title('Original Image')
axes[0].axis('off')

axes[1].imshow(adjusted_image)
axes[1].set_title('Adjusted Image')
axes[1].axis('off')

plt.tight_layout()
plt.show()







'''import tkinter as tk
from PIL import Image, ImageEnhance, ImageTk

def update_image(brightness, contrast, sharpness):
    global img_display, image_label

    brightness_enhancer = ImageEnhance.Brightness(original_image)
    bright_image = brightness_enhancer.enhance(brightness)
    
    contrast_enhancer = ImageEnhance.Contrast(bright_image)
    contrast_image = contrast_enhancer.enhance(contrast)
    
    sharpness_enhancer = ImageEnhance.Sharpness(contrast_image)
    sharp_image = sharpness_enhancer.enhance(sharpness)
    
    resized_image = sharp_image.resize((resized_width, resized_height), Image.LANCZOS)
    
    img_display = ImageTk.PhotoImage(resized_image)
    image_label.config(image=img_display)

def on_brightness_change(val):
    brightness = float(val)
    contrast = contrast_slider.get()
    sharpness = sharpness_slider.get()
    update_image(brightness, contrast, sharpness)

def on_contrast_change(val):
    brightness = brightness_slider.get()
    contrast = float(val)
    sharpness = sharpness_slider.get()
    update_image(brightness, contrast, sharpness)

def on_sharpness_change(val):
    brightness = brightness_slider.get()
    contrast = contrast_slider.get()
    sharpness = float(val)
    update_image(brightness, contrast, sharpness)

root = tk.Tk()
root.title("Image Enhancer")

#
original_image = Image.open(image_path)

# RESIZING ******
resized_width, resized_height = original_image.size[0] // 3, original_image.size[1] // 3
resized_image = original_image.resize((resized_width, resized_height), Image.LANCZOS)
img_display = ImageTk.PhotoImage(resized_image)

image_label = tk.Label(root, image=img_display)
image_label.pack()

brightness_slider = tk.Scale(root, from_=0.0, to=2.0, resolution=0.1, orient='horizontal', label='Brightness', command=on_brightness_change)
brightness_slider.set(1.0)
brightness_slider.pack()

contrast_slider = tk.Scale(root, from_=0.0, to=2.0, resolution=0.1, orient='horizontal', label='Contrast', command=on_contrast_change)
contrast_slider.set(1.0)
contrast_slider.pack()

sharpness_slider = tk.Scale(root, from_=0.0, to=10.0, resolution=0.1, orient='horizontal', label='Sharpness', command=on_sharpness_change)
sharpness_slider.set(1.0)
sharpness_slider.pack()

root.mainloop()'''