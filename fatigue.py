# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import face_recognition
import myDetector
import json
import os
import ASUS.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.ASUS)
SENSE = 257
GPIO.setup(SENSE, GPIO.IN)
key = 0

EYE_CLOSE_TIMES  = 2
MOUTH_OPEN_TIMES = 2
ABNORMAL_TIMES   = 2

# initial distance on face
dist_btw_eyes    = -1
dist_btw_nose    = -1
slope_btw_eyes   = -1

icon = cv2.imread("./1.png")

# initial current user
user_image = None
user_encoding = None

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# initialize the value
blink_frequency  = 0
blink_detected   = False
sleepy           = False
yawn             = False
abnormal         = False

# initialize some time variables
timer_freq       = time.time()
timer_sleepy     = -1
timer_yawn       = -1
timer_abnormal   = -1

i = 0
data = {"frequency" : 0, "close_eye" : 'n', "yawn" : 'n', "posture" : 'n', "unknown" : 'n'}
final = ""

class Timeout(Exception):
    pass

def handler(signum, frame):
    raise Timeout

signal.signal(signal.SIGALRM, handler)

vs = VideoStream(src=0)
vs.start()

def initial():
  time.sleep(1.0)
  while True:
      # grab the frame from the threaded video file stream, resize
      # it, and convert it to grayscale channels)
      frame = vs.read()
      frame = imutils.resize(frame, width=450)
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      # detect faces in the grayscale frame
      rects = detector(gray, 0)

      # loop over the face detections
      for rect in rects:
          # determine the facial landmarks for the face region, then
          # convert the facial landmark (x, y)-coordinates to a NumPy
          # array
          shape = predictor(gray, rect)
          shape = face_utils.shape_to_np(shape)           

      # if the `p` key was pressed, then complete initialize
      if key != GPIO.input(SENSE):
          global key 
          key = GPIO.input(SENSE)
          cv2.imwrite("user.jpg", frame)
          try:
            global user_image
            user_image = face_recognition.load_image_file("user.jpg")
            global user_encoding
            user_encoding = face_recognition.face_encodings(user_image)[0]
            global dist_btw_eyes, dist_btw_nose, slope_btw_eyes 
            dist_btw_eyes, dist_btw_nose, slope_btw_eyes = myDetector.initial(shape) 
            print("[INFO] Initial Complete")
            global timer_freq
            timer_freq       = time.time()
            global timer_sleepy
            timer_sleepy     = -1
            global timer_yawn
            timer_yawn       = -1
            global timer_abnormal
            timer_abnormal   = -1
            return
          except IndexError:
            print("[INFO] Initial Failed. Try Again.")
            pass         

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

initial()    
time.sleep(1.0)
# loop over frames from the video stream
while True:
    timer_now = time.time()
    
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale channels)
    frame = vs.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # extract the left eye, right eye and mouth coordinates
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        mouth = shape[mStart:mEnd]

        # see if blink/mouth_open/abnormalPos detected 
        eye_close = myDetector.blink_detector(leftEye, rightEye)
        mouth_open = myDetector.mouth_open_detector(mouth)
        abnormal = myDetector.pos(shape, dist_btw_eyes, dist_btw_nose,
                                  slope_btw_eyes)                           
        
        # compute blink frequency
        if eye_close and not blink_detected:
            blink_frequency += 1
            print(blink_frequency)
            blink_detected = True
        elif not eye_close:
            blink_detected = False

        if timer_now - timer_freq >= 60:
            if blink_frequency >= 99:
              data["frequency"] = 99
            else:
              data["frequency"] = blink_frequency
            final = json.dumps(data)
            with open("detect.txt", 'w') as f:
              f.write(final) 
            data["frequency"] = 0
            data["close_eye"] = 'n'
            data["yawn"] = 'n'
            data["posture"] = 'n'
            final = ""
            timer_freq = timer_now
            blink_frequency = 0
        
        # if the eye close for more than 2 seconds,
        # print sleepy message
        timer_sleepy = myDetector.update_timer(eye_close, timer_sleepy)
        if timer_now - timer_sleepy >= EYE_CLOSE_TIMES and timer_sleepy > 0:
            data["close_eye"] = 'y'
            print("eye_close")
            timer_sleepy = 0
        
        # if the mouth open for more than 2 seconds,
        # print yawn message
        timer_yawn = myDetector.update_timer(mouth_open, timer_yawn)  
        if timer_now - timer_yawn >= MOUTH_OPEN_TIMES and timer_yawn > 0:
            data["yawn"] = 'y'
            print("yawn")
            timer_yawn = 0

        # see if abnormal pos detected
        timer_abnormal = myDetector.update_timer(abnormal, timer_abnormal)
        if timer_now - timer_abnormal >= ABNORMAL_TIMES and timer_abnormal > 0:
            data["posture"] = 'y'
            print("posture")
            timer_abnormal = -1

    # if 't' is pressed, see if other person come
    if key != GPIO.input(SENSE):
      key = GPIO.input(SENSE)
      print("[INFO] unknown detecting starts") 
      time.sleep(1.0)
      timer_freq = time.time()     
      faces = [ user_encoding ]
      while True:
        timer_now = time.time()
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        cv2.imshow("icon", icon)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        
        if len(rects) > 0:
          filename = "unknown" + str(i) + ".jpg"
          cv2.imwrite(filename, frame)
          unknown_image = face_recognition.load_image_file(filename)          
          try:
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            result = face_recognition.compare_faces(faces, unknown_encoding, tolerance = 0.4)
            if result[0] == False:
               data["unknown"] = 'y'
               print("unknown detected")
               check = True
               for j in range(len(result)):
                  if result[j] == True:
                     check = False
                     break
               if check:
                  i += 1                  
                  print("unknown recorded")
                  faces.append( unknown_encoding )
          except IndexError:
            pass          
          
        if timer_now - timer_freq >= 60:
            final = json.dumps(data)
            with open("detect.txt", 'w') as f:
              f.write(final)
            data = {"frequency" : 0, "close_eye" : 'n', "yawn" : 'n', "posture" : 'n', "unknown" : 'n'}
            final = ""
            timer_freq = timer_now
         
        if key != GPIO.input(SENSE):
          key = GPIO.input(SENSE)
          os.remove(filename)
          i -= 1
          print("[INFO] unknown detecting ends")
          initial()
          time.sleep(1.0)
          break
 
# do a bit of cleanup
vs.stop()
exit()