import numpy as np
import cv2
from multiprocessing.pool import ThreadPool
from collections import deque
from dbr import *
import multiprocessing
import xml.etree.ElementTree as ET

# --- IMPORTANT: REPLACE WITH YOUR LICENSE KEY ---
LICENSE_KEY = 't0083YQEAAKqisPaOrLvM0tGYIFZd04VlwkQPvSCAZ4R2+kDWpFzDsEKVbxLkbhN4noJKQL+E0fMaU/Pmjx9bxkBIbeFwualmfM803jOjFTODC/izSGg=;t0082YQEAAEOa7iWLgmj5HwcSP7J0uNaMQ/kZ/x8HgwPBUpUE8rgwZj8s7nrHomUArjOIL611KRz1gqlYYYTZ98clI+D2lvWM75vifTOySIIddlJJAg==;t0082YQEAAA/YSn4DjmzJcu2C2qrVkNFVQ3pbrfwAi+IqrxbxV31mVURD6/IhsMOj+eYszSaE4PXkcuJ0GyOjRmygD4xAkHAZ3zfF+2bULAkOfcdJCQ=='

BarcodeReader.init_license(LICENSE_KEY)

reader = BarcodeReader()
settings = reader.get_runtime_settings()
settings.expected_barcodes_count = 2

settings.grayscale_transformation_modes = [
    EnumGrayscaleTransformationMode.GTM_INVERTED,
    EnumGrayscaleTransformationMode.GTM_ORIGINAL,
    EnumGrayscaleTransformationMode.GTM_SKIP,
    EnumGrayscaleTransformationMode.GTM_SKIP,
    EnumGrayscaleTransformationMode.GTM_SKIP,
    EnumGrayscaleTransformationMode.GTM_SKIP,
    EnumGrayscaleTransformationMode.GTM_SKIP,
    EnumGrayscaleTransformationMode.GTM_SKIP
]

reader.update_runtime_settings(settings)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

threadn = 1  # min(4, multiprocessing.cpu_count())
pool = ThreadPool(processes=threadn)
barcodeTasks = deque()

# Create an XML root element to store barcode information
root = ET.Element("Barcodes")
xml_file_name = "detected_barcodes.xml"

# Set to store already processed barcodes for duplicate detection
detected_barcodes = set()


def save_xml():
    tree = ET.ElementTree(root)
    tree.write(xml_file_name, encoding="utf-8", xml_declaration=True)


def is_duplicate(barcode_text, barcode_format):
    barcode_key = (barcode_text, barcode_format)
    if barcode_key in detected_barcodes:
        return True
    detected_barcodes.add(barcode_key)
    return False

def add_barcode_to_xml(result):
    if is_duplicate(result.barcode_text, result.barcode_format_string):
        print(f"Duplicate barcode ignored: {result.barcode_text}")
        return

    barcode = ET.SubElement(root, "Barcode")
    ET.SubElement(barcode, "Text").text = result.barcode_text
    ET.SubElement(barcode, "Format").text = result.barcode_format_string
    # Save XML to file after adding a new barcode
    save_xml()
    print(f"New barcode added: {result.barcode_text}")

def process_frame(frame):
    try:
        results = reader.decode_buffer(frame)
        return results
    except BarcodeReaderError as bre:
        print(bre)
        return None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    # Process and display results from completed tasks
    while len(barcodeTasks) > 0 and barcodeTasks[0].ready():
        results = barcodeTasks.popleft().get()
        if results is not None:
            for result in results:
                points = result.localization_result.localization_points
                # Draw bounding box and display result text
                cv2.polylines(frame, [np.array(points, np.int32)], True, (0, 255, 0), 2)
                cv2.putText(frame, result.barcode_text, (points[0][0], points[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # Add barcode result to the XML structure and save in real-time
                add_barcode_to_xml(result)

    # Add new frames to the processing queue if there's capacity
    if len(barcodeTasks) < threadn:
        task = pool.apply_async(process_frame, (frame.copy(),))
        barcodeTasks.append(task)

    cv2.imshow("Press 'Esc' to exit", frame)

    # Exit on 'ESC' key press (ASCII code 27)
    if cv2.waitKey(1) == 27:
        break

# Release resources
print("Closing application...")
cap.release()
cv2.destroyAllWindows()
pool.close()
pool.join()
