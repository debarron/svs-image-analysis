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
|           |       TIFF        |      JPEG      |     PNG        |        BMP        |        GIF      |
|-----------|---------|---------|-------|--------|------|---------|---------|---------|-------|---------|
| Tile Size | MIN     | MAX     | MIN   | MAX    | MIN  | MAX     | MIN     | MAX     | MIN   | MAX     |
|-----------|---------|---------|-------|--------|------|---------|---------|---------|-------|---------|
| 32x32     | 4250    | 4250    | 643   | 893    | 106  | 2608    | 4150    | 4150    | 848   | 1903    |
| 64x64     | 16538   | 16538   | 691   | 1689   | 208  | 9965    | 16438   | 16438   | 900   | 5210    |
| 128x128   | 65690   | 65690   | 883   | 4670   | 392  | 39245   | 65590   | 65590   | 1001  | 18308   |
| 256x256   | 262298  | 262298  | 1651  | 17155  | 856  | 158523  | 262198  | 262198  | 1417  | 70732   |
| 512x512   | 1048730 | 1048730 | 4723  | 66259  | 2201 | 632688  | 1048630 | 1048630 | 3189  | 279602  |
| 1024x1024 | 4194458 | 4194458 | 17011 | 260639 | 6490 | 2495711 | 4194358 | 4194358 | 10190 | 1101039 |  
