import cv2 as cv
import numpy as np

font = cv.FONT_HERSHEY_SIMPLEX

imm = "IMG-3437.mov"
vid = cv.VideoCapture(imm)

cir_count = 0
tot_frame = 0

frame_width = int(vid.get(3))
frame_height = int(vid.get(4))
fps = 15

size = (frame_width, frame_height)

output = cv.VideoWriter('output.mov', cv.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size)

if vid.isOpened() is False:
    print("Error opening file")


while vid.isOpened():
    ret, frame = vid.read()

    if ret:
        new_frame = frame.copy()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        blur = cv.medianBlur(gray, 5)
        circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 1.5, 500)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            x, y, r = circles[0][0], circles[0][1], circles[0][2]
            cv.circle(new_frame, (x, y), r, (0, 255, 0), 10)
            cv.circle(new_frame, (x, y), 5, (0, 255, 0), -1)
            cir_count += 1
        tot_frame += 1
        cv.putText(frame, 'Frames: ' + str(tot_frame), (50, 50), font, 1, (0, 255, 255), 2, cv.LINE_4)
        cv.putText(new_frame, 'Circle Frames: ' + str(cir_count), (50, 50), font, 1, (0, 255, 255), 2, cv.LINE_4)
        output.write(new_frame)
        cv.imshow('Center', np.hstack([frame, new_frame]))

    #close the video by pressing 0
    if cv.waitKey(50) & 0xFF == ord('0'):
        print("Circle Frames: " + str(cir_count))
        print("Total Frames: " + str(tot_frame))
        print("Total percentage of frames with circles: " + str(round(100 * cir_count/tot_frame, 2)) + "%")
        break

vid.release()
output.release()

cv.destroyAllWindows()
