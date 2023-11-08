import cv2
import numpy as np
import random 


#Codes of Nguyễn Trọng Khoa

#Creat fuction to crop the image
def crop_image(img):
    # Randomly crops the input image.
    min_size_ratio = random.uniform(0.1, 0.5)
    h, w, _ = img.shape
    #Caculate the minium size
    min_width = int(w * min_size_ratio)
    min_height = int(h * min_size_ratio)
    #Make random size
    random_width = np.random.randint(min_width, w)
    random_height = np.random.randint(min_height, h)
    #Choose random cutting position
    left = np.random.randint(0, w - random_width)
    upper = np.random.randint(0, h - random_height)
    right = left + random_width
    #Crop the image
    lower = upper + random_height
    cropped = img[upper:lower, left:right]

    return cropped

def rotate_image(img):
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    #Make random rotation
    angle = random.uniform(-360, 360)
    #Create rotation transformation matrix (M) 
    #The center of rotation is the center of the image,
    #the angle is the angle just created, and the scale is 1.0 (no scaling).
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    #Perform image rotation
    rotated = cv2.warpAffine(img, M, (w, h))

    return rotated

#Codes of Đỗ Quỳnh Nga

#Create fuction to change color of the image
def change_color(img):
    #Convert color
    choice = random.choice([cv2.COLOR_BGR2GRAY, cv2.COLOR_BGR2HSV, cv2.COLOR_BGR2RGB])

    img = cv2.cvtColor(img, choice)

    return img

#Create fuction to change the brightness
def change_brightness(img):
    #Generate a random brightness value
    brightness = random.randint(-100, 100)
    #Change brightness
    if brightness > 0:
        matrix = np.ones(img.shape, dtype="uint8") * brightness
        brightened_image = cv2.add(img, matrix)
    else:
        matrix = np.ones(img.shape, dtype="uint8") * -brightness
        darkened_image = cv2.subtract(img, matrix)

    if brightness > 0:
        return brightened_image
    else:
        return darkened_image

#Creat fuction to draw edge of the image
def edge_detection(img):
    #Convert the image to a grayscale image using the argument 0
    edges = cv2.Canny(img, random.randint(10, 100), random.randint(50, 150))
    return edges

#Codes of Cao Ngọc Ý

#Create function to resize the image
def resize_image(img):
    #Randomly select a resizing ratio
    scale = random.uniform(0.1, 2.5)
    #Resize images
    new_width = int(img.shape[1] * scale)
    new_height = int(img.shape[0] * scale)

    resized_image = cv2.resize(img, (new_width, new_height))

    return resized_image

def adjust_contrast(image):
    #Randomly generate `alpha` and `beta` coefficients
    alpha = np.random.uniform(0.5, 2.5)
    beta = np.random.uniform(0.5, 2.5)
    #Apply contrast transformation using `cv2.convertScaleAbs`.
    adjusted_image = cv2.convertScaleAbs(image, alpha, beta)
    return adjusted_image

#Codes of Nguyễn Tấn Thắng

#Create fuction to Optimal function selected by the user
def process_image(input_path, options):
    img = cv2.imread(input_path)

    for option in options:
        if option == 'crop':
            img = crop_image(img)
        elif option == 'bright':
            img = change_brightness(img)
        elif option == 'contrast':
            img = adjust_contrast(img)
        elif option == 'resize':
            img = resize_image(img)
        elif option == 'color':
            img = change_color(img)
        elif option == 'rotate':
            img = rotate_image(img)
        elif option == 'edge detection':
            img = edge_detection(img)

    return img