from cv2 import cv2
import numpy as np
from PIL import Image

in_path = r'D:\pythonVscode\people.jpg'
out_path = r'D:\pythonVscode\photo_new.jpg'

img = cv2.imread(in_path)
rect = (0, 0, img.shape[0], img.shape[1])
 
mask = np.zeros(img.shape[:2], np.uint8)
bgModel = np.zeros((1,65), np.float64)
fgModel = np.zeros((1,65), np.float64)
cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype(np.uint8)
 
out = img * mask2[:, :, np.newaxis]
#out += 255 * (1 - cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR))
 
cv2.imshow('output', out)
cv2.waitKey()

cv2.imwrite(out_path, out)
 