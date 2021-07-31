import cv2
from object_tracker import * 

cap = cv2.VideoCapture('./videos/244_traffic.mp4')

object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40, detectShadows=True)
object_tracker = ObjectTracker()

while True:
  ret, frame = cap.read()

  scale_percent = 120 # percent of original size
  width = int(frame.shape[1] * scale_percent / 100)
  height = int(frame.shape[0] * scale_percent / 100)
  dim = (width, height)

  resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

  roi = resized[100: 288,0: 250]

  mask = object_detector.apply(roi)
  _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
  contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  detections = []
  for contour in contours:
    area = cv2.contourArea(contour)

    if area > 500:
      #cv2.drawContours(roi, [contour], -1, (0, 255, 0), 2)
      x, y, w, h = cv2.boundingRect(contour)
      detections.append([x, y, w, h])

  bboxes = object_tracker.update(detections)
  for id, rect in bboxes:
    x, y, w, h = rect
    cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

  cv2.imshow("Original Video", resized)
  cv2.imshow("Mask", mask)
  cv2.imshow("ROI", roi)

  if cv2.waitKey(50) == 27:
    break

cap.release()
cv2.destroyAllWindows()
