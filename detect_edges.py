#!/bin/python

import sys
from PIL import Image

FILENAME = "SampleData1/SampleSqueezed.txt"
HEIGHT = 5121
WIDTH = 5008

fl_left  = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
fl_right = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
fl_down  = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
fl_up    = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))

filter_matrix_left  = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
filter_matrix_right = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
filter_matrix_down  = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
filter_matrix_up    = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

im = []
for i in range(HEIGHT):
    im.append([0] * WIDTH)

x,y = 0,0
with open(FILENAME) as data:
    for line in data:
        for num in line.split(' '):
            try:
                n = int(num)
                im[y][x] = n
                x += 1
            except:
                continue
        y += 1
        x = 0

for y in range(1, HEIGHT-1):
    if y % 10 == 0:
        print("y: %d" % y, file=sys.stderr)
    for x in range(1, WIDTH-1):
        left_total  = 0
        right_total = 0
        down_total  = 0 
        up_total    = 0
        for a in range(-1,2):
            for b in range(-1, 2):
                left_total  += int(im[y+a][x+b] * 42.5) * filter_matrix_left[a+1][b+1]
                right_total += int(im[y+a][x+b] * 42.5) * filter_matrix_right[a+1][b+1]
                down_total  += int(im[y+a][x+b] * 42.5) * filter_matrix_down[a+1][b+1]
                up_total    += int(im[y+a][x+b] * 42.5) * filter_matrix_up[a+1][b+1]
        
        if left_total > 0:
            fl_left.putpixel((x, y), (0, 0, 0, 255))
        if right_total > 0:
            fl_right.putpixel((x, y), (0, 0, 0, 255))
        if down_total > 0:
            fl_down.putpixel((x, y), (0, 0, 0, 255))
        if up_total > 0:
            fl_up.putpixel((x, y), (0, 0, 0, 255))

fl_left.save('left.png')
fl_right.save('right.png')
fl_down.save('down.png')
fl_up.save('up.png')

