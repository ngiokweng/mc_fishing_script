import cv2
import numpy as np
import pyautogui
import time


path = "./img/sc.jpg"
leftTopTemp_path = "./img/leftTop_tp.jpg"
rightTopTemp_path = "./img/rightTop_tp.jpg"


time.sleep(3)

#檢測區域
scanAreaX = (0,0)
scanAreaY = (400,600) #根據情況需作出改變
#標誌
checkForArea = False

while True:
    pyautogui.screenshot(path)
    img = cv2.imread(path)

    if not checkForArea:
        ###### 計算MC客戶端的大概位置(只需計1次) ######
        leftTopTemp = cv2.imread(leftTopTemp_path)
        leftTopTpWidth,leftTopTpHeight = leftTopTemp.shape[1],leftTopTemp.shape[0]

        rightTopTemp = cv2.imread(rightTopTemp_path)
        rightTopTempWidth,rightTopTempHeight = rightTopTemp.shape[1],rightTopTemp.shape[0]

        lefTop = cv2.matchTemplate(img,leftTopTemp,cv2.TM_CCOEFF_NORMED)
        lt_minVal,lt_maxVal,lt_minLoc,lt_maxLoc = cv2.minMaxLoc(lefTop)

        rightTop = cv2.matchTemplate(img,rightTopTemp,cv2.TM_CCOEFF_NORMED)
        rt_minVal,rt_maxVal,rt_minLoc,rt_maxLoc = cv2.minMaxLoc(rightTop)

        # cv2.rectangle(img,lt_maxLoc,(lt_maxLoc[0]+leftTopTpWidth,lt_maxLoc[1]+leftTopTpHeight),(255,0,0),2)
        # cv2.rectangle(img,rt_maxLoc,(rt_maxLoc[0]+rightTopTempWidth,rt_maxLoc[1]+rightTopTempHeight),(255,0,0),2)

        #計算MC的中間X座標
        mc_midX = int((lt_maxLoc[0]+rt_maxLoc[0]+rightTopTempWidth)/2)
        scanAreaX = (mc_midX-60,mc_midX+60)
        # cv2.rectangle(img,(mc_midX-60,400),(mc_midX+60,600),(255,0,0),3)

        #確保以上代碼只執行一次
        checkForArea = True
    

    #截取【檢測區域】
    img = img[scanAreaY[0]:scanAreaY[1],scanAreaX[0]:scanAreaX[1]]
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #轉為HSV，方便過濾

    lower = np.array([156,43,46])
    upper = np.array([180,255,255])
    mask = cv2.inRange(hsv,lower,upper) #過濾範圍

    # cv2.imshow("mask",mask)
    # if cv2.waitKey(0) == ord('q'):break

    w,h = mask.shape[1],mask.shape[0]

    flag = True
    #遍歷檢測範圍中所有的像素點
    for x in range(h):
        for y in range(w):
            #當檢測到非0時，代表未有魚上吊
            if not mask[x][y] == 0:
                flag = False
                
    #代表有魚上吊/未放吊竿
    if flag:
        time.sleep(0.03) #防止因太快而空吊
        print("出竿 / 收竿")
        pyautogui.rightClick()
        time.sleep(1.5)

    
    #每0.2s檢測1次
    time.sleep(0.2)