import numpy
import cv2

def matrix(width, height, xcompressfactor, ycompressfactor):
    
    x1 = (xcompressfactor/2)*width
    x2 = width-x1
    newheight = height*ycompressfactor
    oldpoints = numpy.float32([[0,0],[width,0],[0,height],[width,height]])
    newpoints = numpy.float32([[x1,0],[x2,0],[0,newheight],[width,newheight]])
    matrix = cv2.getPerspectiveTransform(oldpoints, newpoints)
   
    return matrix

m = None

def transform(img, width, height, xcompressfactor, ycompressfactor):
    
    global m

    if m is None:

        m = matrix(width, height, xcompressfactor, ycompressfactor)
 
    newimg = cv2.warpPerspective(img, m, (width,height))
    
    return newimg
