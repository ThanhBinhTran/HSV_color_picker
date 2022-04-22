import cv2
import numpy as np
from HSV_class import HSV_values
from img_lib import image_filter_color, image_scale, image_stack, image_text  
import argparse

#############################################
# global variables
#############################################
image_hsv = None   
image_src = None   
pixel = (20,60,80) # some stupid default
HSV_offset = np.array([10, 10, 40])     # H_offset, S_offset, V_offset

hsv_values = HSV_values()
colorbar_win = 'Color Tracking bars'
result_win = 'original, masked and its partition images'
HSV_win = 'HSV image [click to get filter image]'

#assign strings for ease of coding
hh='Hue High'
hl='Hue Low'
sh='Saturation High'
sl='Saturation Low'
vh='Value High'
vl='Value Low'

#'optional' argument is required for trackbar creation parameters
def nothing(x):
    pass

def create_slide_bar():

    cv2.namedWindow(colorbar_win, cv2.WINDOW_AUTOSIZE) #/Create a window named 'Colorbars'

    #Begin Creating trackbars for each
    cv2.createTrackbar(hl, colorbar_win,0,179,nothing)
    cv2.createTrackbar(hh, colorbar_win,0,179,nothing)
    cv2.createTrackbar(sl, colorbar_win,0,255,nothing)
    cv2.createTrackbar(sh, colorbar_win,0,255,nothing)
    cv2.createTrackbar(vl, colorbar_win,0,255,nothing)
    cv2.createTrackbar(vh, colorbar_win,0,255,nothing)

def set_position_trackbar(hsv_values):
    cv2.setTrackbarPos(hl, colorbar_win, hsv_values.hl)
    cv2.setTrackbarPos(hh, colorbar_win, hsv_values.hh)
    cv2.setTrackbarPos(sl, colorbar_win, hsv_values.sl)
    cv2.setTrackbarPos(sh, colorbar_win, hsv_values.sh)
    cv2.setTrackbarPos(vl, colorbar_win, hsv_values.vl)
    cv2.setTrackbarPos(vh, colorbar_win, hsv_values.vh)

def apply_filter(img, hsv_pixel, hsv_upper, hsv_lower):
    print("pixed:{0}, lower:{1}, upper:{2}".format(hsv_pixel, hsv_lower, hsv_upper))
    img_filter, img_mask = image_filter_color(img, hsv_lower, hsv_upper)
    img_filter = image_text(img=img_filter, note="pixed:{0}".format(hsv_pixel), org=(10,30), font_Sclae=0.5)
    img_filter = image_text(img=img_filter, note="lower:{0}".format(hsv_lower), org=(10,50), font_Sclae=0.5)
    img_filter = image_text(img=img_filter, note="upper:{0}".format(hsv_upper), org=(10,70), font_Sclae=0.5)
    stacked_image = image_stack(scale=1, imgArray=([img, img_filter, img_mask]))
    cv2.imshow(colorbar_win,stacked_image)
    
# mouse callback function
def pick_color(event,x,y,flags,param):
    global pixel
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y,x]
        hsv_values.set_values_by_offset(pixel, HSV_offset)
        set_position_trackbar(hsv_values=hsv_values)

def main(img_file):
    import sys
    global image_hsv, image_src, pixel # so we can use it in mouse callback

    # read image
    image_src = cv2.imread(img_file)  # 
    image_src = image_scale(img=image_src, scale=0.5)
    if image_src is None:
        print ("the image read is None............")
        return

    ## create track bar for adjustment
    create_slide_bar()
    
    # HSV window
    cv2.namedWindow(HSV_win)
    cv2.setMouseCallback(HSV_win, pick_color)   # call back function for mouse clicking

    # now click into the hsv img , and look at values:
    image_hsv = cv2.cvtColor(image_src,cv2.COLOR_BGR2HSV)
    cv2.imshow(HSV_win,image_hsv)

    # keep updating
    while True:
        hsv_values.hl = cv2.getTrackbarPos(hl, colorbar_win)
        hsv_values.hh = cv2.getTrackbarPos(hh, colorbar_win)
        hsv_values.sl = cv2.getTrackbarPos(sl, colorbar_win)
        hsv_values.sh = cv2.getTrackbarPos(sh, colorbar_win)
        hsv_values.vl = cv2.getTrackbarPos(vl, colorbar_win)
        hsv_values.vh = cv2.getTrackbarPos(vh, colorbar_win)
        upper = hsv_values.get_upper()
        lower = hsv_values.get_lower()
        apply_filter(img=image_src, hsv_pixel= pixel, hsv_upper=upper, hsv_lower=lower)
        
        # press esc to exit
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description='HSV color picker.')
    parser.add_argument('-i', metavar="input image",  help='input video', default="img.jpg")
    menu_result = parser.parse_args()
    img_file = menu_result.i

    HSV_offset = np.array([20, 20, 40])
    main(img_file=img_file)