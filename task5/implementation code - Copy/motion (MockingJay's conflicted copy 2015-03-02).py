import math
import serial
ser=serial.Serial(3) #COM4
grid_line_x = 17
grid_line_y = 17
##########################
# returning grid coordinate from pixels coordinates
#
#
#
#
def getcoor(x,y,m,n):
        '''
        cx=x/n#(int)(round(x/m))
        cy=y/n#(int)(round(y/n))
        return cx,cy
        '''
        #img=cv2.imread(filename) ##getting input image
        X=0
        Y=0
        for i in range(0, grid_line_x): ##drawing lines
                X=X+m
                Y=0
                for j in range(0, grid_line_y): ##drawing lines
                        Y=Y+n
                        #print X,Y
                        if x<=X and y<=Y:
                                return i,j
                                break
##########################
# converting grid coordinates into pixels
#
#
#
#
def gridtopixel(x,y,m,n):
        X=x*m+m/2
        Y=y*n+n/2
        return X,Y
########################
#get slope angle
#
#
#
#
def getslope(x1,y1,x2,y2):
        m=0
        if x2-x1!=0:
                m=-(float)(y2-y1)/(x2-x1)
                return m
        else:
                #ser.write("8")
                #ser.write("4")
                #ser.write("5")
        #print mbb
                return 50#m>50 for angle>88
############################
# getting orientation of the bot and move it
#
#
#
def orientmove(mbs,mbb,ax,ay,bx,by,flag):
        if ax==bx and ay==by: #check if bot has reached next coordinate
                #ser.write("5")
                #print "Hello"
                ser.write("7")
                return 1
        else:
                
                if mbs*mbb!=-1 :
                        theta=math.atan((mbs-mbb)/(1+mbs*mbb))
                        print theta
                        if theta<-0.08 or theta>0.08:
                                #com=1
                                if theta<-0.1:
                                       ser.write("6")  #right turn
                                else:
                                       ser.write("4")   #left turn
                                #com = raw_input()
                                
                                #ser.write(com) #send command
                        
                        else:
                                 ser.write("8")
                                 #ser.write("5")
                return 0
#############################
