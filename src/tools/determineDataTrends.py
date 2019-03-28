"""
   Copyright 2017 Charlie Liu and Bryan Zhou

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import numpy

# Apply a linear regression to the x data and find the range of the y data to compare those values against pre-determined values for determining a gesture
# this is the file that will determine the gesture

'''
Algo : Create a slope of X and Y values
non 0 data will be recorded. once the next 0 is reached, the data array will be created. then i can use the length of the data as x axis
when evaluating yData to see if gesture is left or right:
    A predetermined array of xAxis[0-255]? will be used as x axis and and yData will be used as y axis
'''
def determineDataTrends(xData, yData, xDataThreshold, yDataThreshold):

    # Static X Axis to create slope
    xAxis = []
    

    for i in range(1, len(xData) + 1):

        xAxis.append(i)
    
    if len(xData) > 0:
    
        xSlope = numpy.polyfit(xAxis, xData, 1)[0]

    yRange = max(yData) - min(yData)
    xRange = max(xData) - min(xData)
    print ("max " + str(max(xData)))
    print ("min " + str(min(xData)))
    
    for i in range(0, len(xData)):
        print (xData[i])
    

    if xSlope < -xDataThreshold:

        gestureDetected = "up"
    
    elif xSlope > xDataThreshold:

        gestureDetected = "down"

    elif yRange > yDataThreshold:

        gestureDetected = "left"

        #elif xRange > yDataThreshold:

        gestureDetected = "right"

    else:

        gestureDetected = None
    
    return gestureDetected
