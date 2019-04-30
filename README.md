# EC544-Smart-Doorbell

The goal of our project is to build a secure smart doorbell. There are several similar products like Dropcam, Nest Cam Indoor which are able to help you look after your home and family even when you are not at home. While these products are expensive and they may not have some of the function that we want. What if we want a smart doorbell that it can recognize the person who is pressing the doorbell, and in our database, this person has access, then door will open automatically. And if we can not find the person in our database, the Pi will send the image to user’s phone and user can send a signal to the door and open the door.

## Work flow
< img src="./proposal diagram.jpg" width="180" height="200" style="width:80%">

user press button(knock at the door) -> IoT buton send signal to AWS topic -> Pi get signal from the topic -> trigger OpenCV  facial recognition to detect whether this is the person that we want to open the door for -> If successfully recognize -> sent signal to AWS topic -> frdm board get signal from topic -> green light(Open the door)

## Implementation
### IoT button
We are using AWS MQTT channel to communicate to Pi. For the button’s lambda function, when the button is pressed, it will send  string “RUN”  to our topic (freerots/demos/echo).
For using IoT button, you need to download key, certificates from AWS and configure them into your button. And In lambda function, you need to define your endpoint, the topic you want to publish and the payload which is the message that you want to publish to topic.
If you set up things above, you are able to sent signal to AWS topic.
### Raspberry Pi
If you also want the Pi to receive message from the topic, you need to add new thing Pi in your AWS console. And also download the key and certificates. We are using AWSIoTPythonSDK which will get signal and sent signal to the topic that you subscribe. And you need to define your endpoint, certificate path, key path and the topic that you want to subscribe.
We are using cuntomCallback() to receive the message from MQTT topic. If the message we get from the topic is “RUN” which is sent by the button, we will trigger OpenCV and recognize the person. We are using Pi camera to capture the video. There is already a trained dataset, if the person matches one of the person in our database, it will send a signal to  myAWSIoTMQTTClient.publish() which will publish message to MQTT topic. We are publishing “SINGLE” to the topic.
### Freedom board K64F
For freedom board, we are using C SDK to receive message from MQTT topic, which is the same topic channel as before(freertos/demos/echo) . If the message freedom board gets equals to “SINGLE” the same as Pi published, it will turn the green light on, which means opens the door.

## Files Description
01_face_dataset.py, 02_face_training.py, 03_face_recognition.py and haarcascade_frontalface_default.xml. 
These files can help you build up your own dataset and model. The model generated named trainer.yml should be placed in trainer folder.

lambda.js is a nodejs file which should be set up in AWS IoT lambda function.

frdmk64f_aws_device_configuration_enet is a folder of configuration of freedom board.

## Run the code
Unzip frdmk64f_aws_device_configuration_enet.zip and REPLACE the origin files.

Python subscribe.py (before that, add the paths of your own certificate, key, RootCA... into line #15 to #22).

Press IoT button. 

If Picamera recognizes the person, the light of freedom board will turn green.
