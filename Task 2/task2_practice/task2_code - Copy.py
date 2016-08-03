import numpy as np
import cv2

#Teams can add other helper functions
#which can be added here

def play(img):
    '''
    img-- a single test image as input argument
    route_length  -- returns the single integer specifying the route length
    '''
    #add your code here
        
    return route_length, route_path


if __name__ == "__main__":
    #code for checking output for single image
    img = cv2.imread('test_images/test_image1.png')
    route_length, route_path = play(img)
    print "route length = ", route_length
    print "route path   = ", route_path
    #code for checking output for all images
    route_length_list = []
    route_path_list   = []
    for file_number in range(1,6):
        file_name = "test_images/test_image"+str(file_number)+".png"
        pic = cv2.imread(file_name)
        route_length, route_path = play(pic)
        route_length_list.append(route_length)
        route_path_list.append(route_path)
    print route_length_list
    print route_path_list
