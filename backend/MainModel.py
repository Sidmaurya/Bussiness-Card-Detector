import numpy as np
import os
#import matplotlib.pyplot as plt
import imageio
import corner_detection
import perspective_transform
import text_detection
import cv2
from PIL import Image
import uuid
import pytesseract


def model_process(file_path):
  # Selecting files for testing
  file_img1 = file_path
  img1 = imageio.imread(file_img1)
  #plt.figure(figsize=(30, 30))
  #plt.subplot(131)
  #plt.imshow(img1)
  #plt.show()
  print('image selected for testing')

  #corner detection
  img1_corners = corner_detection.CornerDetector(img1).corner_detector()[0]
  #plt.figure(figsize=(20, 20))
  #plt.imshow(img1_corners)
  #plt.show()
  print('corner detected')

  corner_points1 = corner_detection.CornerDetector(img1).find_corners4().astype(
      np.float32)
  corner_points1[:, [0, 1]] = corner_points1[:, [1, 0]]
  img1_t = perspective_transform.PerspectiveTransform(
      img1, corner_points1).four_point_transform()
  #plt.figure(figsize=(20, 20))
  #plt.imshow(img1_t)
  #plt.show()
  print('image cropped')

  img1_name=file_path.split('/')[-1]
  im = Image.fromarray(img1_t)
  im.save('out_image/'+img1_name)
  pytesseract.pytesseract.tesseract_cmd = (
      r'/usr/bin/tesseract'
  )

  print('cropped image saved')
  img1_t_cv = cv2.cvtColor(img1_t, cv2.COLOR_RGB2BGR)
  sizes = [(17, 3), (30, 10), (5, 5), (9, 3)]
  for size in sizes:
    strs, bound_rects, img_bboxes = text_detection.TextDetector(img1_t_cv,
                                                        size).recognize_text()
    #print(*strs, sep='\n')
    strs=strs.replace('\n', ' ')
    print('text extracted and save to file')
    f = open('out_text/'+img1_name.split('.')[-2]+".txt", "a")
    f.writelines([st+"\n-------------------------------------------------\n" for st in strs])
    f.close()

    return {"img_link":img1_name+".jpeg","data":img1_name+".txt"}

