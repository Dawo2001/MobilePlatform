import cv2
import numpy as np




def calculate_line_equation(line):
    x1, y1, x2, y2 = line

    a = (y2 - y1) / (x2 - x1) if x1 != x2 else 0
    b = y1 - a * x1

    return a, b


def calculate_cross_angle(a1, a2):
    if(a1*a2!=-1):
        rad = np.arctan((a2 - a1) / (1 + a1 * a2))
    else:
        rad = np.pi / 2
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

def find_contours(gray_frame):
    thresh = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 6)

    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    return cnts[0] if len(cnts) == 2 else cnts[1]


def find_circles(contours):
    circles = []

    for c in contours:
        area = cv2.contourArea(c)
        _, _, w, h = cv2.boundingRect(c)
        ratio = w / h
        ((x, y), r) = cv2.minEnclosingCircle(c)

        if .3 < ratio < 1.0 and area > 40:
            circles.append((x, y, r))
    return circles


def locate_measuring_disc(gray_scale_frame, circle):
    x, y, r = map(int, circle)
    rect_x = max(0, x - r)
    rect_y = max(0, y - r)

    crop_gray = gray_scale_frame[rect_y:(rect_y + 2 * r), rect_x:(rect_x + 2 * r)]

    blur = cv2.GaussianBlur(crop_gray, (5, 5), 0)
    edges = cv2.Canny(blur, 255 / 3, 255)

    #lines = cv2.HoughLinesP(edges, 2.0, np.pi / 180, 10, minLineLength=5, maxLineGap=5)
    lines = cv2.HoughLinesP(edges, 2.0, np.pi / 180, 10, minLineLength=10, maxLineGap=10)
    return verify_lines_conditions(crop_gray, lines, (rect_x, rect_y), r)


def verify_lines_conditions(crop, lines, rect, r):
    boxes_coordinates = []

    if lines is not None and len(lines) > 0:
        crop_w, crop_h = crop.shape

        for i in range(len(lines) - 1):
            #min_width, min_height = crop_w * 0.8, crop_h * 0.8
            min_width, min_height = crop_w * 2.2, crop_h * 2.2
            if not is_line_long_enough(lines[i][0], min_width, min_height):
                continue

            for j in range(i + 1, len(lines)):
                if not is_line_long_enough(lines[j][0], min_width, min_height):
                    continue

                intersection = calculate_lines_intersection(lines[i][0], lines[j][0])
                if intersection is not None:
                    x_i, y_i, cross_angle = intersection
                    #width_tolerance, height_tolerance = 0.25 * crop_w / 2, 0.25 * crop_h / 2
                    width_tolerance, height_tolerance = 1 * crop_w / 2, 1 * crop_h / 2
                    middle_width, middle_height = abs(x_i - crop_w / 2) <= width_tolerance, \
                                                    abs(y_i - crop_h / 2) <= height_tolerance

                    if middle_width and middle_height and 86 < abs(cross_angle) < 94:
                        x1y1 = (rect[0], rect[1])
                        x2y2 = (rect[0] + 2 * r, rect[1] + 2 * r)

                        boxes_coordinates.append((x1y1, x2y2))
    return boxes_coordinates


def is_line_long_enough(line, min_width, min_height):
    x1, y1, x2, y2 = line
    x_diff = abs(x1 - x2)
    y_diff = abs(y1 - y2)

    return x_diff <= min_width and y_diff <= min_height


def draw_boxes(rgb_frame, boxes):
    for box in boxes:
        cv2.rectangle(rgb_frame, box[0], box[1], [0, 0, 255], 2)
        break


def distance_to_center(d):
    frame_width = 640
    frame_height = 480
    rX=d[0]
    rY=d[1]
    if rX>=640:
        return rX-(frame_width*3/2-50), rY-(frame_height/2)+130
    else:
        return rX-(frame_width/2+50), rY-(frame_height/2)+130


def detect_disc(rgb_frame):
    cv_image = cv2.cvtColor(np.array(rgb_frame), cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    contours = find_contours(gray_frame)
    circles = find_circles(contours)

    found_boxes = []
    for circle in circles:
        result = locate_measuring_disc(gray_frame, circle)
        found_boxes.extend(result)

    draw_boxes(cv_image, found_boxes)
    if (found_boxes != []):
        distance = distance_to_center(found_boxes[0][0])
    else:
        distance = (0, 0)
    cv_output_frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    return cv_output_frame, distance

