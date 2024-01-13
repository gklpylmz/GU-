import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

def plaka_Konum(img):


    img_bgr = img
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ir_img = cv2.medianBlur(img_gray,5) 
    ir_img = cv2.medianBlur(ir_img,5)


    median = np.median(ir_img)
    low = 0.67* median
    high =1.33*median #113

    kenarlik = cv2.Canny(ir_img,low,high)  
    kenarlik=cv2.dilate(kenarlik,np.ones((3,3),np.uint8),iterations=1)  

    cnt =cv2.findContours(kenarlik,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cnt=cnt[0]
    cnt=sorted(cnt,key=cv2.contourArea,reverse=True)

    H,W=500,500
    plaka=None

    for c in cnt:
        rect=cv2.minAreaRect(c)
        (x,y),(w,h),r=rect
        if(w>h and w>h*3) or (h>w and h>w*3):
            box=cv2.boxPoints(rect)
            box=np.int64(box)
            
            minx=np.min(box[:,0])
            miny=np.min(box[:,1])
            maxx=np.max(box[:,0])
            maxy=np.max(box[:,1])

            tahmini_plaka= img_gray[miny:maxy,minx:maxx].copy()
            tahmini_medyan = np.median(tahmini_plaka)
            #10070
            kontrol1= tahmini_medyan>70 and tahmini_medyan<200 #150 #260 # default 200
            kontrol2=h<50 and w<150
            kontrol3=w<50 and h<150

            print(f"Tahmini Plaka Medyanı : {tahmini_medyan} Genşişlik : {w} Yükseklik {h}")

            kontrol=False
            if(kontrol1 and (kontrol2 or kontrol3)):
                cv2.drawContours(img,[box],0,(0,255,0),2)
                plaka=[int(i) for i in[minx,miny,w,h]]
                kontrol=True

            else:
                #cv2.drawContours(img,[box],0,(0,0,255),2)
                pass
            

            if(kontrol):
                return plaka,img
    return []