import openslide
from math import floor

def writeImage(image, outputDir, keyword):
    imageJ = image.convert("RGB")
    imageJ.save('{}/test_{}.{}'.format(outputDir, keyword, 'JPEG'))
    image.save('{}/test_{}.{}'.format(outputDir, keyword, 'PNG'))
    image.save('{}/test_{}.{}'.format(outputDir, keyword, 'BMP'))
    image.save('{}/test_{}.{}'.format(outputDir, keyword, 'TIFF'))
    image.save('{}/test_{}.{}'.format(outputDir, keyword, 'GIF'))

def cropAndWriteImage(osImage, dim, key, outputDir):
    scaleW = floor(osImage.dimensions[0]/3) - dim
    scaleH = floor(osImage.dimensions[1]/3) - dim
    for label, location in [('start',(0,0)),('mid',(scaleW, scaleH)),('end',(2*scaleW,2*scaleH))]:
        keyword = '{}_{}_{}'.format(key, label, dim)
        size = (dim, dim)
        writeImage(osImage.read_region(location, 0, size), outputDir, keyword)

def runTestFormat(osImage, outputDir):
    dims = [(1,32), (2,64), (3,128), (4,256), (5,512), (6,1024)]
    for key, dim in dims:
        cropAndWriteImage(osImage, dim, key, outputDir)

prefix = '/home/daniel/Code/GithubRepos/svs-image-analysis/results'
imgFile = '/home/daniel/Datasets/nidan-svs/fff3981f-c428-450f-803d-a4f1bf7fca20/TCGA-X6-A8C4-01Z-00-DX5.6D982397-7796-4752-A470-C9E4042446B5.svs'

osImage = openslide.OpenSlide(imgFile)
runTestFormat(osImage, prefix)
