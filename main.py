import cv2
import pickle
import cvzone
import numpy as np

cap=cv2.VideoCapture("D:\CarParkProject\carPark.mp4")
width,height=109,48

def CheckParkingSpace(img_pro):
    space_count = 0
    for pos in pos_list:
        x,y=pos
        image_cropped=img_pro[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),image_cropped)
        count=cv2.countNonZero(image_cropped)
        cvzone.putTextRect(img,str(count),(x,y),scale=1,thickness=2)
        if count<850:
            color=(0,255,0)
            space_count+=1
        else:
            color=(0,0,255)

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2)
    cvzone.putTextRect(img,'free space is {}'.format(str(space_count)), (100,50), scale=3, thickness=5);






while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT) :
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    with open("CarParkPos", "rb") as f:
        pos_list=pickle.load(f)

    sucess, img = cap.read()
    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_binary=cv2.adaptiveThreshold(img_gray, 255,
	cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    img_median=cv2.medianBlur(img_binary,5)
    kernel=np.ones((3,3),np.uint8)
    img_dilate=cv2.dilate(img_median,kernel,iterations=1)
    CheckParkingSpace(img_dilate)
    cv2.imshow("Image",img_dilate)
    cv2.imshow("Image", img)
    cv2.waitKey(1)