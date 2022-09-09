#-*-coding:GBK -*- 
import time
from inspect import isframe
import cv2
import kociemba
from kociemba.pykociemba.color import B
import numpy as np
import multiprocessing
import threading
import serial.tools.list_ports
from sklearn.cluster import KMeans
def bubbleSort(arr):
    located = []
    for i in range(len(arr)):
        located.append(i)
    for i in range(1, len(arr)):
        for j in range(0, len(arr) - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                located[j], located[j + 1] = located[j + 1], located[j]
    return located[0:9]
def kmeans_sort(rgb_save,hsv_save):
    #for i in range(len(hsv_save)):
    #    if i % 9 == 0:
    #        print("")
    #    print(hsv_save[i], end = "\t")
    #print("")
    #for i in range(len(rgb_save)):
    #    if i % 9 == 0:
    #        print("")
    #    print(rgb_save[i], end = "\t")
    #print("")
    s_save = []
    for i in range(54):
        s_save.append(hsv_save[i][1])
    white = bubbleSort(s_save)
   # print(white)
    whiteless_rgb_save = []
    for i in range(len(bgr_save)):
        flag = 0
        for j in range(9):
            if i == white[j]: flag = 1
        if flag == 1: continue
        whiteless_rgb_save.append(rgb_save[i])
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(whiteless_rgb_save)
    whiteless_sort = kmeans.predict(whiteless_rgb_save)
    sorted = []
    flag = 0
    for i in range(len(whiteless_sort) + 9):
        flag1 = 0
        for j in range(9):
            if i == white[j]:
                flag += 1
                flag1 = 1
                break
        if flag1 != 0:
            sorted.append(5)
        else:
            sorted.append(whiteless_sort[i - flag])
    print(sorted)
    return sorted
        #kmeans = KMeans(n_clusters=6)
        #kmeans.fit(bgr_save)
        #sort = kmeans.predict(bgr_save)
        #print(sort)
        #return sort
# 近似轮廓四点排序函数
def point_paixu(lists):
    lists = list(lists)
    for i in range(4):
        for j in range(i + 1, 4):
            if lists[i][0] > lists[j][0]:
                lists[i], lists[j] = lists[j], lists[i]
    if lists[0][1] > lists[1][1]: lists[0], lists[1] = lists[1], lists[0]
    if lists[2][1] < lists[3][1]: lists[2], lists[3] = lists[3], lists[2]
    return lists
# 验证分类数量
def ver(l):
    time_0 = 0
    time_1 = 0
    time_2 = 0
    time_3 = 0
    time_4 = 0
    time_5 = 0
    flag = 0
    for i in range(54):
        if l[i] == 0: time_0 += 1
        if l[i] == 1: time_1 += 1
        if l[i] == 2: time_2 += 1
        if l[i] == 3: time_3 += 1
        if l[i] == 4: time_4 += 1
        if l[i] == 5: time_5 += 1
        if time_0>9 or time_1>9 or time_2>9 or time_3>9 or time_4>9 or time_5>9:flag = 1
    if flag:
       # print(time_0,time_1,time_2,time_3,time_4,time_5)
        return 0
    return 1
# 对已分类对象排版
def x_y(l):
    t = []
    for i in range(54): t.append(0)
    for i in range(54):
        if 0 <= i < 9: t[i] = l[8 - ((int(i / 3) * 3 + 2 - i) * 3 + int(i / 3))]
        if 9 <= i < 18: t[i] = l[i + 9]
        if 18 <= i < 27: t[i] = l[i + 18]
        if 27 <= i < 36: t[i] = l[(int((i - 27) / 3) * 3 + 2 - (i - 27)) * 3 + int((i - 27) / 3) + 27]
        if 36 <= i < 45: t[i] = l[i + 9]
        if 45 <= i < 54: t[i] = l[i - 36]
    return t
def y_z(l):
    t = []
    for i in range(54):t.append(0)
    for i in range(54):
        if 0 <= i < 9: t[i] = l[i + 18]
        if 9 <= i < 18: t[i] = l[((int((i-9) / 3) * 3 + 2 - (i-9)) * 3 + int((i-9) / 3))+9]
        if 18 <= i < 27: t[i] = l[i + 9]
        if 27 <= i < 36: t[i] = l[8 - (i -27) + 45]
        if 36 <= i < 45: t[i] = l[8 - ( (int((i-36) / 3) * 3 + 2 - (i-36))* 3 + int((i-36) / 3) )+36]
        if 45 <= i < 54: t[i] = l[8 - (i - 45)]
    return t
def paiban(l):
    s = ''
    for i in range(54):
        if l[i] == l[4]:s = s + 'U'
        elif l[i] == l[13]:s = s + 'R'
        elif l[i] == l[22]:s = s + 'F'
        elif l[i] == l[31]:s = s + 'D'
        elif l[i] == l[40]:s = s + 'L'
        elif l[i] == l[49]:s = s + 'B'
    return s
def result(l,n):
    s = ''
    for i in range(len(l)):
        if n[len(n)-1] == '1':
            if l[i] == 'F': s += 'L'
            elif l[i] == 'L': s += 'B'
            elif l[i] == 'B': s += 'R'
            elif l[i] == 'R': s += 'F'
            else: s += l[i]
        elif n[len(n)-1] == '2':
            if l[i] == 'U': s += 'F'
            elif l[i] == 'F': s += 'D'
            elif l[i] == 'D': s += 'B'
            elif l[i] == 'B': s += 'U'
            else: s += l[i]
    if len(n) > 1:
        s = result(s,n[0:len(n)-1])
    return s
def result_flag(l):
    s = ''
    for i in range(len(l)):
        if l[i] == 'U' or l[i] == 'D': s = s + '1'
        if l[i] == 'R' or l[i] == 'L': s = s + '2'
        if l[i] == 'F' or l[i] == 'B': s = s + '3'
    return s
def sort_go(l):
    rube_re = []
    sort1 = l.copy()
    yan_zheng = []
    t = ''
   # print(paiban(l))
    try:  x = kociemba.solve(paiban(l))
    except Exception: 
        flag_yichang=1
        return

    rube_re.append(x)
    yan_zheng.append(result_flag(x))
    for i in range(6):
        for j in range(3):
            t = t + '1'
            sort1 = x_y(sort1)
            x = result(kociemba.solve(paiban(sort1)), t)
            cs = result_flag(x)
            flag = 0
            for k in range(len(yan_zheng)):
                if yan_zheng[k] == cs:
                    flag = 1
                    break
            if flag == 0:
                yan_zheng.append(cs)
                rube_re.append(x)
        t = t + '2'
        sort1 = y_z(sort1)
        if i == 2:
            t = t + '1' + '2' + '1'
            sort1 = x_y(y_z(x_y(sort1)))
        if i != 5:
            x = result(kociemba.solve(paiban(sort1)), t)
            cs = result_flag(x)
            flag = 0
            for k in range(len(yan_zheng)):
                if yan_zheng[k] == cs:
                    flag = 1
                    break
            if flag == 0:
                yan_zheng.append(cs)
                rube_re.append(x)
    return rube_re
def qurgb(img3):
    # global hsv_change
    jihe = []
    num = 0
    for i in range(img3.shape[0]):
        for j in range(img3.shape[1]):
            jihe.append(list(img3[i, j]))
            num += 1
    sum_x = sum_y = sum_z = 0
    for i in range(num):
        x, y, z = jihe[i]
        sum_x = sum_x + x
        sum_y = sum_y + y
        sum_z = sum_z + z
    r = int(sum_x / num)
    g = int(sum_y / num)
    b = int(sum_z / num)
    return list((r, g, b))

# 设置摄像头 
def setcapture() :
     global capture1, capture2 ,capture3, capture4 
     capture1 = cv2.VideoCapture(4)    #前面 拍的是魔方的右面  
     capture2 = cv2.VideoCapture(1)        #后面
     capture3 = cv2.VideoCapture(2)    #上面  
     capture4 = cv2.VideoCapture(3)    #下面
    
     capture1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
     capture1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
     capture2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
     capture2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
     capture3.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
     capture3.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
     capture4.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
     capture4.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# 画出四个面 色块的点
def drawline():
        global img1,img2,img3,img4,frame1,frame2,frame3,frame4
        ret1, frame1 = capture1.read(1)  # 前摄像头
        ret4, frame4 = capture4.read(1)  # 下摄像头
        ret2, frame2 = capture2.read(1)  # 后摄像头
        ret3, frame3 = capture3.read(1)   # 上摄像头
        img1=frame1.copy()
        img2=frame2.copy()
        img3=frame3.copy()
        img4=frame4.copy()
        
       # # 魔方R面 色块 
        #cv2.line(frame1, (15, 190), (210, 390), color=(0, 0, 255), thickness=1)
        #cv2.line(frame1, (15, 190), (215, 15), color=(0, 0, 255), thickness=1)
        #cv2.line(frame1, (215, 15), (410, 200), color=(0, 0, 255), thickness=1)
        #cv2.line(frame1, (410, 200), (210, 390), color=(0, 0, 255), thickness=1)
        cv2.rectangle(frame1,(125,220),(135,230),(0,0,255),1) #画矩形  第一排
        cv2.rectangle(frame1,(200,155),(210,165),(0,0,255),1) #画矩形
        cv2.rectangle(frame1,(270,85),(280,95),(0,0,255),1) #画矩形

        cv2.rectangle(frame1,(200,290),(210,300),(0,0,255),1) #画矩形  第二排
        cv2.rectangle(frame1,(270,220),(280,230),(0,0,255),1) #画矩形
        cv2.rectangle(frame1,(320,145),(330,155),(0,0,255),1) #画矩形

        cv2.rectangle(frame1,(270,370),(280,380),(0,0,255),1) #画矩形 第三排
        cv2.rectangle(frame1,(320,270),(330,280),(0,0,255),1) #画矩形
        cv2.rectangle(frame1,(410,215),(420,225),(0,0,255),1) #画矩形
       ## ##魔方L面 
        #cv2.line(frame2, (220, 250), (385, 440), color=(0, 0, 255), thickness=1)
        #cv2.line(frame2, (220, 250), (340, 50), color=(0, 0, 255), thickness=1)
        #cv2.line(frame2, (390, 50), (550, 210), color=(0, 0, 255), thickness=1)
        #cv2.line(frame2, (550, 210), (385, 440), color=(0, 0, 255), thickness=1)



        cv2.rectangle(frame2,(140,250),(150,260),(0,0,255),1) #画矩形  
        cv2.rectangle(frame2,(230,175),(240,185),(0,0,255),1) #画矩形  
        cv2.rectangle(frame2,(285,105),(295,115),(0,0,255),1) #画矩形  第一排

        cv2.rectangle(frame2,(230,310),(240,320),(0,0,255),1) #画矩形  
        cv2.rectangle(frame2,(280,245),(290,255),(0,0,255),1) #画矩形
        cv2.rectangle(frame2,(355,190),(365,200),(0,0,255),1) #画矩形  第二排

        cv2.rectangle(frame2,(290,380),(300,390),(0,0,255),1) #画矩形
        cv2.rectangle(frame2,(355,305),(365,315),(0,0,255),1) #画矩形
        cv2.rectangle(frame2,(430,240),(440,250),(0,0,255),1) #画矩形  第三排

       ###魔方 U面 F面 
        #cv2.line(frame3, (150, 370), (370, 420), color=(0, 0, 255), thickness=1)
        #cv2.line(frame3, (150, 90), (360, 50), color=(0, 0, 255), thickness=1)
        #cv2.line(frame3, (360, 50), (540, 95), color=(0, 0, 255), thickness=1)
        #cv2.line(frame3, (540, 370), (370, 420), color=(0, 0, 255), thickness=1)
        #cv2.line(frame3, (150, 90), (150, 370), color=(0, 0, 255), thickness=1)
        #cv2.line(frame3, (540, 95), (540, 370), color=(0, 0, 255), thickness=1)
        #cv2.line(frame3, (360, 50), (370, 420), color=(0, 0, 255), thickness=1)

        cv2.rectangle(frame3,(495,140),(505,150),(0,0,255),1) #画矩形 魔方上面 第一排
        cv2.rectangle(frame3,(500,235),(510,245),(0,0,255),1) #画矩形
        cv2.rectangle(frame3,(495,340),(505,350),(0,0,255),1) #画矩形
        

        cv2.rectangle(frame3,(440,135),(450,145),(0,0,255),1) #画矩形 魔方上面 第二排
        cv2.rectangle(frame3,(440,235),(450,245),(0,0,255),1) #画矩形
        cv2.rectangle(frame3,(440,345),(450,355),(0,0,255),1) #画矩形


        cv2.rectangle(frame3,(380,135),(390,145),(0,0,255),1) #画矩形 魔方上面 第三排
        cv2.rectangle(frame3,(380,235),(390,245),(0,0,255),1) #画矩形
        cv2.rectangle(frame3,(375,345),(385,355),(0,0,255),1) #画矩形
        

        cv2.rectangle(frame3,(280,130),(290,140),(0,0,255),1) #画矩形 魔方正面 第一排
        cv2.rectangle(frame3,(280,235),(290,245),(0,0,255),1) #画矩形
        cv2.rectangle(frame3,(280,345),(290,355),(0,0,255),1) #画矩形
      

        cv2.rectangle(frame3,(220,140),(230,150),(0,0,255),1) #画矩形 魔方正面 第二排 
        cv2.rectangle(frame3,(220,235),(230,245),(0,0,255),1) #画矩形   
        cv2.rectangle(frame3,(220,345),(230,355),(0,0,255),1) #画矩形
        

        cv2.rectangle(frame3,(165,140),(175,150),(0,0,255),1) #画矩形 魔方正面 第三排
        cv2.rectangle(frame3,(165,235),(175,245),(0,0,255),1) #画矩形
        cv2.rectangle(frame3,(160,340),(170,350),(0,0,255),1) #画矩形
      

       ###魔方 下面 后面
        #cv2.line(frame4, (230, 190), (480, 210), color=(0, 0, 255), thickness=1)
        #cv2.line(frame4, (230, 190), (250, 50), color=(0, 0, 255), thickness=1)
        #cv2.line(frame4, (250, 50), (480, 55), color=(0, 0, 255), thickness=1)
        #cv2.line(frame4, (480, 55), (480, 210), color=(0, 0, 255), thickness=1)
        #cv2.line(frame4, (230, 190), (230, 360), color=(0, 0, 255), thickness=1)
        #cv2.line(frame4, (470, 370), (230, 360), color=(0, 0, 255), thickness=1)
        #cv2.line(frame4, (470, 370), (480, 210), color=(0, 0, 255), thickness=1)


        cv2.rectangle(frame4,(525,130),(535,140),(0,0,255),1) #画矩形 魔方下面 第一排
        cv2.rectangle(frame4,(525,250),(535,260),(0,0,255),1) #画矩形
        cv2.rectangle(frame4,(525,350),(535,360),(0,0,255),1) #画矩形


        cv2.rectangle(frame4,(455,130),(465,140),(0,0,255),1) #画矩形 第二排
        cv2.rectangle(frame4,(455,250),(465,260),(0,0,255),1) #画矩形x
        cv2.rectangle(frame4,(455,370),(465,380),(0,0,255),1) #画矩形

        cv2.rectangle(frame4,(395,130),(405,140),(0,0,255),1) #画矩形 第三排
        cv2.rectangle(frame4,(395,250),(405,260),(0,0,255),1) #画矩形
        cv2.rectangle(frame4,(395,370),(405,380),(0,0,255),1) #画矩形



        cv2.rectangle(frame4,(145,370),(155,380),(0,0,255),1) #画矩形 魔方后面 第一排
        cv2.rectangle(frame4,(145,250),(155,260),(0,0,255),1) #画矩形      
        cv2.rectangle(frame4,(155,130),(165,140),(0,0,255),1)

       # #画矩形
        cv2.rectangle(frame4,(195,370),(205,380),(0,0,255),1) #画矩形 魔方后面 第二排
        cv2.rectangle(frame4,(205,130),(215,140),(0,0,255),1)
        cv2.rectangle(frame4,(195,250),(205,260),(0,0,255),1) #画矩形
       

        cv2.rectangle(frame4,(285,370),(295,380),(0,0,255),1) #画矩形 魔方后面 第三排
        cv2.rectangle(frame4,(285,130),(295,140),(0,0,255),1)
        cv2.rectangle(frame4,(285,250),(295,260),(0,0,255),1) #画矩形
    



        cv2.putText(frame1, 'F', (0, 24), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame2, 'B', (0, 24), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame3, 'UR', (0, 24), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame4, 'LD', (0, 24), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        frame12=np.hstack((frame1, frame2))
        frame34=np.hstack((frame3, frame4))
        frame1234=np.vstack((frame12, frame34))
        frame1234= cv2.resize(frame1234, (960,720))
        cv2.imshow("frame1234",frame1234)
# 获取 色块的 rgb
def getvalue():
    global hsv_save, bgr_save # 保存寻点坐标bgr列表
    bgr_save=[]
    hsv_save=[]
# 上面
    #area1=img3[130:140,460:470]
    #area2=img3[235:245,455:465]
    #area3=img3[340:350,455:465]

    #area4=img3[130:140,400:410]
    #area5=img3[235:245,405:415]
    #area6=img3[345:355,400:410]

    #area7=img3[125:135,330:340]
    #area8=img3[235:245,330:340]
    #area9=img3[345:355,330:340]
#更改后
    area18=img3[140:150,495:505]
    area17=img3[235:245,500:510]
    area16=img3[340:350,495:505]

    area15=img3[135:145,440:450]
    area14=img3[235:245,440:450]
    area13=img3[345:355,440:450]

    area12=img3[135:145,380:390]
    area11=img3[235:245,380:390]
    area10=img3[340:350,375:385]

# 右面
    #area10=img1[240:250,60:70]
    #area11=img1[200:210,110:120]
    #area12=img1[110:120,210:220]

    #area13=img1[320:330,130:140]
    #area14=img1[260:270,200:210]
    #area15=img1[195:205,235:245]

    #area16=img1[380:390,185:195]
    #area17=img1[315:325,245:255]
    #area18=img1[255:265,330:340]

#更改后
    area21=img1[220:230,125:135]
    area24=img1[155:165,200:210]
    area27=img1[85:95,270:280]

    area20=img1[290:300,200:210]
    area23=img1[220:230,270:280]
    area26=img1[145:155,320:330]

    area19=img1[370:380,270:280]
    area22=img1[270:280,320:330]
    area25=img1[235:245,410:420]


#  前面
    #area19=img3[125:135,250:260]
    #area20=img3[235:245,250:260]
    #area21=img3[345:355,250:260]

    #area22=img3[125:135,180:190]
    #area23=img3[235:245,180:190]
    #area24=img3[345:355,180:190]

    #area25=img3[130:140,115:125]
    #area26=img3[235:245,115:125]
    #area27=img3[340:350,120:130]

#更改后
    area3=img3[130:140,280:290]
    area6=img3[235:245,280:290]
    area9=img3[345:355,280:290]

    area2=img3[140:150,220:230]
    area5=img3[235:245,220:230]
    area8=img3[345:355,220:230]

    area1=img3[140:150,165:175]
    area4=img3[235:245,165:175]
    area7=img3[340:350,160:170]


 # 下面
    #area28=img4[67:77,275:285]
    #area29=img4[70:80,350:360]
    #area30=img4[72:82,425:435]

    #area31=img4[112:122,275:285]
    #area32=img4[120:130,350:360]
    #area33=img4[120:130,425:435]

    #area34=img4[157:167,270:280]
    #area35=img4[165:175,350:360]
    #area36=img4[170:180,425:435]
#更改后
    area37=img4[130:140,535:545]
    area38=img4[250:260,535:545]
    area39=img4[350:360,535:545]

    area40=img4[130:140,465:475]
    area41=img4[250:260,465:475]
    area42=img4[370:380,465:475]

    area43=img4[130:140,395:405]
    area44=img4[250:260,395:405]
    area45=img4[370:380,395:405]
# 左面
    #area37=img2[220:230,420:430]
    #area38=img2[295:305,365:375]
    #area39=img2[360:370,305:315]

    #area40=img2[177:187,340:350]
    #area41=img2[245:255,300:310]
    #area42=img2[300:310,245:255]

    #area43=img2[100:110,300:310]
    #area44=img2[195:205,240:250]
    #area45=img2[230:240,170:180]
    #更改后
    area52=img2[250:260,140:150]
    area49=img2[175:185,230:240]
    area46=img2[105:115,285:295]

    area53=img2[310:320,230:240]
    area50=img2[245:255,280:290]
    area47=img2[190:200,355:365]

    area54=img2[380:390,290:300]
    area51=img2[305:315,355:365]
    area48=img2[240:250,430:440]
 # 后面
    #area46=img4[347:357,420:430]
    #area47=img4[343:353,340:350]
    #area48=img4[338:348,270:280]

    #area49=img4[300:310,415:425]
    #area50=img4[290:300,340:350]
    #area51=img4[280:290,265:275]

    #area52=img4[250:260,423:433]
    #area53=img4[240:250,350:360]
    #area54=img4[230:240,270:280]

    area30=img4[370:380,145:155]
    area33=img4[250:260,145:155]
    area36=img4[130:140,155:165]

    area29=img4[370:380,195:205]
    area32=img4[250:260,205:215]
    area35=img4[130:140,195:205]

    area28=img4[370:380,285:295]
    area31=img4[250:260,285:295]
    area34=img4[130:140,285:295]
    Area=[area1,area2,area3,area4,area5,area6,area7,area8,area9,
      area10,area11,area12,area13,area14,area15,area16,area17,area18,
      area19,area20,area21,area22,area23,area24,area25, area26,area27,
      area28,area29,area30,area31,area32,area33,area34,area35,area36,
      area37,area38,area39,area40,area41,area42,area43,area44,area45,
      area46,area47,area48,area49,area50,area51,area52,area53,area54]
    for area in Area:                  
      bgr_save.append(qurgb(area))
      hsv=cv2.cvtColor(area, cv2.COLOR_BGR2HSV)
      hsv_save.append(qurgb(hsv))
   #   print(qurgb(area))
# 对rgb 进行聚类
def read_msg():
    try:
        print("等待接收数据")
        while True:
            data = ser.read(ser.in_waiting).decode('gbk')
            if data != '':
                break
        print("已接受到数据:",data)
    except Exception as exc:
        print("读取异常",exc)    
# 打开串口 
def open_ser():
    global ser
    port = 'com15'  # 串口号
    baudrate = 115200  # 波特率
    try:    
        ser = serial.Serial(port,baudrate,timeout=0.5)
        if(ser.isOpen()==True):
            print("串口打开成功")
    except Exception as exc:
        print("串口打开异常",exc)
# 关闭串口
def close_ser():
        try:
            ser.close()
            if ser.isOpen():
                print("串口未关闭")
            else:
                print("串口已关闭")
        except Exception as exc:
            print("串口关闭异常", exc)
if __name__ == '__main__':
    flag_yichang=0
    flag_a=0
    flag_b=1
    num=0
    open_ser()
    setcapture()
    while True:
       drawline()
       if cv2.waitKey(1) & 0xFF == 32:  

           while num<10:
              num+=1
              getvalue()
              if ver(kmeans_sort(bgr_save,hsv_save)) == 1:
               break
           break
    while 1:       
         if ver(kmeans_sort(bgr_save,hsv_save)) == 0: # 表示识别分类错误了                           
            print("Kmeans Error")  
            if flag_b==1:
             ser.write("ab".encode('utf-8'))
             flag_b=0          
            time.sleep(0.3)
            flag_a=1    
            while True:
              drawline()
              if cv2.waitKey(1) & 0xFF == 32: 
                break
              if flag_a==1:
                  break 
            getvalue() 
         else :          
            Rube_result = sort_go(kmeans_sort(bgr_save,hsv_save))
            if flag_yichang==1:
                  time.sleep(0.3)
                  getvalue()
                  flag_yichang==0
                  continue
                  
            else:
                ser.write("ct".encode('utf-8'))
                for i in Rube_result:
                    ser.write(i.encode('utf-8') + "\n".encode('utf-8'))
                ser.write("\0".encode('utf-8'))
                for i in Rube_result:
                      print(i)
            flag_b=1                 
            while True:
              drawline()
              if cv2.waitKey(1) & 0xFF ==32: 

                break
            getvalue() 
  
    open_ser() #打开串口 等待数据接收  2, 2, 4, 1, 5, 5, 2, 4, 3, 4, 1, 1, 5, 5, 5, 2, 0, 3, 3, 3, 1, 3, 3, 3, 0, 1, 5, 1, 4, 4, 2, 5, 1, 0, 2]
    ##l=[1,1,1,0,0,0,0,0,0,1,1,3,1,1,3,1,1,3,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,0,4,4,0,4,4,0,4,4,5,5,5,5,5,5,5,5,5]
  #  l=[0,1,3,4,4,5,2,5,1,5,3,4,1,1,3,1,4,5,3,1,0,0,2,0,3,2,4,2,4,2,2,0,5,1,0,4,5,1,4,2,3,3,2,0,0,5,2,3,4,5,3,1,5,0]
   
   # l=[0,1,1,2,1,3,4,1,0,1,5,2,5,4,0,5,0,4,1,2,3,2,3,4,3,5,3,4,0,0,0,5,1,5,1,1,5,4,2,3,0,5,2,2,5,0,3,2,3,2,4,3,4,4]
   # l=[3,5,2,0,1,2,2,4,1,4,4,1,1,3,2,0,3,5,0,3,3,3,5,5,1,0,3,3,5,5,1,0,1,0,3,1,4,4,4,0,2,5,5,4,5,4,2,0,1,4,2,2,0,2]
    #l=  [0, 2, 1, 5, 2, 1, 1, 1, 2, 5, 3, 3, 5, 0, 2, 0, 1, 4, 3, 4, 0, 4, 4, 3, 2, 0, 2, 4, 2, 4, 0, 3, 5, 5, 4, 3, 5, 0, 5, 2, 1, 3, 1, 3, 1, 4, 1, 3, 5, 5, 4, 0, 0, 2]
    l= [1, 2, 5, 1, 0, 3, 2, 1, 4, 2, 4, 0, 0, 5, 3, 1, 1, 5, 0, 0, 3, 4, 3, 3, 0, 4, 5, 2, 5, 4, 0, 4, 5, 0, 1, 3, 2, 4, 3, 5, 2, 2, 5, 2, 1, 3, 3, 4, 5, 1, 0, 4, 2, 1]
  #  l= [3, 5, 5, 5, 1, 2, 3, 5, 2, 0, 5, 2, 0, 4, 3, 0, 3, 0, 5, 3, 1, 2, 3, 1, 1, 1, 4, 4, 4, 5, 4, 5, 1, 3, 2, 1, 2, 0, 2, 4, 2, 1, 5, 3, 3, 0, 4, 1, 2, 0, 0, 4, 0, 4]
  #  l=[3, 5, 4, 1, 5, 2, 4, 0, 1, 0, 1, 3, 3, 0, 2, 0, 5, 2, 0, 1, 4, 2, 2, 1, 5, 3, 2, 0, 4, 1, 5, 1, 2, 3, 5, 3, 1, 4, 5, 0, 3, 3, 2, 3, 2, 5, 0, 4, 0, 4, 4, 1, 4, 5]
   # l=[4, 2, 3, 0, 4, 0, 0, 1, 3, 5, 1, 5, 4, 2, 4, 5, 2, 3, 4, 3, 1, 5, 3, 2, 0, 0, 0, 1, 2, 2, 1, 5, 5, 0, 3, 4, 2, 5, 1, 3, 1, 1, 4, 4, 5, 2, 3, 3, 0, 0, 5, 1, 4, 2]
 #   l=[0, 3, 1, 0, 4, 3, 3, 2, 2, 0, 5, 2, 4, 5, 0, 5, 4, 3, 5, 1, 1, 1, 3, 2, 0, 5, 4, 2, 1, 3, 3, 0, 5, 1, 3, 4, 5, 2, 0, 0, 2, 4, 4, 0, 3, 4, 2, 1, 1, 1, 5, 2, 4, 5]
    Rube_result = sort_go(l)
    ser.write("ct".encode('utf-8'))
    for i in Rube_result:
     #  print(i)
       ser.write(i.encode('utf-8') + "\n".encode('utf-8'))
    ser.write("\0".encode('utf-8'))
    close_ser()
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
