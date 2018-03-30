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

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
args = vars(ap.parse_args())

EYE_CLOSE_TIMES  = 2
MOUTH_OPEN_TIMES = 2
ABNORMAL_TIMES   = 2

# initial distance on face
dist_btw_eyes    = -1
dist_btw_nose    = -1
slope_btw_eyes   = -1

# initial current user
user = None

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
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
         
    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `p` key was pressed, then complete initialize
    if key == ord("p"):
        dist_btw_eyes, dist_btw_nose, slope_btw_eyes = myDetector.initial(shape)
        cv2.imwrite("user.jpg", frame) 
        print("[INFO] Initial Complete")
        break
    
time.sleep(1.0)

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
            blink_detected = True
        elif not eye_close:
            blink_detected = False
            
        if timer_now - timer_freq >= 10:
            print(blink_frequency)
            timer_freq = timer_now
            blink_frequency = 0

        # if the eye close for more than 2 seconds,
        # print sleepy message
        timer_sleepy = myDetector.update_timer(eye_close, timer_sleepy)
        if timer_now - timer_sleepy >= EYE_CLOSE_TIMES and timer_sleepy > 0:
            print("sleepy detected")
            timer_sleepy = 0
        
        # if the mouth open for more than 2 seconds,
        # print yawn message
        timer_yawn = myDetector.update_timer(mouth_open, timer_yawn)  
        if timer_now - timer_yawn >= MOUTH_OPEN_TIMES and timer_yawn > 0:
            print("yawn detected")
            timer_yawn = 0

        # see if abnormal pos detected
        timer_abnormal = myDetector.update_timer(abnormal, timer_abnormal)
        if timer_now - timer_abnormal >= ABNORMAL_TIMES and timer_abnormal > 0:
            print("abnormal pos detected")
            timer_abnormal = 0
         
    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if 't' is pressed, see if other person come
    if key == ord("t"):
      while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        cv2.imshow("Frame", frame)
        cv2.imwrite("unknown.jpg", frame)
        user_image = face_recognition.load_image_file("user.jpg")
        unknown_image = face_recognition.load_image_file("unknown.jpg")
        print("unknown_image")
        if type(unknown_image) != type(None):
          user_encoding = face_recognition.face_encodings(user_image)[0]
          unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
          result = face_recognition.compare_faces([user_encoding], unknown_encoding)
          print(result)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("t"):
          break

    # if 'q' is pressed, break from the loop
    if key == ord("q"):
        cv2.destroyAllWindows()
        break
 
# do a bit of cleanup
vs.stop()
exit()
