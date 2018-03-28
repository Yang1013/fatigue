from scipy.spatial import distance as dist
import numpy as np

EYE_THRESH = 0.2
MOUTH_THRESH = 0.2

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear

def blink_detector(leftEye, rightEye):
    # compute ear
    leftEAR  = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    ear = (leftEAR + rightEAR) / 2.0
    # check if ear is below the blink threshold
    if ear < EYE_THRESH:
        return True
    else:
        return False

def mouth_aspect_ratio(mouth):
    # compute the euclidean distances between the horizontal
    # mouth landmark (x, y)-coordinates
    A = dist.euclidean(mouth[12], mouth[16])
    
    # compute the euclidean distances between the vertical
    # mouth landmark (x, y)-coordinates
    B = dist.euclidean(mouth[14], mouth[18])
    mar = B / A
    return mar

def mouth_open_detector(mouth):
    mar = mouth_aspect_ratio(mouth)
    if mar > MOUTH_THRESH:
        return True
    else:
        return False
