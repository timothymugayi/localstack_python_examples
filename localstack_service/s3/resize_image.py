import os
import boto3
from PIL import Image

# Directory for temporary image storage
TEMP_DIR = "temp"
RESIZED_DIR = f"{TEMP_DIR}/resized"

# Ensure directories exist
os.makedirs(RESIZED_DIR, exist_ok=True)


# AWS S3 Configuration
AWS_ACCESS_KEY = "test"  # Replace with your AWS Access Key
AWS_SECRET_KEY = "test"  # Replace with your AWS Secret Key
AWS_REGION = "us-east-1"          # e.g., "us-west-2"
S3_BUCKET_NAME = "my-test-bucket" # Replace with your bucket name

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

def save_resized_images(image_path, resize_path, size):
    """
    Resize images to the specified sizes and save them in the resized directory.
    large emduin and m
    :param image_path: Path of the input image to resize.
    :param resize_path_template: Template for saving resized images (with placeholders).
    :param sizes: Dictionary of sizes to resize images to.
    :return: List of paths to resized images.
    """
    
    size_map = {
    "large": (1024, 1024),
    "medium": (512, 512),
    "small": (256, 256),
    }

    if not os.path.isfile(image_path):
        print(f"File '{image_path}' does not exist.")
        return []


    # Open the uploaded image
    # Open the uploaded image
    with Image.open(image_path) as image:
        # Resize image while maintaining aspect ratio
        image.thumbnail(size_map[size])
        
        # Determine the format of the original image
        image_format = image.format or 'JPEG'  # Default to 'JPEG' if format is not set
        
        # Save the resized image
        image.save(resize_path, format=image_format)
        print(f"Saved resized image: {resize_path}")
 

def upload_to_s3(file_path, s3_key):
    """
    Upload a file to an S3 bucket.
    
    :param file_path: Local file path to upload.
    :param s3_key: Key (path) in the S3 bucket.
    """
    try:
        s3_client.upload_file(file_path, S3_BUCKET_NAME, s3_key)
        print(f"Uploaded {file_path} to S3 bucket {S3_BUCKET_NAME} as {s3_key}")
    except Exception as e:
        print(f"Error uploading {file_path} to S3: {e}")

def process_and_upload_image(filename):
    """
    Process an image: resize it to multiple sizes and upload the resized images to S3.
    
    :param filename: Name of the image file to process.
    """
    image_path = f"{TEMP_DIR}/{filename}"
    resize_path_template = f"{RESIZED_DIR}/resized-{{size}}-{filename}"
    
    sizes = ['large', 'medium', 'small']  # Sizes to generate
    
    for size in sizes:
    # Resize the images
        resized_path = resize_path_template.format(size=size)
        save_resized_images(image_path, resized_path, size)
        
        s3_client.upload_file(
            resized_path,
            S3_BUCKET_NAME,
            f'product_images/{size}/{filename}'
        )

# Example usage: process and upload an image
uploaded_filename = "initial.jpg"  # Replace with the actual filename
process_and_upload_image(uploaded_filename)
