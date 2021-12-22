import cv2

# read image
img = cv2.imread('image/ngao.jpg', 1)

# resize image
# img = cv2.resize(img, [400, 200])
# fx = 50%, fy=50%
img = cv2.resize(img, [0, 0], fx=0.5, fy=0.5)

# rotate image
img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

# export image
cv2.imshow("show image", img)
# k = ASCII code
k = cv2.waitKey()
# ord("s") return ASCII code character s
if k == ord("s"):
    # create new image
    cv2.imwrite("image/new_ngao.jpg", img)


