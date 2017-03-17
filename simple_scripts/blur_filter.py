#!/bin/python

import sys
from PIL import Image


def drawProgressBar(percent_done, barLength = 40):
    """Display an updating progress bar in a terminal

    :percent_done: the percent done to display
    :barLength: how many chars long the bar is
    :returns: None

    """
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLength):
        if i <= int(barLength * percent_done):
            if i+1 <= int(barLength * percent_done):
                progress += "="
            else:
                progress += ">"
        else:
            progress += " "
    sys.stdout.write("[%s] %.2f%%" % (progress, percent_done * 100))
    sys.stdout.flush()




FILENAME = "SampleData1/SampleSqueezed.txt"
HEIGHT = 5121
WIDTH = 5008

fl_left  = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
fl_right = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
fl_down  = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
fl_up    = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))


mask_type = ''
if len(sys.argv) > 1:
    mask_type = sys.argv[1]
else:
    mask_type = 'Prewitt'


# sobel masks
filter_matrix_left  = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
filter_matrix_right = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
filter_matrix_down  = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
filter_matrix_up    = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

# prewitt masks
if mask_type == 'Prewitt':
    filter_matrix_left  = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]
    filter_matrix_right = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    filter_matrix_down  = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
    filter_matrix_up    = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]

# kirsch masks
elif mask_type == 'Kirsch':
    filter_matrix_left  = [[5, -3, -3], [5, 0, -3], [5, -3, -3]]
    filter_matrix_right = [[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]
    filter_matrix_down  = [[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]
    filter_matrix_up    = [[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]


blur_size = 3

blur_matrix = []
# default shitty blur
for i in range(blur_size):
    blur_matrix.append([1] * blur_size)
blur_matrix[blur_size//2][blur_size//2] = 0


im = []
im2 = []
im3 = []
for i in range(HEIGHT):
    im.append([0] * WIDTH)
    im2.append([0] * WIDTH)
    im3.append([0] * WIDTH)

x,y = 0,0
print("Loading image...")
with open(FILENAME) as data:
    for line in data:
        drawProgressBar(y/(HEIGHT-1))
        for num in line.split(' '):
            try:
                n = int(num)
                im[y][x] = n
                x += 1
            except:
                continue
        y += 1
        x = 0


print()
print("Filtering image with %s filter" % mask_type)
max1 = 0
max2 = 0
for y in range(1, HEIGHT-1):
    drawProgressBar(y/(HEIGHT-2))
    for x in range(1, WIDTH-1):
        left_total  = 0
        right_total = 0
        down_total  = 0 
        up_total    = 0
        for a in range(-1,2):
            for b in range(-1, 2):
                left_total  += int(im[y+a][x+b]) * filter_matrix_left[a+1][b+1]
                right_total += int(im[y+a][x+b]) * filter_matrix_right[a+1][b+1]
                down_total  += int(im[y+a][x+b]) * filter_matrix_down[a+1][b+1]
                up_total    += int(im[y+a][x+b]) * filter_matrix_up[a+1][b+1]

        im2[y][x] = ((left_total + right_total + down_total + up_total)*42.5) // 4
        im3[y][x] = (left_total + right_total + down_total + up_total) // 4
        max1 = max([im2[y][x], max1])
        max2 = max([im3[y][x], max2])



print()
print("Applying blur filter to alpha channel...")
for y in range(1, HEIGHT-1):
    for x in range(1, WIDTH-1):
        drawProgressBar(y/(WIDTH-2))
        total1 = 0
        total2 = 0
        for a in range(-1, 2):
            for b in range(-1, 2):
                total1 += im2[y+a][x+b]
                total2 += im3[y+a][x+b]
        alpha1 = (total1 / max1) // 9 
        alpha2 = (total2 / max2) // 9 

        one.putpixel((x, y), (0, 0, 0, alpha1))
        two.putpixel((x, y), (0, 0, 0, alpha2))
        if alpha1 > 125:
            three.putpixel((x, y), (1, 0, 0, 255))
        if alpha2 > 155:
            four.putpixel((x, y), (0, 0, 0, 255))


print()
print("Saving images...")

one.save('one.png')
two.save('two.png')
three.save('three.png')
four.save('four.png')

print("Finished saving images....")

