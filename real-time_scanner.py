import numpy as np
import cv2
from multiprocessing.pool import ThreadPool
from collections import deque
from dbr import DynamsoftBarcodeReader
from dbr import *

# --- IMPORTANT: REPLACE WITH YOUR LICENSE KEY ---
LICENSE_KEY = 't0083YQEAAKqisPaOrLvM0tGYIFZd04VlwkQPvSCAZ4R2+kDWpFzDsEKVbxLkbhN4noJKQL+E0fMaU/Pmjx9bxkBIbeFwualmfM803jOjFTODC/izSGg=;t0082YQEAAEOa7iWLgmj5HwcSP7J0uNaMQ/kZ/x8HgwPBUpUE8rgwZj8s7nrHomUArjOIL611KRz1gqlYYYTZ98clI+D2lvWM75vifTOySIIddlJJAg==;t0082YQEAAA/YSn4DjmzJcu2C2qrVkNFVQ3pbrfwAi+IqrxbxV31mVURD6/IhsMOj+eYszSaE4PXkcuJ0GyOjRmygD4xAkHAZ3zfF+2bULAkOfcdJCQ=='

BarcodeReader.init_license(LICENSE_KEY)

reader = BarcodeReader()
settings = reader.get_runtime_settings()
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

threadn = 1
pool = ThreadPool(processes=threadn)
barcodeTasks = deque()

def process_frame(frame):
    """
    Decodes barcodes from a frame using the configured mixed-mode detection.
    """
    try:
        # The DBR engine will now handle both regular and inverted barcodes
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

    # Add new frames to the processing queue if there's capacity
    if len(barcodeTasks) < threadn:
        task = pool.apply_async(process_frame, (frame.copy(),))
        barcodeTasks.append(task)

    cv2.imshow('Mixed Barcode Scanner - Dynamsoft', frame)

    # Exit on 'ESC' key press (ASCII code 27)
    if cv2.waitKey(1) == 27:
        break

# Release resources
print("Closing application...")
cap.release()
cv2.destroyAllWindows()
pool.close()
pool.join()