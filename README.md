DRONE TRACKER

Course Title: Software Engineering

Course Number: MCIS 6153 Software Engineering

Instructor’s Name: Dr. M. Banisakher

Project Team:

Sriram Rasanollu (999902659)

Pavan Reddy Aavula (999902630)

Venkata Siva Akhil Gupta Chunduri (999901598)

Chaithanya Varma Pandeti (999902006)

Satya Sri Vasavi Chunduri (999901599)



Drone-Tracking

Drone / Unmanned Aerial Vehicle (UAV) Detection is a very safety critical project. It takes in Infrared (IR) video streams and detects drones in it with high accuracy.

Scope:

Real-time Unmanned Aerial Vehicle (UAV) detection system. The objective of the project is to make a real-time embedded drone detection system for a flying vehicle from the infrared data. The model should detect UAV in presence of varying UAV sizes/types, altitudes, distances and lighting conditions.



* Drone vs Bird Classification:

1. A classification model based on trajectory of the drone.
2. Current model predicts both drones and birds with high accuracy as drone so if a trajectory based classification is done it makes drone detection more robust.
3. After brainstorming we came up with the following features:
   1. X-coordinate in terms of pixel
   2. Y--coordinate in terms of pixel
   3. z-coordinate in relation to absolute size of frame with UAV Bounding box size
   4. Curvature of drone at particular frame
   5. Eucledian distance from last frame
4. We trained on ensemble of methods and are yet to find the best model
5. PS: The dataset doesn't include a bird class as it doesn't contain one. We tested this on a custom dataaset. If birds are labelled as seperate class that might also make the model more robust. However, since the size of objects can become extremely small it is better to go with this classification approach.

* Model Optimization:

1. This is one of the most critical part of the project because a full-blown deep learning model cannot run on an embedded device @50 FPS.
2. So model quantization as well as sparsification needs to be done in order to to utilize maximum hardware resources to get the best results.
3. We have tried several optimization techniques as follows:

   1. Deepsparse by Neuralmagic: This is probably one of the best methods that could be employed to our need but it was facing issues in setting up on Jetson TX2

   2. AIMET by Qualcomm: This is another toolkit which is very promising but didn’t got much chance to explore it due to time crunch

1. TAO by Nvidia:: This is a toolkit which can be very fruitful but again didn’t explore it much due to time crunch.

Overview

The overview describes a drone detection and tracking system using YOLO computer vision technology, which will receive video feeds from surveillance cameras, analyze the images to detect and track drones, and generate alerts to notify security personnel of the drone's location and trajectory. The system will have a user interface that allows real-time monitoring, and it will be designed to operate in a distributed manner for scalability and fault tolerance. The main file's routines include initialization, object detection, and object tracking. Python is a suitable programming language for the development of such a system, given its ease of use and the availability of libraries and tools for computer vision and machine learning.