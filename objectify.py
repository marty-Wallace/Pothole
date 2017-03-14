#!/bin/python

from PIL import Image

FILENAME = "SampleData1/SampleSqueezed.txt"
HEIGHT = 5121
WIDTH = 5008

classified = Image.new('RGBA', (WIDTH, HEIGHT), 'BLACK')

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

least = 6
n = 7

#set an iv so we can fill the road, line and outer parts of the picture
outer_IV = [(0, 0), (0, 4900), (4900, 0), (HEIGHT-1, WIDTH-1)]
road_IV = [(186, 1986), (174, 2134)]
line_IV = [(992, 2207), (1044, 2202)]

#generate some discernable colors for holes
object_colour_cycle = [
        (255, 0, 255), 
        (0, 255, 255), 
        (255, 0, 0), 
        (0, 255, 0), 
        (0, 0, 255),
        (255, 0, 125),
        (255, 125, 0),
        (125, 0, 255),
        (125, 255, 0),
        (255, 255, 125),
        (255, 125, 255),
        (125, 255, 255),
        (255, 125, 75),
        (255, 75, 125),
        (125, 255, 75),
        (125, 75, 255),
        (75, 125, 255),
        (75, 255, 125),
        ]

# Do a floodfill on the picture, set the RGB value
def floodfill(im, y, x, new, rgb=None):
    val = im[y][x]
    q = []
    q.append((y, x))
    if rgb is None:
        rgb = object_colour_cycle[new % len(object_colour_cycle)]
    while not len(q) == 0:
        y, x = q.pop()
        if y < 0 or y >= HEIGHT or x < 0 or x >= WIDTH or im[y][x] != val:
            continue
        im[y][x] = new
        classified.putpixel((x, y), rgb)
        q.append((y+1, x))
        q.append((y-1, x))
        q.append((y, x+1))
        q.append((y, x-1))

#Outside of road IV
for y, x in outer_IV:
    floodfill(im, y, x, n, rgb=(255, 255, 255))
n += 1

#Flood fill road IV
for y, x in road_IV:
    floodfill(im, y, x, n, rgb=(0, 0, 0))
n += 1

#Flood fill line IV
for y, x in line_IV:
    floodfill(im, y, x, n, rgb=(255, 255, 0))
n += 1

#if it hasn't been filled yet, do a floodfill operation
for y in range(0, HEIGHT):
    for x in range(0, WIDTH):
        if im[y][x] <= least:
            floodfill(im, y, x, n)
            n += 1

#save image
classified.save('classified.png')
print("Done...")

