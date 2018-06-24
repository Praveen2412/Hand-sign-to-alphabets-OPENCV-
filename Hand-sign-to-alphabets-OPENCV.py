import cv2
import numpy as np
import math
from pynput.keyboard import Key,Controller
import time
import pyautogui
import os
import subprocess as sp

keyboard=Controller()




cam=int(input("Enter Camera number: "))

cap = cv2.VideoCapture(cam)

f= open("text1.txt","w+")
programName = "notepad.exe"
fileName = "text1.txt"
sp.Popen([programName, fileName])

while(cap.isOpened()):
    # read image
    ret, img = cap.read()
    resize = cv2.resize(img, (800, 800), interpolation = cv2.INTER_LINEAR)

    # get hand data from the rectangle sub window on the screen
    cv2.rectangle(resize, (300,300), (00,00), (0,255,0),0)
    crop_img = resize[00:300, 00:300]
    cv2.rectangle(resize, (800,300), (500,00), (255,0,0),0)
    crop_img1 = resize[00:300, 500:800]
    # convert to grayscale
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    grey1 = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)

    # applying gaussian blur
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)
    blurred1 = cv2.GaussianBlur(grey1, value, 0)

    # thresholding: Otsu's Binarization method
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    _, thresh2 = cv2.threshold(blurred1, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # show thresholded image
    #cv2.imshow('Thresholded', thresh1)
    

    # check OpenCV version to avoid unpacking error
    (version, _, _) = cv2.__version__.split('.')

    if version == '3':
        image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        image1, contours1, hierarchy1 = cv2.findContours(thresh2.copy(), \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    elif version == '2':
        contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
               cv2.CHAIN_APPROX_NONE)
        contours1, hierarchy1 = cv2.findContours(thresh2.copy(),cv2.RETR_TREE, \
               cv2.CHAIN_APPROX_NONE)

  
         

    # find contour with max area
    cnt = max(contours, key = lambda x: cv2.contourArea(x))
    cnt1 = max(contours1, key = lambda x1: cv2.contourArea(x1))

    # create bounding rectangle around the contour (can skip below two lines)
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)
    x1, y1, w1, h1 = cv2.boundingRect(cnt1)
    cv2.rectangle(crop_img1, (x1, y1), (x1+w1, y1+h1), (0, 0, 255), 0)

    # finding convex hull
    hull = cv2.convexHull(cnt)
    hull1 = cv2.convexHull(cnt1)

    
    # drawing contours
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], 0,(0, 0, 255), 0)

    drawing1 = np.zeros(crop_img1.shape,np.uint8)
    cv2.drawContours(drawing1, [cnt1], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing1, [hull1], 0,(0, 0, 255), 0)

    # finding convex hull
    hull = cv2.convexHull(cnt, returnPoints=False)
    hull1 = cv2.convexHull(cnt1, returnPoints=False)

    # finding convexity defects
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

    defects1 = cv2.convexityDefects(cnt1, hull1)
    count_defects1 = 0
    cv2.drawContours(thresh2, contours1, -1, (0, 255, 0), 3)

  

    # applying Cosine Rule to find angle for all defects (between fingers)
    # with angle > 90 degrees and ignore defects
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]

        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        #index finger
       # A = math.atan((cy-far[1])/(cx-far[0]))
       # print(math.degrees(A))
       # print(far[0],far[1])
        # find length of all sides of triangle
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

        # apply cosine rule here
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        

        # ignore angles > 90 and highlight rest with red dots
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img, far, 1, [0,0,255], -1)
        #dist = cv2.pointPolygonTest(cnt,far,True)

        # draw a line from start to end i.e. the convex points (finger tips)
        # (can skip this part)
        cv2.line(crop_img,start, end, [0,255,0], 2)
        #cv2.circle(crop_img,far,5,[0,0,255],-1)


   




    for j in range(defects1.shape[0]):
        s1,e1,f1,d1 = defects1[j,0]

        start1 = tuple(cnt1[s1][0])
        end1 = tuple(cnt1[e1][0])
        far1 = tuple(cnt1[f1][0])

        # find length of all sides of triangle
        a1 = math.sqrt((end1[0] - start1[0])**2 + (end1[1] - start1[1])**2)
        b1 = math.sqrt((far1[0] - start1[0])**2 + (far1[1] - start1[1])**2)
        c1 = math.sqrt((end1[0] - far1[0])**2 + (end1[1] - far1[1])**2)

        # apply cosine rule here
        angle1 = math.acos((b1**2 + c1**2 - a1**2)/(2*b1*c1)) * 57

        # ignore angles > 90 and highlight rest with red dots
        if angle1 <= 90:
            count_defects1 += 1
            cv2.circle(crop_img1, far1, 1, [0,0,255], -1)
        #dist = cv2.pointPolygonTest(cnt,far,True)

        # draw a line from start to end i.e. the convex points (finger tips)
        # (can skip this part)
        cv2.line(crop_img1,start1, end1, [0,255,0], 2)
        #cv2.circle(crop_img,far,5,[0,0,255],-1)



    #cv2.imshow('Gesture', resize)

    # define actions required
    if count_defects == 1 and  count_defects1 == 0 :
        cv2.putText(resize,'A', (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
  
        keyboard.press('a')
        keyboard.release('a')
        time.sleep(0.1)
       
    elif count_defects == 2 and count_defects1 == 0:
        str = "B"
        cv2.putText(resize, str, (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('b')
        keyboard.release('b')
        time.sleep(0.1)
    elif count_defects == 3 and count_defects1 == 0 :
        cv2.putText(resize,"C ", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('c')
        keyboard.release('c')
        time.sleep(0.1)
    elif count_defects == 4 and count_defects1 == 0:
        cv2.putText(resize,"D", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('d')
        keyboard.release('d')
        time.sleep(0.1)
        
    elif count_defects1 == 1 and count_defects == 0 :
        cv2.putText(resize,"E", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('e')
        keyboard.release('e')
        time.sleep(0.1)
    elif count_defects1 == 2 and count_defects == 0 :
        str = "F"
        cv2.putText(resize, str, (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('f')
        keyboard.release('f')
        time.sleep(0.1)
    elif count_defects1 == 3 and count_defects == 0 :
        cv2.putText(resize,"G ", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('g')
        keyboard.release('g')
        time.sleep(0.1)
    elif count_defects1 == 4 and count_defects == 0 :
        cv2.putText(resize,"H", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('h')
        keyboard.release('h')
        time.sleep(0.1)
    
    elif count_defects == 1 and count_defects1 == 1:
        cv2.putText(resize,"I", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('i')
        keyboard.release('i')
        time.sleep(0.1)
    elif count_defects == 2 and count_defects1 == 1:
        str = "J"
        cv2.putText(resize, str, (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('j')
        keyboard.release('j')
        time.sleep(0.1)
    elif count_defects == 3 and count_defects1 == 1:
        cv2.putText(resize,"K ", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('k')
        keyboard.release('k')
        time.sleep(0.1)
    elif count_defects == 4 and count_defects1 == 1:
        cv2.putText(resize,"L", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('l')
        keyboard.release('l')
        time.sleep(0.1)

    elif count_defects == 1 and count_defects1 == 2:
        str = "M"
        cv2.putText(resize, str, (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('m')
        keyboard.release('m')
        time.sleep(0.1)
    elif count_defects == 2 and count_defects1 == 2:
        cv2.putText(resize,"N", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('n')
        keyboard.release('n')
        time.sleep(0.1)
    elif count_defects == 3 and count_defects1 == 2:
        cv2.putText(resize,"O", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('o')
        keyboard.release('o')
        time.sleep(0.1)
        
    elif count_defects == 4 and count_defects1 == 2:
        str = "P"
        cv2.putText(resize, str, (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('p')
        keyboard.release('p')
        time.sleep(0.1)
    elif count_defects == 1 and count_defects1 == 3:
        cv2.putText(resize,"Q", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('q')
        keyboard.release('q')
        time.sleep(0.1)
    elif count_defects == 2 and count_defects1 == 3:
        cv2.putText(resize,"R", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('r')
        keyboard.release('r')
        time.sleep(0.1)

    elif count_defects == 3 and count_defects1 == 3:
        str = "S"
        cv2.putText(resize, str, (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('s')
        keyboard.release('s')
        time.sleep(0.1)
    elif count_defects == 4 and count_defects1 == 3:
        cv2.putText(resize,"T", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('t')
        keyboard.release('t')
        time.sleep(0.1)
    elif count_defects == 1 and count_defects1 == 4:
        cv2.putText(resize,"U", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('u')
        keyboard.release('u')
        time.sleep(0.1)

    elif count_defects == 2 and count_defects1 == 4:
        str = "V"
        cv2.putText(resize, str, (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press('v')
        keyboard.release('v')
        time.sleep(0.1)
    elif count_defects == 3 and count_defects1 == 4:
        cv2.putText(resize,"Backspace ", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
        
        time.sleep(0.1)
    elif count_defects == 4 and count_defects1 == 4:
        cv2.putText(resize,"Space", (400, 600), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
        
      
        keyboard.press(Key.space)
        keyboard.release(Key.space)
       
        time.sleep(0.1)
    else:
        cv2.putText(resize,"Place hand inside box", (50, 600),\
                    cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 255, 0), 4)    

    # show appropriate images in windows
    cv2.resizeWindow('Gesture', 1000,800)
    cv2.imshow('Gesture', resize)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('Contours', all_img)

    all_img1 = np.hstack((drawing1, crop_img1))
    cv2.imshow('Contours1', all_img1)
    #print(angle)
    cv2.imshow('blur',blurred)
    cv2.imshow('blur1',blurred1)
    cv2.imshow('thresh1',thresh1)
    cv2.imshow('thresh2',thresh2)
        
        
    k = cv2.waitKey(10)
    if k == 27:
        break
    if  k & 0xFF == ord('q'):
        
        break
cap.release()
cv2.destroyAllWindows()
os.system('TASKKILL /F /IM notepad.exe')
          
