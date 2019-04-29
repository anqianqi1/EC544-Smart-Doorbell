# EC544-Smart-Doorbell

The goal of our project is to build a secure smart doorbell. There are several similar products like Dropcam, Nest Cam Indoor which are able to help you look after your home and family even when you are not at home. While these products are expensive and they may not have some of the function that we want. What if we want a smart doorbell that it can recognize the person who is pressing the doorbell, and in our database, this person has access, then door will open automatically. And if we can not find the person in our database, the Pi will send the image to user’s phone and user can send a signal to the door and open the door.

## work flow
user press button(knock at the door) -> IoT buton send signal to AWS topic -> Pi get signal from the topic -> trigger OpenCV to facial recognition to detect whether this is the person that we want to open the door for -> If successfully recognize -> sent signal to AWS topic -> frdm board get signal from topic -> light green light(Open the door)

## implementation
