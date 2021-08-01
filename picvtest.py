import cv2
import os

##car update logic
def update(xold, xnew):
    AB = xold
    if((xold & 1)  ^ (xold >> 1) == 0):
        AB = xnew
    return AB


#loopstart

#    camera.capture('/home/pi/Desktop/image.jpg')
##read camera image
img = cv2.imread('/home/pi/Desktop/image.jpg',1)
##
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
##establish the obstacle colours
mask1 = cv2.inRange(hsv, (25,50,60), (36, 200, 220))
##Isolate the obstacles
target = cv2.bitwise_and(img,img, mask=mask1)
##
# convert image to grayscale image
gray_image = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
# convert the grayscale image to binary image
ret,thresh = cv2.threshold(gray_image,127,255,0)

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
centers = []
for c in contours:
   # calculate moments for each contour
    M = cv2.moments(c)
   # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    centers.append([cX,cY])
cv2.imshow("Image", img)

height, width, channels = img.shape
ymax = 0
ymin = height
for c in centers:
    if(c[1] > ymax):
        ymax = c[1]
    if(c[1] < ymin):
        ymin = c[1]
ycenter = ymax - ((ymax - ymin) / 2)
course = 0x00
for c in centers:
    if(c[0] > width / 2):
        if(c[1] > ycenter):
            if (c[0] > (5/8) * width):
                course = course | 0b1
            elif(c[0] < (5/8) * width):
                course = course | 0b10
        if(c[1] < ycenter):
            if (c[0] > (5/8) * width):
                course = course | 0b100
            elif(c[0] < (5/8) * width):
                course = course | 0b1000
    if(c[0] < width / 2):
        if(c[1] > ycenter):
            if (c[0] < (3/8) * width):
                course = course | 0b100000
            elif(c[0] > (3/8) * width):
                course = course | 0b10000
        if(c[1] < ycenter):
            if (c[0] < (3/8) * width):
                course = course | 0b10000000
            elif(c[0] > (3/8) * width):
                course = course | 0b1000000
        

os.system('cls' if os.name=='nt' else 'clear')
print(course)
cv2.waitKey(0)

#loopend



