import cv2
import math
import sys

class ObjectTracker():
  def __init__(self):
    self.objects = {} # id, cx, cy
    self.counting = 0

  def update(self, boundingRects):
    bboxes = []

    for rect in boundingRects:
      closest = self.findClosest(rect)
      id = closest["object_id"]
      if id == 0:
        # id = len(self.objects.items()) + 1 
        self.counting = self.counting + 1     
        id = self.counting
        
      self.objects[id] = (closest["cx"], closest["cy"])
      bboxes.append((id, rect))

    self.removeNoneExistedObject(bboxes)
    return bboxes

  def findClosest(self, rect):
    x, y, w, h = rect
    cx = x + (w // 2)
    cy = y + (h // 2)

    closest = {
      "object_id": 0,
      "dist": 500,
      "cx": cx,
      "cy": cy
    }

    for id, center_points in self.objects.items():
      ecx, ecy = center_points
      dist = math.hypot(cx - ecx, cy - ecy)

      if dist < closest["dist"]:
        closest = {
          "object_id": id,
          "dist": dist,
          "cx": cx,
          "cy": cy
        }
    
    if closest["dist"] < 50:
      return closest

    return {
      "object_id": 0,
      "dist": 500,
      "cx": cx,
      "cy": cy
    }
  
  def removeNoneExistedObject(self, bboxes):
    keys = self.objects.keys()
    for key in keys:
      bbox = [item for item in bboxes if item[0] == key]
      # print(bbox)
      # if len(bbox) == 0:
        # del self.objects[key]
      




