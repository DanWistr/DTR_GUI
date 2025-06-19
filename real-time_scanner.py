import numpy as np
import cv2
from multiprocessing.pool import ThreadPool
from collections import deque
import dbr
from dbr import *

LICENSE_KEY = 't0083YQEAAKqisPaOrLvM0tGYIFZd04VlwkQPvSCAZ4R2+kDWpFzDsEKVbxLkbhN4noJKQL+E0fMaU/Pmjx9bxkBIbeFwualmfM803jOjFTODC/izSGg=;t0082YQEAAEOa7iWLgmj5HwcSP7J0uNaMQ/kZ/x8HgwPBUpUE8rgwZj8s7nrHomUArjOIL611KRz1gqlYYYTZ98clI+D2lvWM75vifTOySIIddlJJAg==;t0082YQEAAA/YSn4DjmzJcu2C2qrVkNFVQ3pbrfwAi+IqrxbxV31mVURD6/IhsMOj+eYszSaE4PXkcuJ0GyOjRmygD4xAkHAZ3zfF+2bULAkOfcdJCQ=='

BarcodeReader.init_license(LICENSE_KEY)
reader = BarcodeReader()
cap = cv2.VideoCapture(0)

threadn =cv2.getNumberOfCPUs()
pool = ThreadPool(processes = threadn)
barcodeTasks = deque()

def process_frame(frame):
    try:
        # Step 2: Desaturate using HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        s[:] = 0
        hsv_min_sat = cv2.merge([h, s, v])
        desat_img = cv2.cvtColor(hsv_min_sat, cv2.COLOR_HSV2BGR)

        # Step 3: Convert to grayscale
        gray = cv2.cvtColor(desat_img, cv2.COLOR_BGR2GRAY)

        # Step 4: Invert grayscale image
        inverted = cv2.bitwise_not(gray)

        # Convert back to BGR for compatibility with decoder if needed
        processed = cv2.cvtColor(inverted, cv2.COLOR_GRAY2BGR)

        # Decode the processed (inverted) frame
        results = reader.decode_buffer(processed)
        return results
    except BarcodeReaderError as bre:
        print(bre)
        return None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    while len(barcodeTasks) > 0 and barcodeTasks[0].ready():
        results = barcodeTasks.popleft().get()
        if results is not None:
            for result in results:
                points = result.localization_result.localization_points
                cv2.line(frame, points[0], points[1], (0,255,0), 2)
                cv2.line(frame, points[1], points[2], (0,255,0), 2)
                cv2.line(frame, points[2], points[3], (0,255,0), 2)
                cv2.line(frame, points[3], points[0], (0,255,0), 2)
                cv2.putText(frame, result.barcode_text, points[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

    if len(barcodeTasks) < threadn:
        task = pool.apply_async(process_frame, (frame.copy(), ))
        barcodeTasks.append(task)

    cv2.imshow('Barcode & QR Code Scanner', frame)
    if cv2.waitKey(1) == 27:  # ESC key
        break