from PIL import Image, ImageDraw
import numpy as np


# Specifying the upload image function and verify its dimensions 
def upload_and_verify_image(image_path):
    img = Image.open(image_path)
    
    # Verify image size
    if img.size != (512, 512):
        raise ValueError("Error! Image size must be 512x512 pixels")
    
    return img


# Creating a mask that ensures only non transparent pixels are within a circular region
def circle_mask(size):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    return mask


# Apply the circle mask to the uploaded image
def apply_circle_mask(image, mask):
    result = Image.new("RGBA", image.size)
    result.paste(image, mask=mask)
    return result


# Colours that give a happy feeling
def happy_colours(image):
  
    # Get the pixel data as a numpy array
    pixels = np.array(image)

    # Apply colour adjustments
    red_multiplier = 1.2
    green_multiplier = 1.1
    blue_multiplier = 1.3

    pixels[:, :, 0] = pixels[:, :, 0] * red_multiplier
    pixels[:, :, 1] = pixels[:, :, 1] * green_multiplier
    pixels[:, :, 2] = pixels[:, :, 2] * blue_multiplier

    # Ensure pixel values are within [0, 255] range
    pixels = np.clip(pixels, 0, 255).astype(np.uint8)

    # Convert the numpy array back to an image
    adjusted_image = Image.fromarray(pixels, 'RGBA')

    return adjusted_image


# Convert the image to PNG format
def convert_to_png(image, output_path):
    image.save(output_path, "PNG")


# Applying all functions
def process_badge(input_path, output_path):
    try:
        # Upload and verify image
        img = upload_and_verify_image(input_path)
        
        # Create circle mask
        mask = circle_mask(img.size)
        
        # Apply circle mask
        img = apply_circle_mask(img, mask)
        
        # Adjust colours
        img = happy_colours(img)
        
        # Convert to PNG and save
        convert_to_png(img, output_path)
        
        print("Badge successfully processed!")
    except Exception as e:
        print("Error: ", str(e))

# Input & Output
input_image_path = "avatar-male.jpeg"
output_image_path = "processed_badge.png"
process_badge(input_image_path, output_image_path)