from PIL import Image
import os
import glob
import numpy as np


def crop(im, height, width):
    # im = Image.open(infile)
    imgwidth, imgheight = im.size
    rows = np.int(imgheight/height)
    cols = np.int(imgwidth/width)
    for i in range(rows):
        for j in range(cols):
            # print (i,j)
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)


if __name__ == '__main__':
    # change the path and the base name of the image files
    imgdir = '.'
    basename = 'Cam-*.tif'
    filelist = glob.glob(os.path.join(imgdir, basename))
    for filenum, infile in enumerate(filelist):
        # infile='/Users/alex/Documents/PTV/test_splitter/cal/Camera 1-1-9.tif'
        print(f'file no = {filenum}')  # keep the numbers for the future
        print(f'name is {infile}')
        im = Image.open(infile)
        imgwidth, imgheight = im.size
        print(('Image size is: %d x %d ' % (imgwidth, imgheight)))
        height = np.int(imgheight/2)
        width = np.int(imgwidth/2)
        start_num = 0
        for k, piece in enumerate(crop(im, height, width), start_num):
            # print k
            # print piece
            img = Image.new('L', (width, height), 255)
            # print img
            img.paste(piece)
            path = os.path.join("cam%d_1%05d.tif" % (int(k+1),filenum))
            img.save(path)
            os.rename(path, os.path.join("cam%d.1%05d" % (int(k+1), filenum)))
