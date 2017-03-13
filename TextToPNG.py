#!/bin/python

from PIL import Image

FILENAME = "SampleData1/SampleSqueezed.txt"

WIDTH = 5008
HEIGHT = 5121

# 255/6
# 6 different values -> split evenly between 255 rgb values 
MULT = 42.5
px_lookup = [int(x*MULT) for x in range(0, 7)]

im = Image.new('RGB', (WIDTH, HEIGHT), 'black')
x,y = 0, 0

counts = [0]*7

with open(FILENAME) as data:
    for line in data:
        for num in line.split(' '):
            try:
                n = int(num)
                counts[n] += 1
            except:
                continue
            im.putpixel((x, y), (px_lookup[n], px_lookup[n], px_lookup[n] ))
            x += 1
        x = 0
        y += 1

im.show()
im.save('putpixel.png')


print("Counts of each value: \n0: %d\n1: %d\n2: %d\n3: %d\n4: %d\n5: %d\n6: %d\n" % (counts[0], counts[1], counts[2], counts[3], counts[4], counts[5], counts[6]))
