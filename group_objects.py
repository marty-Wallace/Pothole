#!/bin/python

from PIL import Image
import math

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


class Region(object):


    def __init__(self, value, number, max_x=0, min_x=9999999, max_y=0, min_y=9999999, num_px = 0):
        self.value  = value
        self.number = number
        self.max_x  = max_x
        self.min_x  = min_x
        self.max_y  = max_y
        self.min_y  = min_y
        self.num_px = num_px
        self.px     = []
    

    def height(self):
        if self.num_px == 0:
            return 0
        return abs(self.max_y - self.min_y)+1


    def width(self):
        if self.num_px == 0:
            return 0
        return abs(self.max_x - self.min_x)+1


    def area(self):
        return self.height() * self.width()
    

    def can_grow(self):
        return self.num_px > 4


    def add_px(self, x, y):
        if x < self.min_x:
            self.min_x = x
        if x > self.max_x:
            self.max_x = x
        if y < self.min_y:
            self.min_y = y
        if y > self.max_y:
            self.max_y = y
        self.num_px += 1
        self.px.append((y, x))


    def _merge(self, region):
        if region.min_x < self.min_x:
            self.min_x = region.min_x
        if region.max_x > self.max_x:
            self.max_x = region.max_x
        if region.min_y < self.min_y:
            self.min_y = region.min_y
        if region.max_y > self.max_y:
            self.max_y = region.max_y
        region.min_y = 9999999
        region.min_x = 9999999
        region.max_y = 0
        region.max_x = 0
        region.number = self.number
        self.num_px += region.num_px
        region.num_px = 0
        self.px += region.px
        region.px = []


    def max_grow_x(self):
        val = self.width() * self.num_px
        if val < 1:
            return 0
        return round(math.log(val))


    def max_grow_y(self):
        val = self.height() * self.num_px
        if val < 1:
            return 0
        return round(math.log(val))


    def add_to_img(self, img, n):
        if self.value == 5:
            rgb = (255, 255, 255)
        elif self.value == 4:
            rgb = (0, 0, 0)
        elif self.value == 1:
            rgb = (255, 255, 0)
        else:
            rgb = object_colour_cycle[n % len(object_colour_cycle)]

        for y,x in self.px:
            img.putpixel((x,y), rgb)


    def __str__(self):
        return "Region %d of type %d with %d px %d height %d width and %d area" % (self.number, self.value, self.num_px, self.height(), self.width(), self.area())

    
    def consume_neighbors(self, im, regions):
        max_grow_x = self.max_grow_x()
        max_grow_y = self.max_grow_y()
        print("Region %d attempting to consume neighbors with grow_x=%d and grow_y=%d" % (self.number, max_grow_x, max_grow_y))

        '''
        Too tired I don't know what any of this does
        rect = []
        for i in range(self.height() + (2* max_grow_y):
            rect.append([0] * (self.width()+(2* max_grow_x)))

        h = self.height()
        w = self.width()
        for y,x in self.px:
            y -= self.min_y
            x -= self.min_x
            rect[y][x] = 1

        for y,x in self.px:
            y -= self.min_y
            x -= self.min_x
            if rect[y][x] == 1:
                num = 0
                right = 1
                while num < max_grow_x and x+num+right < w:
                    if rect[x+num+right][y] == 1:
                        rect[x+num+right][y] = 3
                        right += 1
                    elif rect[x+num+right][y] == 0:
                        rect[x+num+right][y] = 2
                        num += 1
                    else:
                        num += 1
                        continue

                num = 0
                left = 1
                while num < max_grow_x and x-num-left >= 0:
                    if rect[x-num-left][y]== 1:
                        rect[x-num-left][y] = 3
                        left += 1
                    elif rect[x-num-left] == 0:
                        rect[x-num-left] = 2
                        num += 1
                    else:
                        num += 1
                        continue

                num = 0
                down = 1
                while num < max_grow_y and y+num+down < h:
                    if rect[x][y+num+down] == 1:
                        rect[x][y+num+down] = 3
                    elif rect[x][y+num+down] == 0:
                        rect[x][y+num+down] = 2
                        num += 1
                    else:
                        num += 1
                        continue

                num = 0
                up = 1
                while num < max_grow_y and y-num-up >= 0:
                    if rect[x][y-num-up] == 1:
                        rect[x][y-num-up] = 3
                        up += 1
                    elif rect[x][y-num-up] == 0:
                        rect[x][y-num-up] = 2
                        num += 1
                    else:
                        num += 1
                        continue
                
                rect[y][x] = 3
        ''' 
        
        
                        

        '''
        very very very bad way of doing it
        a = 0
        while a < len(self.px):
            y,x = self.px[a]   
            for i in range(-max_grow_x, max_grow_x+1):
                for j in range(-max_grow_y, max_grow_y+1):
                    if i == 0 and j == 0:
                        continue
                    if x+i < 0 or x+i >= WIDTH or y+j < 0 or y+j >= HEIGHT:
                        continue
                    region = regions[im[y][x]]
                    if region.value == self.value and region.number != self.number:
                        print("Consuming region %d" % region.number)
                        self._merge(region)
                        max_grow_x = self.max_grow_x()
                        max_grow_y = self.max_grow_y()
            a += 1
        '''

regions = {}

# Do a floodfill on the picture, set the RGB value
def floodfill(im, x, y, new, region):
    val = im[y][x]
    q = []
    q.append((y, x))
    while not len(q) == 0:
        y, x = q.pop()
        if y < 0 or y >= HEIGHT or x < 0 or x >= WIDTH or im[y][x] != val:
            continue
        im[y][x] = new
        region.add_px(x, y)
        q.append((y+1, x))
        q.append((y-1, x))
        q.append((y, x+1))
        q.append((y, x-1))
    print(region)

#Outside of road IV
for y, x in outer_IV:
    r = Region(im[y][x], n)
    floodfill(im, x, y, n, r)
    regions[n] = r
n += 1

#Flood fill road IV
for y, x in road_IV:
    r = Region(im[y][x], n)
    floodfill(im, x, y, n, r)
    regions[n] = r
n += 1

#Flood fill line IV
for y, x in line_IV:
    r = Region(im[y][x], n)
    floodfill(im, x, y, n, r)
    regions[n] = r
n += 1

#if it hasn't been filled yet, do a floodfill operation
for y in range(0, HEIGHT):
    for x in range(0, WIDTH):
        if im[y][x] <= least:
            r = Region(im[y][x], n)
            floodfill(im, x, y, n, r)
            regions[n] = r
            n += 1

for key in regions:
    region = regions[key]
    if region.can_grow():
        region.consume_neighbors(im, regions)


for key in regions:
    region = regions[key]
    if region.num_px > 0:
        region.add_to_img(classified, n)
        n += 1

#save image
classified.save('classified.png')
print("Done...")

