import cv2
def space_map(img):
    grid_map= [ [ 0 for i in range(10) ] for j in range(10) ]# initializing zero filled 10x10 matrix 
    for x in range(0, 10):
        X=x*40+20 
        for y in range(0,10):
            Y=y*40+20
            #img[Y,X] is pixel at the centre of each cell
            if img[Y,X,0]!=255 or img[Y,X,1]!=255 or img[Y,X,2]!=255: #detecting obstacle, if pixel color is not white then mark it as obstacle
                grid_map[y][x]=1 #marking obstacles with value 1
            continue
    return grid_map

img=cv2.imread("test_images/test_image1.png")
print space_map(img)
