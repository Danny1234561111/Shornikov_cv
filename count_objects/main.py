import cv2
import zmq
import numpy as np
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE,b"")

global position
position=None

port = 5555
socket.connect("tcp://192.168.0.100:%s" % port)
cv2.namedWindow("Client-recv",cv2.WINDOW_GUI_NORMAL)


flimit=20
slimit = 20

def fupdate(value):
    global flimit
    flimit=value
def supdate(value):
    global slimit
    slimit=value

cv2.namedWindow("Mask",cv2.WINDOW_GUI_NORMAL)
cv2.createTrackbar("F","Mask",flimit,255,fupdate)
cv2.createTrackbar("S","Mask",slimit,255,supdate)

massiv=[]
while True:
    chet_rect = 0
    chet_circle = 0
    msg = socket.recv()
    frame = cv2.imdecode(np.frombuffer(msg,np.uint8),-1)

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    gray =cv2.GaussianBlur(gray,(7,7),0)
    mask = cv2.erode(gray, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    countours = cv2.Canny(mask,flimit,slimit)
    fcountours, hierarchy = cv2.findContours(countours,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cnts, _ = cv2.findContours(countours, cv2.RETR_EXTERNAL,  cv2.CHAIN_APPROX_SIMPLE)

    for i,countor in enumerate(fcountours):
        if cv2.contourArea(countor)>120:
            rect = cv2.minAreaRect(countor)
            box = cv2.boxPoints(rect)
            box = np.int64(box)
            if cv2.contourArea(box)<=cv2.contourArea(countor)+220:
                chet_rect+=1
            else:
                chet_circle+=1
            cv2.drawContours(frame, [box], 0, (255, 255, 0), 2)

    # cv2.drawContours(frame,fcountours,-1,(255,255,255),3)
    cv2.putText(frame, f"count_rect - {chet_rect}, count_circle - {chet_circle}", (100,100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 3)
    cv2.imshow("Camera-recv", frame)
    cv2.imshow("Mask", countours)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
# green - 60-70 (80-120)(170-180) red 0-10

cv2.destroyAllWindows()
