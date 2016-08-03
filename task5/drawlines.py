import cv2
def grid_draw(filename,m,n): ##filename is image filename with full file path, n is grid of n lines
    img=cv2.imread(filename) ##getting input image
    h,k,l=img.shape
    print h,k
    line_widthm=h/(m-1)
    line_widthn=k/(n-1) ##calculating width between 2 consecutive parallel lines
    for x in range(0, m): ##drawing lines
        X=x*line_widthm

        cv2.line(img,(0,X),(k,X),(0,0,255), 2)#lines is red color, bgr format
    for y in range(0, n): ##drawing lines
        Y=y*line_widthn

        cv2.line(img,(Y,0),(Y,h),(255,0,0), 2)#lines is red color, bgr format
    return (img)        
    
#img=cv2.imread("test_images/test_image1.png")

img=grid_draw("binary.jpg",15,15) ##10,14 perfect for path deduction
cv2.imshow("Grid map",img)
cv2.imwrite("binary1.jpg",img)
############################################
## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
############################################
