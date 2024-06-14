import os
import shutil
from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator
import multiprocessing
import winshell
from win32com.client import Dispatch

multiprocessing.freeze_support()

# Function to read paths from a text file
def read_paths_from_file(file_path):
    paths = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(' = ')
            paths[key.strip()] = value.strip().strip('"')
    return paths

# Function to confirm parameters with the user
def confirm_parameters(paths):
    print("Are these parameters correct?")
    print(f"model_path = {paths['model_path']}")
    print(f"input_dir = {paths['input_dir']}")
    print(f"output_dir = {paths['output_dir']}")
    confirmation = input("(y/n): ").lower()
    return confirmation == 'y'

# Function to create shortcut in Windows
def create_shortcut(target, shortcut):
    shell = Dispatch('WScript.Shell')
    shortcut_file = shell.CreateShortCut(shortcut)
    shortcut_file.TargetPath = target
    shortcut_file.save()

# Function to draw bounding boxes on images
def draw_bounding_boxes(image, results, names, shift_factor):
    annotator = Annotator(image)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            # Shifting the bounding box
            shift_x = int((b[2] - b[0]) * shift_factor)
            shift_y = int((b[3] - b[1]) * shift_factor)
            b_shifted = [b[0] + shift_x, b[1] + shift_y, b[2] + shift_x, b[3] + shift_y]
            annotator.box_label(b_shifted, names[int(c)])
    return annotator.result()


# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # Navigate one directory up

# Construct the path to paths.txt
paths_file_path = os.path.join(parent_dir, 'paths.txt')
print(paths_file_path)

# Read paths from the text file
paths = read_paths_from_file(paths_file_path)


# Confirm parameters with the user
if confirm_parameters(paths):
    # Initialize YOLO model with the provided model file
    model = YOLO(paths['model_path'])

    # Get class names from the model
    names = model.names

    # Input and output directories from the text file
    input_dir = paths['input_dir']
    output_dir = paths['output_dir']
    bounding_boxes = input("Do you want bounding boxes on predicted images? (y/n): ").lower()

    # Function to organize images based on predicted classes
    def organize_images(input_dir, output_dir):
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Iterate over images in the input directory
        for filename in os.listdir(input_dir):
            if filename.endswith(".jpg") or filename.endswith(".JPG"):
                image_path = os.path.join(input_dir, filename)
                print(f"Processing image: {image_path}")
                # Perform object detection on the image
                results = model.predict(image_path)

                # Create directories based on predicted classes and copy images
                for r in results:
                    # Find prediction with the highest confidence
                    max_confidence_index = r.boxes.conf.argmax()
                    max_confidence_class = names[int(r.boxes.cls[max_confidence_index])]
                    max_confidence = r.boxes.conf[max_confidence_index]

                    # Create directory for the prediction with highest confidence
                    max_confidence_dir = os.path.join(output_dir, max_confidence_class)
                    os.makedirs(max_confidence_dir, exist_ok=True)

                    # Copy image to the directory
                    output_image_path = os.path.join(max_confidence_dir, filename)
                    shutil.copy(image_path, output_image_path)
                    print(f"Image {filename} predicted as {max_confidence_class} with confidence {max_confidence}")

                    # Draw bounding boxes if user wants
                    # bounding_boxes = input("Do you want bounding boxes on predicted images? (y/n): ").lower()
                    if bounding_boxes == 'y':
                        # Adjust the shift_factor as needed
                        shift_factor = 0.5  # Example value, adjust as necessary
                        annotated_image = draw_bounding_boxes(cv2.imread(image_path), results, names, shift_factor)
                        cv2.imwrite(output_image_path, annotated_image)

                    # Create shortcut for predictions with lower confidence
                    for i, conf in enumerate(r.boxes.conf):
                        if i != max_confidence_index:
                            lower_confidence_class = names[int(r.boxes.cls[i])]
                            lower_confidence_dir = os.path.join(output_dir, lower_confidence_class)
                            os.makedirs(lower_confidence_dir, exist_ok=True)  # Ensure directory exists
                            if not os.path.exists(os.path.join(lower_confidence_dir, filename)):
                                create_shortcut(output_image_path, os.path.join(lower_confidence_dir, filename + ".lnk"))
                                print(f"Shortcut created for {filename} in {lower_confidence_class}")

    # Organize images based on predicted classes
    organize_images(input_dir, output_dir)

    input("PRESS ENTER TO EXIT...")
else:
    print("Execution aborted.")