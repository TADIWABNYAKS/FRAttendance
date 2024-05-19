# FR Attendance

Attendance system for university tutorials that uses facial recognition to mark student attendace , and get a list of students who have met the course's required minimum attendance.
### WARNING⚠️: This project is currently under development so not all features have been implemented and testing is still under progress 

## Prerequisites

The script has the following external libraries: maskpass , pymongo , open_cv , face_recognition and numpy to install the use the following pip commands 
```
pip install pymongo[srv]
pip install face_recogntion #NB: As this library uses C++ algos ,you're gonna need Cmake to install this
pip install maskpass
pip install opencv-python
pip install numpy
```

## How to use 

To implement , replace the mongo string in the main method with your own, and the database name and you should be good to go provided the database exists and you supply valid credentials. 

In addition to that you need pictures of all the students in the session in a subdirectory called 'StudentImages' and have the name of each image be how you want to identfify the student in the database , perhabs student number? 

 Other than that , use is as simple as following the text based UI housed in the main method. 
