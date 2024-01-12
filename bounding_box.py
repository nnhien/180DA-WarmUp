import numpy as np
import cv2 as cv

"""
    * Using HSV instead of BGR is better for detection
"""

cap = cv.VideoCapture(1)

while True:
    _, bgr_frame = cap.read()

    hsv_frame = cv.cvtColor(bgr_frame, cv.COLOR_BGR2HSV)

    lower_color_hsv = np.array([0, 120, 181], dtype=np.uint8)
    upper_color_hsv = np.array([8, 255, 255], dtype=np.uint8)

    mask = cv.inRange(hsv_frame, lower_color_hsv, upper_color_hsv)

    contours, hierarchy = cv.findContours(mask, 1, 2)

    if contours:
        largest_contour = max(contours, key=cv.contourArea)
        x,y,w,h = cv.boundingRect(largest_contour)
        cv.rectangle(bgr_frame, (x,y), (x+w, y+h), (0, 255, 0), 4)

    cv.imshow("BGR Frame", bgr_frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv.destroyAllWindows()