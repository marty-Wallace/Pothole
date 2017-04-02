#!/bin/python

from PIL import Image
import sys

if '-h' in sys.argv or '--help' in sys.argv:
    print("python box_cutter.py filename startX startY height width > output.txt") 
    exit(1)

FILENAME = sys.argv[1]

startX = int(sys.argv[2])
startY = int(sys.argv[3])
width  = int(sys.argv[4])
height = int(sys.argv[5])

x,y = 0, 0

with open(FILENAME) as data:
    count = sum([1 for _ in data])
    data.seek(0)
    for line in data:
        im_line = []
        if y >= startY and y-startY < height:
            for num in line.split(' '):
                if x >= startX and x-startX < width:
                    im_line.append(num)
                x += 1
            print(' '.join(im_line))
        y += 1
        x = 0

