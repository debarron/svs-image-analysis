# svs-image-analysis

This project started as way to show evidence on how much storage
does it take to write the same image in different image formats.

We tested the following formats, and their compression style:
* TIFF, Lossless compression
* JPEG, Lossy compression
* PNG, Lossless compression
* GIF, Lossless compression
* BMP, Lossless compression

The experiments are conducted with Python and the OpenSlide library.

# Experiments
We extract tiles with different sizes from an image in the TCGA project.
We loaded the SVS image using the OpenSlide repository. Later we extract
tiles from three different regions: start, middle and end.
We extract six different tiles from each region, starting from a 32x32 size
and doubling all the way up to tiles with 1024x1024 in size.
Every tile generated, is stored in all five image formats, thus generating
90 tiles (5 formats x 6 dimensios x 3 regions).

# Results
  
