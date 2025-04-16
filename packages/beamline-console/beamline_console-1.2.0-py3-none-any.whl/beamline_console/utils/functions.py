#!/usr/bin/env python

# ----------------------------------------------------------------------
# Author:        Sebastian Piec <sebastian.piec@desy.de>
# Last modified: 2015, April 9
# ----------------------------------------------------------------------

import datetime
import inspect
import logging
import os
import re
import uuid

# only for curr date??? TODO

from PyQt5 import QtWidgets, QtCore

# ----------------------------------------------------------------------
def _makeRange(startStr, endStr, stepStr):
  """
  """
  fromValue = float(startStr)
  toValue = float(endStr)
  valueStep = float(stepStr)

  targetPositions = []

  if abs(valueStep) < 0.0000000001:
    raise RuntimeError("Parameter's step must be non-zero!")
     
  if valueStep > 0:
    while fromValue < toValue:
      targetPositions.append(round(fromValue, 6))     # think on round() TODO!
      fromValue += valueStep
        
  elif valueStep < 0:
    while fromValue > toValue:
      targetPositions.append(round(fromValue, 6))
      fromValue += valueStep

        # include last value? TODO
  if abs(fromValue - toValue) < 0.0000000001:
    targetPositions.append(round(toValue, 6))
   
  return targetPositions



def modificationDate(filename):
  t = os.path.getmtime(filename)
  return datetime.datetime.fromtimestamp(t)



# ----------------------------------------------------------------------
def niceFloat(number):
  """
  """
  strep = str(number)
  return strep.rstrip("0").rstrip(".") if "." in strep else strep



# is postfix used? TODO
# ---------------------------------------------------------------------- 
def generateUniqueName(baseName, usedNames, postfix=""):
  """Generate name unique within "usedNames" name for Region, RegionGroup, etc.
  different from names present in "usedItems".
  """
  baseName += postfix    # e.g. " - Copy"
  newName = baseName
    
  copyCnt = 1
    
  while True:
    isClashing = any([newName == usedName for usedName in usedNames])
      
      # try another name 
    if isClashing:
      newName = baseName + f" ({copyCnt})"
      copyCnt += 1 
    else:
      return newName
       


# ---------------------------------------------------------------------- 
def script_info():
  """ 
  """ 
  from inspect import currentframe, getframeinfo
  
  frameinfo = getframeinfo(currentframe())
  return "%s, line: %d" % (frameinfo.filename, frameinfo.lineno)




# ---------------------------------------------------------------------- 
def makeTimeStamp(dateTime):
  """ Return string representation of QDateTime object.
  """
  format = "yyyy_MM_dd_hhmmss"
  return dateTime.toString(format)
 

# ---------------------------------------------------------------------- 
def _extractRealBase(baseName):
  """ In case there is time stamp, don't append next one...

  tmp_spiec - with this dir will not work...
  """
  tokens = baseName.split("_")
  
    # no timestamp
  if len(tokens) < 5:
    return baseName

  nTokens = len(tokens)

  if re.match(r"\d{6}", tokens[-1]) and re.match(r"\d{2}", tokens[-2]) and \
      re.match(r"\d{2}", tokens[-3]) and re.match(r"\d{4}", tokens[-4]):
      #print (">>>>>>>>>>>>>>>>> FOUND TIME_STAMP, ", tokens[0:nTokens-4])
      return "".join(tokens[0:nTokens-4])

  return baseName
    

      
# ---------------------------------------------------------------------- 
def fileNameWithStamp(fileName, replace=False):
  """If fileName already contains "time stamp" do nothing.
  """
  baseName, fileExtension = os.path.splitext(fileName)

    # possibly substitute previous time stamp
  newBaseName = _extractRealBase(baseName)

    # either "no time stamp" or "user wants to replace it"
  if newBaseName == baseName or replace:
    currentDate = QtCore.QDateTime.currentDateTime()

    fileName = newBaseName + "_" + makeTimeStamp(currentDate) + fileExtension
  
  return fileName
 
 
def makeFileName():
  """
  """ 
 
 
 
# ---------------------------------------------------------------------- 
def niceFileName(fileName, extension):  
  """ Extract file name from a given tuple.
  """
  if not fileName:
    return ""

    # add suffix if it wasn't specified by user
  fileInfo = QtCore.QFileInfo(str(fileName))
  if len(fileInfo.suffix()) == 0:
    fileName = fileInfo.absoluteFilePath() + "." + extension
    
  return fileName


# ---------------------------------------------------------------------- 
def uniqueFileName(baseName, usedNames):
  """Generate unique name for Region, RegionGroup, etc.
  different from names present in "usedItems".
  """
  newName = baseName
  copyCnt = 1
    
  while True:
    clash = False
      
    for usedName in usedNames:
      if newName == usedName:
        clash = True
        break
      
        # newName not found on the list
    if not clash:
      break
     
      # try another name 
    newName = baseName + "_%02d" % copyCnt 
    copyCnt += 1 
    
  return newName




   
# ---------------------------------------------------------------------- 
def parseLogLevel(levelStr):
  """ Return logging level "object" corresponding to a given string 
    representation (case insensitive).
  """
  logLevel = levelStr.lower()
    
  if logLevel == "debug":
    return logging.DEBUG
  elif logLevel == "info":
    return logging.INFO
  elif logLevel == "warning":
    return logging.WARNING
  elif logLevel == "error":
    return logging.ERROR
  elif logLevel == "critical":
    return logging.CRITICAL
  


# ---------------------------------------------------------------------- 
def uniqueName(baseName, postfix, usedItems):
  """Generate unique name for Region, RegionGroup, etc.
  different from names present in "usedItems"."""

  baseName = baseName + postfix    # e.g. " - Copy"
  newName = baseName
    
  copyCnt = 1
    
  while True:
    clash = False
      
    for item in usedItems:
      if newName == item.name:
        clash = True
        break
      
        # newName not found on the list
    if not clash:
      break
     
      # try another name 
    newName = baseName + " (%d)" % copyCnt 
    copyCnt += 1 
    
  return newName





# ----------------------------------------------------------------------  
def assertUniqueInstance(lockFileName, parent):
  """Checks if any other instance of the program is already running on this PC.
  """
  if os.path.isfile(lockFileName):
    msg = f"Looks like another instance of {parent._app_name} is already running!\n"
    msg += "Do you want to continue?"

    response = QtWidgets.QMessageBox.question(parent, "Lockfile found", msg,
                                              QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

    if response != QtWidgets.QMessageBox.Yes:
      raise RuntimeError(f"Multiple instance exception ({parent._app_name})")
  
  else:
    with open(lockFileName, "w") as lockFile:
      lockFile.write("locked\n")
      
# ----------------------------------------------------------------------  
def unlockAppInstance(lockFileName):
  """Simply remove "lockfile".
  """
  if os.path.isfile(lockFileName):
    os.remove(lockFileName)
    print(f"Lockfile {lockFileName} removed successfully!")

# ---------------------------------------------------------------------- 
def timeToString(totalAcqTime, options="compact"):
  """Convert time (in seconds) to human readable format.
  """
  secInYear = 365 * 24 * 3600                 # roughly
  secInMonth = 31 * 24 * 3600       
  secInDay = 24 * 3600

  years = int(totalAcqTime / secInYear)
  months = int((totalAcqTime - years * secInYear) / secInMonth)                     # the rest 
  days = int((totalAcqTime - years * secInYear - months * secInMonth) / secInDay)   # --||--

  hours = int((totalAcqTime - years * secInYear - months * secInMonth - days * secInDay) / 3600)
  minutes = int((totalAcqTime - years * secInYear - months * secInMonth - days * secInDay - hours * 3600) / 60)
  seconds = int(totalAcqTime - years * secInYear - months * secInMonth - days * secInDay - hours * 3600 - minutes * 60)
  
  strRep = ""
  if options == "easy":  
    if years != 0:
      strRep = "%dY %dM %dD %dh %dm %ds" % (years, months, days, hours, minutes, seconds)
    elif months != 0:
      strRep = "%dM %dD %dh %dm %ds" % (months, days, hours, minutes, seconds)
    elif days != 0:
      strRep = "%dD %dh %dm %ds" % (days, hours, minutes, seconds)
    elif hours != 0:
      strRep = "%dh %dm %ds" % (hours, minutes, seconds)
    elif minutes != 0:
      strRep = "%dm %ds" % (minutes, seconds)
    elif seconds != 0:
      strRep = "%ds" % (seconds)
  
  else:
    if years != 0:
      strRep = "%dY %dM %dD %02d:%02d:%02d" % (years, months, days, hours, minutes, seconds)
    elif months != 0:
      strRep = "%dM %dD %02d:%02d:%02d" % (months, days, hours, minutes, seconds)
    elif days != 0:
      strRep = "%dD %02d:%02d:%02d" % (days, hours, minutes, seconds)
    else:  
      strRep = "%02d:%02d:%02d" % (hours, minutes, seconds)

  return strRep


# ----------------------------------------------------------------------  
def levelToNumber(levelName):
  """Convert given logging name to integer number.
  """
  levelNumber = 0
  levelName = levelName.lower()

  if levelName == "debug":
    levelNumber = 0 
  elif levelName == "info":
    levelNumber = 1 
  elif levelName == "warning":
    levelNumber = 2 
  elif levelName == "error":
    levelNumber = 3 
    
  return levelNumber

# ----------------------------------------------------------------------
def get_text_coordinates(plot_item, size, xinfo, position='tl'):

    [[x_min, x_max], [y_min, y_max]] = plot_item.viewRange()

    dx = abs(x_max - x_min) * 0.05
    dy = abs(y_max - y_min) * 0.05

    if xinfo == 'binding':
      if 'l' in position:
        position.replace('l', 'r')
      else:
        position.replace('l', 'r')

    if position == 'tl':
      textx = x_min + dx
      texty = y_max - dy
    elif position == 'tr':
      textx = x_max - dx - size.width() * plot_item.getViewBox().viewPixelSize()[0]
      texty = y_max - dy
    elif position == 'bl':
      textx = x_max + dx
      texty = y_min + dy + size.height() * plot_item.getViewBox().viewPixelSize()[1]
    elif position == 'br':
      textx = x_max - dx - size.width() * plot_item.getViewBox().viewPixelSize()[0]
      texty = y_min + dy + size.height() * plot_item.getViewBox().viewPixelSize()[1]

    return QtCore.QPointF(textx, texty)


# ----------------------------------------------------------------------
class Segment:
  """ Simple representation of line segment.
  """

  # ---------------------------------------------------------------------- 
  def __init__(self, x1, y1, x2, y2):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2

# ---------------------------------------------------------------------- 
def segmentsCoincident(x1, y1, x2, y2,         # first segment
                       x3, y3, x4, y4):        # second segment
  """
  """
  xMinA = min(x1, x2)
  xMaxA = max(x1, x2)
  yMinA = min(y1, y2)
  yMaxA = max(y1, y2)

  xMinB = min(x3, x4)
  xMaxB = max(x3, x4)
  yMinB = min(y3, y4)
  yMaxB = max(y3, y4)
  
  denominator = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
  if denominator == 0:      # lines are parallel
      # if any of 2 end points of the first segment is "within" the second segment
    if (xMinA >= xMinB and xMinA <= xMaxB and yMinA >= yMinB and yMinA <= yMaxB) or \
       (xMaxA >= xMinB and xMaxA <= xMaxB and yMaxA >= yMinB and yMaxA <= yMaxB):
      return True

    if (xMinB >= xMinA and xMinB <= xMaxA and yMinB >= yMinA and yMinB <= yMaxA) or \
       (xMaxB >= xMinA and xMaxB <= xMaxA and yMaxB >= yMinA and yMaxB <= yMaxA):
      return True

  return False  

# ---------------------------------------------------------------------- 
def segmentsIntersect(x1, y1, x2, y2,         # first segment
                      x3, y3, x4, y4):        # second segment
  """ Return logical True if given line segments intersect each other.

    The function is used e.g. to verify if motor's trajectory intersects
    with user defined border.
  """
  if segmentsCoincident(x1, y1, x2, y2, x3, y3, x4, y4):
    return True

    # check if segments are parallel but not coincident
  denominator = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
  if denominator == 0:
    return False

    # calculate intersection point of 2 lines defined by the segments
  px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denominator
  py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denominator

    # intersection point should be within segmentA and segmentB
  xMinA = min(x1, x2)
  xMaxA = max(x1, x2)
  yMinA = min(y1, y2)
  yMaxA = max(y1, y2)

  xMinB = min(x3, x4)
  xMaxB = max(x3, x4)
  yMinB = min(y3, y4)
  yMaxB = max(y3, y4)
  
  return (px >= xMinA and px <= xMaxA and py >= yMinA and py <= yMaxA and
          px >= xMinB and px <= xMaxB and py >= yMinB and py <= yMaxB)








