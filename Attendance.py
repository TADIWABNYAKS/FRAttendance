import maskpass    # pip install maskpass 
import pymongo  # pip install pymongo, pip install pymongo[srv]
import cv2 
import face_recognition  # pip3 install face_recognition AFTER 
import numpy as np 
import os 
from datetime import date

class Attendance():
    def __init__(self, c, d, s):
        self.client = c
        self.day = d.strftime('%A')  # Day of week for tutorial session 
        self.date = d.strftime('%d/%m/%Y')  # Exact date of tutorial 
        self.session = s 
        self.path = 'StudentImages'
        self.session_student, self.student_names = self.getKnownStudents() 
        self.present = [] 
        self.dp = 0.8  # Percentage of tutorials that must be attended in a year for student to have dp 

    def endSession(self):
        record = {
            "Date": self.date,
            "Session": self.session,
            "Attended": self.present
        }
        db = self.client["UCTAttendance"] 
        area = db[self.day]
        try:
            area.insert_one(record)
            print(record)
            print("Done")
        except:
            print("INSERTION OF TUT DATA FAILED")
            print("DATA FOR MANUAL INSERTION")
            print(record)

    def addStudent():
        print("I DON'T WORK YET, ADD pics manually for now")
        pass

    def dpList(): 
        print('I DONT WORK YET')
        pass

    def mark(self): 
        cam = cv2.VideoCapture(0)  # initialize camera 
        title = "Tut: " + self.day + " " + str(self.session)
        while True:
            success, image = cam.read()
            if not success:  # Error handling for camera not working
                print("Camera not detected please connect a camera")
                return 

            compressed_img = cv2.resize(image, (0, 0), None, 0.25, 0.25)  # Scaling image down to 1/4 size to make processing faster
            compressed_img = cv2.cvtColor(compressed_img, cv2.COLOR_BGR2RGB)
            frame = face_recognition.face_locations(compressed_img)
            encodedframe = face_recognition.face_encodings(compressed_img, frame)
            frame_counter = 0  
            frame_interval = 120  # Detect faces every X frames. (For performance)

            for encodface, faceloc in zip(encodedframe, frame):  # Iterate through faces and encoded faces in the 2 lists
                if frame_counter % frame_interval == 0:  # Check if it's time to detect faces
                    matches = face_recognition.compare_faces(self.session_students, encodface)
                    face_distance = face_recognition.face_distance(self.session_students, encodface)  # Face distances to data, where smaller the distance the higher chance of a match
                    matchIndex = np.argmin(face_distance)  # Get match from face distance list
                    y1, x2, y2, x1 = faceloc  # Bounds for person's face
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scaling frame bound up as they were generated using a scaled down
                    
                    if matches[matchIndex]:
                        student_num = self.student_names[matchIndex].upper()  # E.G NYSTAD002
                        # Student found, show that on camera and add them to present list.   
                        if student_num not in self.present:
                            self.present.append(student_num)
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(image, student_num, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)
                     
            cv2.imshow(title, image)
            key = cv2.waitKey(1)
            if key == ord("q"):
                cam.release()
                cv2.destroyAllWindows()
                break
        return

    def encode(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        return encode

    def getKnownStudents(self):
        students = os.listdir(self.path)
        student_names = [] 
        student_encodings = []
        for file in students:
            currentImg = cv2.imread(f'{self.path}/{file}')
            student_encodings.append(self.encode(currentImg))
            student_names.append(os.path.splitext(file)[0])
        return np.array(student_encodings), np.array(student_names)




def connect_to_mongodb():
    while True:
        username = input('Enter username for database\n')
        password = maskpass.askpass(mask="*")
        mongo_str = f'mongodb+srv://{username}:{password}@<YOUR_MONGO_CLUSTER_URI>'
        try:
            client = pymongo.MongoClient(mongo_str)
            client.server_info()  # Test connection to check if details are valid
            return client
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(f"Error during database connection: {err}")
            print("Maybe wrong password?")


def main():
    day = date.today()
    start_time = int(input('Enter start time of session,  Format:HHMM\n'))  # All sessions are assumed to be 2 hrs, so if start is 1400 hrs this is the 1400 to 1600 session
    client = connect_to_mongodb()
    
    attendance = Attendance(client, day, start_time)  # Start instance of attendance object before looping menu to save state
    while True:
        print('*****_____Attendance System_____*****')
        print('1: Take tut attendance')
        print('2: Publish tut attendance')
        print('3: Add new student to session images')
        print('4: Get attendance rate and DP csv (NOT WORKING YET)')
        print('Q: QUIT PROGRAM')
        choice = input("CHOICE: ").upper()
        if choice == '1':
            attendance.mark()
        elif choice == '2':
            attendance.end_session()
        elif choice == '3':
            attendance.add_student()
        elif choice == '4':
            print("NOT WORKING YET")
        elif choice == 'Q':
            print('Great work today (〃￣︶￣)人(￣︶￣〃)')
            break
        else:
            print("Unrecognized command, try again?")
        print("\033[2J\033[H", end="", flush=True)  # Clear terminal

if __name__ == '__main__':
    main()
