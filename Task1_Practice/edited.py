import numpy as np
import cv2

img = cv2.imread('test_images/1.jpg')

#Teams can add other helper functions which can be \
#added here

'''def play(img):
   
    img-- a single test image as input argument
    ball_number  -- returns the single integer specifying the target that was 
    hit  eg. 1, 5, etc
   
    #add your code here
    return ball_number
'''

if __name__ == "__main__":
    #checking output for single image
    img = cv2.imread('test_images/1.jpg')
    ball_number = play(img)
    print ball_number, " number ball at target range"
    #checking output for all images
    num_list = []
    for file_number in range(1,9):
        file_name = "test_images/"+str(file_number)+".jpg"
        pic = cv2.imread(file_name)
        ball_number = play(pic)
        num_list.append(ball_number)
    print num_list
