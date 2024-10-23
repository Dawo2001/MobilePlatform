
import cv2
import numpy as np

import time

def detect_disc():
    try:
        try:
            image = cv2.imread("my.bmp")
            cv2.imshow('image', image)
        except Exception as e:
            print("nema obrazu")
            pass
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 6)

        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]


        circles = []
        for c in cnts:
            area = cv2.contourArea(c)
            _, _, w, h = cv2.boundingRect(c)
            ratio = w / h
            ((x, y), r) = cv2.minEnclosingCircle(c)
            if .15 < ratio < 3.50 and area > 20:
                circles.append((x, y, r))


        for circle in circles:
            x, y, r = map(int, circle)

            rectX = max(0, x - r)
            rectY = max(0, y - r)
        crop = gray[rectY:(rectY + 2 * r), rectX:(rectX + 2 * r)]
       
        #wszystkie kółka
        #cv2.rectangle(image, (rectX, rectY),(rectX + 2 * r, rectY + 2 * r),[0, 255, 255], 2)
        blur = cv2.GaussianBlur(crop, (5, 5), 0)

        edges = cv2.Canny(blur, 255/3, 255)

        dilation = cv2.dilate(edges,np.ones((2, 2), dtype=np.uint8),iterations=1)

        lines = cv2.HoughLinesP(edges, 2.0, np.pi / 180, 10, minLineLength=10, maxLineGap=10)


        def calculate_line_equation(line):
            x1, y1, x2, y2 = line
            a = (y2 - y1) / (x2 - x1) if x1 != x2 else 0
            b = y1 - a * x1
            return a, b

        def calculate_cross_angle(a1, a2):
            rad = np.arctan((a2 - a1) / (1 + a1 * a2))
            return rad * 180 / np.pi

        def calculate_lines_intersection(line1, line2):
            a1, b1 = calculate_line_equation(line1)
            a2, b2 = calculate_line_equation(line2)
            cross_angle = calculate_cross_angle(a1, a2)
            intersection_x = (b2 - b1) / (a1 - a2) \
                if a1 != a2 else None
            if intersection_x is None:
                return None
            intersection_y = a1 * intersection_x + b1
            return intersection_x, intersection_y, cross_angle

        if (lines is not None):
            for i in range(len(lines) - 1):
                for j in range(i + 1, len(lines)):
                    intersection = calculate_lines_intersection(lines[i][0], lines[j][0])
                    middle_width = False
                    middle_height = False
                    if intersection is not None:
                        x_i, y_i, cross_angle = intersection
                        #cv2.rectangle(image, (rectX+int(x_i), rectY+int(y_i)), (rectX+int(x_i)+10, rectY+int(y_i)+10), [255, 255, 0], 2)
                        crop_w, crop_h = crop.shape
                        width_tolerance, height_tolerance = 1 * crop_w / 2, 1 * crop_h / 2
                        middle_width, middle_height = abs(x_i - crop_w / 2) <= width_tolerance, abs(y_i - crop_h / 2) <= height_tolerance

                    if middle_width and middle_height and 83 < abs(cross_angle) < 97:
                        cv2.rectangle(image, (319, 239), (321, 241), [0, 255, 255], 2)
                        cv2.rectangle(image, (959, 239), (961, 241), [0, 255, 255], 2)
                        cv2.rectangle(image, (369, 239), (371, 241), [255, 0, 255], 2)
                        cv2.rectangle(image, (909, 239), (911, 241), [255, 0, 255], 2)
                        cv2.rectangle(image, (rectX, rectY),(rectX + 2 * r, rectY + 2 * r),[0, 0, 255], 2)
                        cv2.imshow('image', image)
                        cv2.waitKey(0)
                        time.sleep(0.1)
                        distance_to_center(rectX+r, rectY+r)
                        return rectX+r, rectY+r
    except Exception as e:
        pass

def distance_to_center(rectX, rectY):
    frame_width = 640
    frame_height = 480
    if rectX>=640:
        return rectX-(frame_width*3/2-50), rectY-(frame_height/2)+130
    else:
        return rectX-(frame_width/2+50), rectY-(frame_height/2)+130



if __name__ == "__main__":
    try:
        print("xd")
        rx, ry = detect_disc()
        print(rx, ry)
        dist = distance_to_center(rx, ry)
        print(dist)
        cv2.imshow('image', image)
        cv2.waitKey(0)
        time.sleep(0.1)
    except Exception as e:    
        pass
