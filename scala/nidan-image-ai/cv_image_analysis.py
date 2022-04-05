from PIL import Image
import io
import numpy as np
import cv2
import matplotlib.pyplot as plt

IMG_FILE = "input/img_1.JPEG"


def read_fromm_bytes(img_bytes):
  stream = io.BytesIO(bytearray(img_bytes))
  return Image.open(stream)

def read_PIL_image(_imagePath):
  PILImage = Image.open(_imagePath)
  PILImage.show()

def PIL_from_bytes(_imagePath):
  img_bytes_1 = open(_imagePath, "rb").read()
  img_bytes = io.BytesIO(bytearray(img_bytes_1))
  return Image.open(img_bytes)
  

def cv2Image_from_bytes(_imagePath):
  img_bytes = open(_imagePath, "rb").read()
  np_image = np.frombuffer(img_bytes.getvalue(), dtype=np.uint8)
  return cv2.imdecode(np_image, cv2.IMREAD_COLOR)

def display_images(imageList, legendList, cols, _outputFile = ""):
  rows = len(imageList) / cols

  for i in xrange(len(imageList)):
    plt.subplot(rows,cols,i+1),plt.imshow(imageList[i])
    plt.title(legendList[i])
    plt.xticks([]),plt.yticks([])

  if _outputFile != "":
    plt.savefig(_outputFile)
  else:
    plt.show()




## COUNTING STUFF
def test_filters(_imagePath, _minT, _maxT):
  im = cv2.imread(_imagePath, -1)
  imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

  minT = _minT
  maxT = _maxT

  ret, tBinary = cv2.threshold(imgray, minT, maxT, cv2.THRESH_BINARY)
  ret, tBinaryInv = cv2.threshold(imgray, minT, maxT, cv2.THRESH_BINARY_INV)
  ret, tTrunc = cv2.threshold(imgray, minT, maxT, cv2.THRESH_TRUNC)
  ret, tZero = cv2.threshold(imgray, minT, maxT, cv2.THRESH_TOZERO)
  ret, tZeroInv = cv2.threshold(imgray, minT, maxT, cv2.THRESH_TOZERO_INV)
  ret, tBOtsu = cv2.threshold(imgray, minT, maxT, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
  ret, tBInvOtsu = cv2.threshold(imgray, minT, maxT, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  ret, tBTri = cv2.threshold(imgray, minT, maxT, cv2.THRESH_BINARY+cv2.THRESH_TRIANGLE)
  ret, tBInvTri = cv2.threshold(imgray, minT, maxT, cv2.THRESH_BINARY_INV+cv2.THRESH_TRIANGLE)
  th = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)

  legends = ["original", "gray", "binary", "binaryInv", "trunc", "zero", "zeroInv", "binOtsu", "binInvOtsu", "binTri", "binInvTri", "adaptive"]
  imgs = [im, imgray, tBinary, tBinaryInv, tTrunc, tZero, tZeroInv, tBOtsu, tBInvOtsu, tBTri, tBInvTri, th]
  display_images(imgs, legends, 4)


def write_rois(_image, _rois, _prefix):
  index = 1
  for roi in _rois:
    img_path = "%s/roi_%d.jpg" % (_prefix, index)
    #print(roi)
    print(cv2.contourArea(roi))
    #x, y, w, h = roi
    #output = "x:%d y:%d w:%d h%d" % (x,y,w,h)
    #print("# %s %s" %(img_path, output))


def test_rois(_imagePath, _minT = 0, _maxT = 255):
  im = cv2.imread(_imagePath, -1)
  imBlurred = cv2.pyrMeanShiftFiltering(im, -10, 91)
  imgray = cv2.cvtColor(imBlurred,cv2.COLOR_BGR2GRAY)

  ret, tBinary = cv2.threshold(imgray, _minT, _maxT, cv2.THRESH_BINARY_INV+cv2.THRESH_TRIANGLE)
  roiBinary, hierarchy = cv2.findContours(tBinary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
  
  #cv2.drawContours(im, roiBinary, -1, (0,0,255),6)
  for roi in roiBinary:
    x,y,w,h = cv2.boundingRect(roi)
    cv2.rectangle(im, (x,y), (x+w,y+h), (0,255,0), 2)

  cv2.imshow("The image", im)
  cv2.waitKey()

#  
#  blured = cv2.adaptiveThreshold(tBinary, _maxT, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
#  roiBlured, hierarchy = cv2.findContours(blured,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_L1)
#
#  median7 = cv2.medianBlur(tBinary, 7)
#  roiMedian7, hierarchy = cv2.findContours(median7,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_L1)
#  
#  median13 = cv2.medianBlur(tBinary, 13)
#  roiMedian13, hierarchy = cv2.findContours(median13,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_L1)
#
#  print("ROIS binary: " + str(len(roiBinary)))
#  print("ROIS Blured: " + str(len(roiBlured)))
#  print("ROIS Median7: " + str(len(roiMedian7)))
#  print("ROIS Median13: " + str(len(roiMedian13)))

#  write_rois(im, roiBinary, "stuff")

test_rois(IMG_FILE)


#filtered = cv2.bitwise_and(im, im, mask=median13)
#
#roiMedian13, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#img = cv2.drawContours(imgray, contours, -1, (255,255,255), 3)
#print(contours)
#
#plt.figure(figsize=(10,10))
#plt.subplot(1,2,1),plt.title('Original Image'),plt.imshow(imgray)#,'red')
#plt.subplot(1,2,2),plt.title('OpenCV.findContours'),plt.imshow(img, 'gray')#,'red')
#plt.show()
#print('number of detected contours: ',len(contours))
#
#
#print("W: " + str(width) + " H: " + str(height))
#print(len(img.getbands()))
#print(img_bytes_2)
#img_bytes = bytes(img_bytes_1, encoding="utf8")
#print(img_bytes)
#
#
#test_filters(IMG_FILE, 200, 255)




