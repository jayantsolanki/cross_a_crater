############################################
## Import OpenCV
import numpy as np
import cv2
def get_perspective_image(frame):
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    lower = np.array([0, 0, 0]) #black color mask
    upper = np.array([120, 120, 120])
    mask = cv2.inRange(frame, lower, upper)
    
    ret,thresh1 = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame,contours,-1,(0,255,0),3)
    cv2.imshow('src', frame)

    return frame



cap = cv2.VideoCapture(1)
ret, src = cap.read()
cv2.imshow('src', src)
cv2.imwrite("input_image.jpg", src)

##getting the perspective image
img_src= get_perspective_image(src)

cv2.imwrite("output_image.jpg", img_src)

#cv2.imshow('dst', img_src)
############################################

## Video Loop
while(1):
## Read the image
        ret, frame = cap.read()
        cap.set(10, 2)
        img_src= get_perspective_image(frame)
## End the video loop
        if cv2.waitKey(1) == 27:  ## 27 - ASCII for escape key
                break

############################################

############################################
## Close and exit
# close camera
cap.release()
cv2.destroyAllWindows()
############################################
