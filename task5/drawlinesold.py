import cv2
def grid_draw(filename,n): ##filename is image filename with full file path, n is grid of n lines
    img=cv2.imread(filename) ##getting input image
    line_width=400/(n-1) ##calculating width between 2 consecutive parallel lines
    for x in range(0, n): ##drawing lines
        X=x*line_width
        for y in range(0,n):
            Y=y*line_width
            ##vertical lines
            cv2.line(img,(Y,X),(Y,400),(0,0,255), 2)#lines is red color, bgr format
            ##horizontal lines
            cv2.line(img,(X,Y),(400,Y),(0,0,255), 2)#lines is red color, bgr format
    return (img)        
    
#img=cv2.imread("test_images/test_image1.png")
img=grid_draw("images/input.jpg",4)
cv2.imshow("Grid map",img)
############################################
## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
############################################
