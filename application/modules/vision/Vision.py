import numpy as np
import cv2
from cv2 import aruco
import glob

'''
from Vision import Vision

v = Vision(None, None, 0.3)
while (True):
    print(v.fire())
'''

# класс про машинное видение
class Vision:
    def __init__(self, db, mediator, settings):
        self.db = db
        self.mediator = mediator
        self.TYPES = mediator.getTypes()
        self.markerSize = settings['MARKER_SIZE']  # Размер маркера в метрах
        self.cap = cv2.VideoCapture(0)


        '''
        For example, I can check the frame width and height by cap.get(3) and cap.get(4). 
        It gives me 640x480 by default. 
        But I want to modify it to 320x240. Just use ret = cap.set(3,320) and ret = cap.set(4,240).
        '''

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6 * 7, 3), np.float32)
        objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.
        images = glob.glob(settings['PATH_TO_CALIBRATE_IMAGES'])
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
            # If found, add object points, image points (after refining them)
            if ret:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)
        self.ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        # тут должен быть while, который скриншотит камеру, но не вешает сервак!!!
        print(self.fire())

    def fire(self):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
        tvec = []
        if np.all(ids):
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[0], self.markerSize, self.mtx, self.dist)
            # (rvec-tvec).any() # get rid of that nasty numpy value array error

        self.mediator.call(self.TYPES['CAMERA_IMAGE_CAPTURE'], cv2.imencode(".jpg", frame))

        return tvec        
