from scipy.spatial import distance as dist
import numpy as np
import time

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

def initial(shape):
    # dist between eyes
    A = dist.euclidean(shape[36], shape[45])
    # dist between nose
    B = dist.euclidean(shape[27], shape[33])
    # slope of line between eyes
    C = (shape[45][1] - shape[36][1]) / (shape[45][0] - shape[36][0])

    return A, B, C

def pos(shape, dist_btw_eyes, dist_btw_nose, slope_btw_eyes):
    A, B, C = initial(shape)
    if C < -0.087 or C > 0.087:
        return True
    if A/B < 0.8*(dist_btw_eyes/dist_btw_nose):
    # if B < 0.85*dist_btw_nose
        return True
    if A > 1.2*dist_btw_eyes:
        return True

def update_timer(state, timer_state):
    if state and timer_state < 0:
        return time.time()
    elif not state:
        return -1
    return timer_state
