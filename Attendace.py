import maskpass  
from pymongo import MongoClient #pip install pymongo, pip install pymongo[srv]


class Attendance():
    def __init__(self , mongo , d , s):
        self.db = MongoClient(mongo) ; 
        self.day = d;
        self.session = s ;
    

    '''
    Method uploads session doc to the mongodb session doc comprises of a list of all student nums scanned and verified. And terminates program for the day. 
    doc = { day: , sesh: , users: []}  
    '''
    def sessionEnd():
        print("I DON'T WORK YET")
        pass
    

    '''
    Method to register student's iamge and their student number. 
    Images stored locally on machine where this script is running, but a solution using S3 to store the pictures and downloading them per sesh can be easily done 
    '''
    def addStudent():
        print("I DON'T WORK YET")
        pass

    '''
    Method to mark attendance of students using open cv library 
    '''
    def mark(): 
        print("I DON'T WORK YET")
        pass
    
    
    '''
     Method produces attendance for all students in all tut sessions in the db 
     HAS NOT BEEN IMPLEMENTED YET.
    '''
    def attendace():
        print("I DON'T WORK YET")
        pass





'''
Main method for attendace script , tutor enters session details for the day , and makes connection to db using private password reserved for them.
Launces instance of Attendance object which then runs for the marking 
'''
def main():
     
  day_of_week = input('Enter the day of your session\n')
  start_time = int(input('Enter start time of session,  Format:HHMM\n')) #All sessions are assumed to be 2 hrs , so if start is 1400 hrs this is the 1400 to 1600 session
  username = input('Enter username for database\n')
  password = maskpass.askpass(mask="*")
  user_and_pass = username + ':'+ password 
  mongo = 'mongodb+srv://'+user_and_pass+'INSERT YOUR DATABASE CONNECTION HERE '

  tut = Attendance(mongo, day_of_week , start_time) 
#   INSERT MENU HERE 
#   while(True):
#       print('*****_____Attendance System_____*****')


if __name__ == '__main__':
     main();