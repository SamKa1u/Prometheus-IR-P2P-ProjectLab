#   Prometheus Lighting System

A [TTU Whitacre College of Engineering](https://www.depts.ttu.edu/coe/) ECE-3338 lab project \
 <img src = 'Images/dbl_T.png'/>

## Description

The Prometheus Lighting system is a light control system that leverages computer vision software to perform gesture detection. It relies on an infrared point to point communication system to transmit gestures detected by the main unit (Pi-5) to the control unit (Arduino Mega) of an LED strip.​

### Dependencies

* OpenCV
* ultralytics
  
### Overview
<img src = 'Images/prometheus_block_diagram.png' />

### Hardware

#### Master controller
* Raspberry pi 5
* Arducam
* NodeMCU ESP12E 
* Custom-built IR emitter \
  <img src = 'Images/master_unit.jpeg' style=" width:445;height:250px;"/> 
  
#### Light control unit
* Custom-built IR receiver 
* Arduino mega
* LED lightstrip \
   <img src = 'Images/LED_controller.jpeg' style=" width:445;height:250px;" />

### Software

#### Model Training
* [Training pipeline](https://github.com/SamKa1u/YOLO-Transfer-Learning)
* Results:
<div class= 'flex-cols'>
 <img src = 'Images/F1_curve.png' style=" width:445;height:250px;"/> 
 <img src = 'Images/confusion_matrix.png' style=" width:445;height:250px;"/>
 <img src = 'Images/results.png' style=" width:445;height:250px;"/>
</div>

#### GUI
 <img src = 'Images/gui.jpeg'/> 

## Meet The Team

Samuel Kalu <sub>(CV software development)</sub>
  
* Email : [samkalu@ttu.edu](mailto:samkalu@ttu.edu)
* [Linkedin](https://www.linkedin.com/in/samuel-kalu-74a359342/)

Aiden Zsebenyi <sub>(Software and Hardware development: IR reciever)</sub>
* Email : [azsebeny@ttu.edu](mailto:azsebeny@ttu.edu)

Michael Dec  <sub>(Hardware development: IR emitter)</sub>
* Email : [mdec@ttu.edu](mailto:mdec@ttu.edu)

## Acknowledgments

### Special thanks to Professor Everret Mcarthur
Inspiration, code snippets, etc.
* [TTU WCOE ECE Department](https://www.depts.ttu.edu/ece/)
* [Learnopencv](https://learnopencv.com/face-detection-opencv-dlib-and-deep-learning-c-python/#:~:text=We%20notice%20that%20the%20OpenCV,along%20with%20the%20bounding%20box.)
* [Label Studio](https://labelstud.io/guide/export)
* [Ultralytics](https://docs.ultralytics.com/guides/raspberry-pi/#set-up-ultralytics)
* [Edje Electronics](https://www.ejtech.io/learn/train-yolo-models)
* [Tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter)
* [Raspberry pi](https://www.raspberrypi.com/software/)
* [Bro Code](https://www.youtube.com/watch?v=STEOavXqXkQ&ab_channel=BroCode)
* [Gpiozero docs](https://gpiozero.readthedocs.io/en/latest/api_output.html)
  
