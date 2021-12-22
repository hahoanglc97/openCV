import random

import cv2

img = cv2.imread('image/ngao.jpg', 1)

# --------edit image-----------
# img.shape = ['total line','total column','channel']
#
# for i in range(100):
#     for j in range(img.shape[1]):
#         img[i][j] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

# --------copy image-----------
selectionArea = img[0:100, 200:500]
img[300:400, 500:800] = selectionArea

# print(img.shape)
cv2.imshow('show image', img)
cv2.waitKey()
