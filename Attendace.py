import maskpass  
from pymongo import MongoClient #pip install pymongo, pip install pymongo[srv]
import cv2 
import face_recognition #pip3 install face_recognition AFTER 
import numpy as np 
import os 
from datetime import date

class Attendance():
    def __init__(self , mongo , d , s):
        #self.client = MongoClient(mongo) ; 
        self.day = d.strftime('%A') #Day of week for tutorial session 
        self.date = d.strftime('%d/%m/%Y') #Exact date of tutorial 
        self.session = s 
        self.path = 'StudentImages'
        self.session_student , self.student_names = self.getKnownStudents();
        self.present = [] 
        self.dp  = 0.8 #Percantage of of tutorials that must be attended in a year for student to have dp 
    '''
    Method uploads session doc to the mongodb session doc comprises of a list of all student nums scanned and verified. And terminates program for the day. 
    doc = { day: , sesh: , users: []}  
    '''
    def endSession(self):

        record= {"Date": self.date ,
                "Session":self.session,
                "Attended":self.present
                }
        
       # db = self.client["UCTAttendance"] #Replace 'UCTAttendance' with db with course code name in live build or a simillar idea
        #This script was created with one course in mind so a course has its own db , but if it becomes massively adpoted have each collection be a course code or something.  
       # area = db[self.day] #Each DB contains approx 5 collections so 1 collections for each day of the week meaning that all Tuesday tuts are stored in the same collection , etc.

        try:
            #area.insert_one(record)
            print(record)
            print("Done")
        except:
            print("INSERTION OF TUT DATA FAILED")
            print("DATA FOR MANUAL INSERTION")
            print(record) # Set up output redirection to file or something for errors , or save record to .csv 
            

    '''
    Method to register student's iamge and their student number. 
    Images stored locally on machine where this script is running, but a solution using S3 to store the pictures and downloading them per sesh can be easily done 
    '''
    def addStudent():
        print("I DON'T WORK YET , ADD pics manually for now")
        pass

    '''
    Method to run query on db and determine the attendace rate of all students in the db , saving them to a .csv file with a flag dp attached to it , where DP : True means the student has dp for the tut attendance part of the course.
    '''
    def dpList():
        print('I DONT WORK YET')
        pass
    
    '''
    Method to mark attendance of students using open cv library 
    '''
    def mark(self): 
        cam = cv2.VideoCapture(0) #initialize camera 
        title = "Tut: "+ self.day +" "+ str(self.session)
        while(True):
            success , image = cam.read()
            compressed_img = cv2.resize(image,(0,0),None,0.25,0.25 )#   Scalling image down to 1/4 size to make processing faster
            compressed_img = cv2.cvtColor(compressed_img , cv2.COLOR_BGR2RGB)
            frame = face_recognition.face_locations(compressed_img)
            encodedframe= face_recognition.face_encodings(compressed_img,frame , model='small')

            for encodface,faceloc in zip(encodedframe,frame): #Iterate through  faces and encoded faces in the 2 lists
                matches = face_recognition.compare_faces(self.session_student ,encodface)
                face_distance = face_recognition.face_distance(self.session_student,encodface) #Face distances to data , where smaller the distance the higher chance of a match
                matchIndex = np.argmin(face_distance) #Get match from face distance list
                y1,x2,y2,x1 =  faceloc #Bounds for person's face
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4 #Scalling frame bound up as they were generated using a scaled down
                
                if matches[matchIndex]:
                     student_num = self.student_names[matchIndex].upper() #E.G NYSTAD002
                     #Student found , show that on camera and add them to present list.   
                     if student_num not in self.present:
                          self.present.append(student_num)
                     cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
                    # cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)
                     cv2.putText(image,student_num,(x1+6 , y2-6) , cv2.FONT_HERSHEY_TRIPLEX,1,(255,255,255) ,2)
                     
            cv2.imshow(title , image)
            key = cv2.waitKey(1)
            if key == ord("q"):
                 cam.release()
                 cv2.destroyAllWindows()
                 break
        return
        
    def encode(self , image):
         image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
         encode  = face_recognition.face_encodings(image,model='small')[0]
         return encode

    def getKnownStudents(self):
        students = os.listdir(self.path) ; 
        student_names = [] 
        student_encodings = [] 
        for file in students:
            currentImg = cv2.imread(f'{self.path}/{file}')
            student_encodings.append(self.encode(currentImg))
            student_names.append(os.path.splitext(file)[0])
        return student_encodings ,student_names
    




'''
    Main method for attendace script , tutor enters session details for the day , and makes connection to db using private password reserved for them.
    Launces instance of Attendance object which then runs for the marking 
'''
def main():
  day = date.today()
  start_time = int(input('Enter start time of session,  Format:HHMM\n')) #All sessions are assumed to be 2 hrs , so if start is 1400 hrs this is the 1400 to 1600 session
  username = input('Enter username for database\n')
  password = maskpass.askpass(mask="*")
  user_and_pass = username + ':'+ password 
  mongo = 'mongodb+srv://'+user_and_pass+'INSERT YOUR DATABASE CONNECTION HERE '
  
  tut = Attendance(mongo, day , start_time) 
  #INSERT MENU HERE 
  while(True):
       print('*****_____Attendance System_____*****')
       print('1: Take tut attendance')
       print('2: Publish tut attendance')
       print('3: Add new student to session images')
       print('4: Get attendance rate and DP csv')
       print('Q: QUIT PROGRAM')
       i = input("CHOICE:").upper()
       if i == '1':
           tut.mark()
       elif i == '2':
           tut.endSession()
       elif i == '3':
           tut.addStudent()
       elif i == "q":
          print('Great work today (〃￣︶￣)人(￣︶￣〃)')
          quit()
          
       else:
           print("unrecognised command try again?")
     #  print("\033[2J\033[H", end="", flush=True) # Clear terminal


if __name__ == '__main__':
     main();