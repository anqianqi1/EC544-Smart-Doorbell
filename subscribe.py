import os
import sys
import AWSIoTPythonSDK

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import argparse
import json
#import recognition as recog

import cv2
import numpy as np
import os 

host = "a2ccd2xwv31ide-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "AmazonRootCA1.pem"
certificatePath = "86fbd1be14-certificate.pem.crt"
privateKeyPath = "86fbd1be14-private.pem.key"
port = 8883
clientId = "pi"
topic = "freertos/demos/echo"   #subscribe
topic2 = "freertos/demos/echo"  #publish

flag = 0
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    global result
#    download()
#    result = valid_photo()
    #print(type(message.payload))
    #print(result)
    global flag
    if(message.payload=='RUN'):
        flag = 1
#        while True:
#            ret, img =cam.read()
#            if (recognition(img) == True):
#                flag = 1
#                print(recognition(img))
#                break
#        recog.recognition
        
    #myAWSIoTMQTTClient.unsubscribe(topic)
    #myAWSIoTMQTTClient.disconnect()






myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(50)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)


# Publish to the same topic in a loop forever
loopCount = 0

#
#if (flag==1):
#    message_to_print ='SINGLE'
#        #result
#    message = {}
#    message['result'] = message_to_print
#    messageJson = json.dumps(message)
#    myAWSIoTMQTTClient.publish(topic2, message_to_print, 1)
#    myAWSIoTMQTTClient.unsubscribe(topic)
#    myAWSIoTMQTTClient.disconnect()


#while True:
#    ret, img =cam.read()
#    if (recog.recognition(img) == True):
#        flag = 1
#        print(recog.recognition(img))
#        break

#opencv
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0
c = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Lekai', 'Sichi', 'A', 'B', 'C'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

def recognition(img):
    ret, img =cam.read()
    #img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 90):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            global c
            c=True
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img)
    return c



#board

#if flag == 1:
#    while True:
#        ret, img =cam.read()
#        if (recognition(img) == True):
#            flag = 2
#            print(recognition(img))
#            break

while True:
    
    if flag == 1:
        while True:
            ret, img =cam.read()
            if (recognition(img) == True):
                flag = 2
                print(recognition(img))
                break

    if flag ==2:

        message_to_print ='SINGLE'
        #result
        message = {}
        message['result'] = message_to_print
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(topic2, message_to_print, 1)
        flag = 0
        # myAWSIoTMQTTClient.unsubscribe(topic)
        # myAWSIoTMQTTClient.disconnect()
    else:
        time.sleep(1)
