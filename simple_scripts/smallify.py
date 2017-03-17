#!/bin/python

from PIL import Image

FILENAME = "SampleData1/SampleSqueezed.txt"

WIDTH = 5008
HEIGHT = 5121

NEW_WIDTH = WIDTH // 10
NEW_HEIGHT = HEIGHT // 10

im = []
for i in range(NEW_HEIGHT):
    im.append([0] * NEW_WIDTH)

x,y = 0, 0

counts = [0]*7

with open(FILENAME) as data:
    for line in data:
        if y > NEW_HEIGHT:
            continue
        for num in line.split(' '):
            if x > NEW_WIDTH:
                continue
            try:
                n = int(num)
                counts[n] += 1
                im[y][x]= n
            except:
                pass
            x += 1
        x = 0
        y += 1

for line in im:
    print(' '.join([str(s) for s in line]))

