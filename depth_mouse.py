import cv2
from statistics import mode, stdev

# Image paths
img_name = 'sample_RGB.png'
img_dname = 'corres_depth.png'

# Read images
img = cv2.imread(img_name)
img_depth = cv2.imread(img_dname, cv2.CV_8UC1)

# Variables
ix, iy = -1, -1
drawing = False
values = [0, 0, 0, 0]

def draw_rectangle_with_drag(event, x, y, flags, param):
    global ix, iy, drawing, img, img_depth

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img = cv2.imread(img_name)
            cv2.rectangle(img, pt1=(ix, iy), pt2=(x, y), color=(0, 255, 255), thickness=1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        img = cv2.imread(img_name)
        cv2.rectangle(img, pt1=(ix, iy), pt2=(x, y), color=(0, 255, 255), thickness=1)
        img_depth = cv2.imread(img_dname, cv2.CV_8UC1)
        values[0], values[1], values[2], values[3] = ix, iy, x, y
        intensity(pixels(ix, iy, x, y, img_depth))

cv2.namedWindow(winname="RGB")
cv2.setMouseCallback("RGB", draw_rectangle_with_drag)

def pixels(ix, iy, x, y, img):
    points = []
    cv2.rectangle(img, pt1=(ix, iy), pt2=(x, y), color=(255, 255, 255), thickness=1)

    for x_count in range(ix + 1, x - 1, 1):
        for y_count in range(iy + 1, y - 1, 1):
            points.append(float(img[y_count, x_count]))

    return points

def intensity(value):
    pixels = filter_list(value)
    length_pixels = len(pixels)
    total_pixels = sum(pixels)
    average_intensity = round(total_pixels / length_pixels)
    max_intensity = max(pixels)
    min_intensity = min(pixels)
    mode_intensity = mode(pixels)
    std_intensity = stdev(list(pixels))

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottom_left_corner_of_text = (64, 457)
    font_scale = 0.6
    font_color = (255, 255, 255)
    thickness = 1
    line_type = 2

    message = f'av_intensity: {average_intensity} stdev: {std_intensity}'
    cv2.putText(img, message, bottom_left_corner_of_text, font, font_scale, font_color, thickness, line_type)

def filter_list(array):
    filtered_list = list(filter(lambda num: num != 0, array))
    #print(values) 

    return filtered_list





while True:
    cv2.imshow("RGB", img)
    cv2.imshow("Depth", img_depth)
    
    if cv2.waitKey(10) == 27:
        break

cv2.destroyAllWindows()
