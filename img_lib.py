import cv2
import numpy as np

# text color 
color_green = (  0, 255,   0)
color_red   = (  0,   0, 255)
color_blue  = (255,   0,   0)


def image_text(img, note , org = (10,30), color= color_green, font_Sclae=1):
  return cv2.putText(img, note, org=org, fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                        fontScale=font_Sclae, color=color, thickness=2)

def image_resize(img, new_size):
  return cv2.resize(img, new_size, interpolation = cv2.INTER_AREA)
  
def image_scale(img, scale= 0.5):
    width = int(img.shape[1] * scale )
    height = int(img.shape[0] * scale)
    dim = (width, height)
  
    # resize image
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def image_crop(img, roi_x, roi_y, roi_w, roi_h):
  return img[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]

#Draw a Rectangle
def image_rectangle_1(img, x,y, w,h, color = color_green, thickness=1):
    return cv2.rectangle(img, (x,y), (x+w, y+h), color=color, thickness=thickness)

#Draw a Rectangle
def image_rectangle(img, start_pt = (0,0), end_point = (10,10), color = color_green, thickness=1):
    return cv2.rectangle(img, start_pt, end_point, color=color, thickness=thickness)

# Draw A circle
def image_circle(img, center_coordinates, radius, color = color_green, thickness = 1):
    return cv2.circle(img, center_coordinates, radius, color, thickness)

# Draw a line
def image_line(img, start_pt = (0,0), end_point = (10,10), color = color_green, thickness=1):
    return cv2.line(img, start_pt, end_point, color=color, thickness=thickness)

# Draw a line
def image_polylines (img, pts, isClosed = True, color = color_green, thickness=1):
    cv2.polylines(img, [pts], isClosed=isClosed, color=color, thickness=thickness)

# gray image
def image_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Simple Thresholding
def image_threshold(img, lower=150, upper=255):
    return cv2.threshold(img, lower, upper, cv2.THRESH_BINARY )

def image_filter_color(img, threshold_low, threshold_high):
    GB_img=cv2.GaussianBlur(img,(5,5),0)
    hsv_frame = cv2.cvtColor(GB_img, cv2.COLOR_BGR2HSV)

    img_mask = cv2.inRange(hsv_frame, threshold_low, threshold_high)
    img_filter = cv2.bitwise_and(img, img, mask=img_mask)
    return img_filter, img_mask

''' stack array of images into a bigger image'''
def image_stack(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver