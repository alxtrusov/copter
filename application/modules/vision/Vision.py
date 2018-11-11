
#import numpy as np
#import cv2
#import cv2.aruco as aruco

# класс про машинное видение
class Vision:
    def __init__(self, db, mediator):
        self.db = db
        self.mediator = mediator

    #def fire(self):
        #dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        #board = cv2.aruco.GridBoard_create(5, 7, 0.04, 0.01, dictionary)
        #img = board.draw((200*3, 200*3))

        #Dump the calibration board to a file
        #cv2.imwrite('aruco.png',img)
