#!/bin/python

import sys
import getopt
from PIL import Image

#TODO seperate into "module"

edge_masks = {
        "Sobel": [
            [[1, 0, -1], [2, 0, -2], [1, 0, -1]], 
            [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], 
            [[-1, -2, -1], [0, 0, 0], [1, 2, 1]], 
            [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
            ],
        "Prewitt": [
            [[1, 0, -1], [1, 0, -1], [1, 0, -1]],
            [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]],
            [[-1, -1, -1], [0, 0, 0], [1, 1, 1]],
            [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
            ],
        "Kirsch": [
            [[5, -3, -3], [5, 0, -3], [5, -3, -3]], 
            [[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]],
            [[-3, -3, -3], [-3, 0, -3], [5, 5, 5]],
            [[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]
            ],
        }

#Some simple filters for applying a blur, that may or may not be any good
blurs = {
        "GreyScale": [
            42.5
        ],

        "Simple3": [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
            ],
        "Simple5": [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
            ],
        "Inner5": [
            [1, 1, 1, 1, 1],
            [1, 2, 2, 2, 1],
            [1, 2, 2, 2, 1],
            [1, 2, 2, 2, 1],
            [1, 1, 1, 1, 1]
            ],
        "HardInner5": [
            [1, 1, 1, 1, 1],
            [1, 3, 3, 3, 1],
            [1, 3, 3, 3, 1],
            [1, 3, 3, 3, 1],
            [1, 1, 1, 1, 1]
            ],
        "Simple7": [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1]
            ],
        "Inner7": [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 1],
            [1, 2, 3, 3, 3, 2, 1],
            [1, 2, 3, 3, 3, 2, 1],
            [1, 2, 3, 3, 3, 2, 1],
            [1, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1]
            ],
        "HardInner7": [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 1],
            [1, 2, 4, 4, 4, 2, 1],
            [1, 2, 4, 0, 4, 2, 1],
            [1, 2, 4, 4, 4, 2, 1],
            [1, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1]
            ],
        "Simple15": [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                ],
        "Simple35": [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ]
        } 

class _Filter(object):

    """Base Class for a Filter"""

    def __init__(self, im, filter_matrix=None, show_progress_bar=True):
        """Init for a base filter

        :im:            the image 
        :filter_matrix: the matrix to apply to each pixel
        :returns:       None

        """
        self.im = im
        self.height = len(im)
        if im:
            self.width = len(im[0])
        else:
            self.width = 0
        self.filter_matrix = filter_matrix
        self.progress_bar = ProgressBar(self.height)
        self.show_progress_bar = show_progress_bar


    def update(self, n):
        if self.show_progress_bar:
            self.progress_bar.update(n+1)


    def new_image(self):
        ret = []
        for y in range(self.height):
            ret.append([0] * self.width)
        return ret


    @staticmethod
    def _average(s, n):
        return sum(s) / n


    @staticmethod
    def filter_range(x):
        return range(-(x//2), x-(x//2))


class FloodFiller(_Filter):

    """Docstring for FloodFiller. TODO"""


    def __init__(self, im, growth, defaults={}, show_progress_bar=True):
        """TODO: to be defined1.

        :im: TODO
        :growth: TODO
        :defaults: TODO
        :show_progress_bar: TODO

        """
        _Filter.__init__(self, im, show_progress_bar=show_progress_bar)
        self.defaults = defaults
        self.growth = growth


    def fill(self):
        #TODO make object id generation not crappy
        #for now just assign a high value
        least = 9999
        n = least
        for y in range(self.height):
            self.update(y)
            for x in range(self.width):
                if self.im[y][x] < least:
                    if self.im[y][x] in self.defaults:
                        self._floodfill(x, y, self.defaults[ self.im[y][x] ])
                    elif self.im[y][x] not in self.defaults.values():
                        self._floodfill(x, y, n)
                        n += 1


    def _floodfill(self, x, y, number):
        """Does an iterative flood fill starting at spot x,y """
        val = self.im[y][x]
        q = []
        q.append((x, y))
        while len(q) > 0:
            x, y = q.pop()
            self.im[y][x] = number
            for i in range(-self.growth, self.growth+1):
                for j in range(-self.growth, self.growth+1):
                    if i == 0 and j == 0:
                        continue
                    if y+j < 0 or y+j >= self.height or x+i < 0 or x+i >= self.width or self.im[y+j][x+i] != val:
                        continue
                    q.append((x+i, y+j))


    def to_image(self, color_map=None, color_wheel=None):
        if color_map is None:
            color_map = {
                    7: (255, 255, 255),
                    8: (0, 0, 0),
                    9: (255, 255, 0),
                    }
            if color_wheel is None:
                color_wheel = [
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

                image = Image.new('RGBA', (self.width, self.height), 'BLACK')
        color_counter = 0
        for y in range(self.height):
            self.update(y)
            for x in range(self.width):
                if self.im[y][x] not in color_map:
                    color_map[self.im[y][x]] = color_wheel[color_counter]
                    color_counter = (color_counter + 1) % len(color_wheel)
                image.putpixel((x, y), color_map[self.im[y][x]])

        return image


class EdgeGrower(object):

    """Docstring for EdgeGrower. TODO"""

    def __init__(self, im, show_progress_bar=True):
        """TODO: to be defined1.

        :im: TODO

        """
        self._im = im
        self.show_progress_bar = show_progress_bar


    def update(self, n):
        if self.show_progress_bar:
            self.progress_bar.update(n+1)


    def grow(self, threshold):
        pass


class SimpleBlurFilter(_Filter):

    """Docstring for SimpleBlurFilter. TODO"""

    def __init__(self, im, filter_matrix, threshold=None, show_progress_bar=True):
        """Init for SimpleBlurFilter

        :im: TODO
        :filter_matrix: TODO

        """
        _Filter.__init__(self, im, filter_matrix, show_progress_bar=show_progress_bar)
        self.threshold = threshold


    def filter(self, display_averages=False):
        filter_length = len(self.filter_matrix)
        filter_total = filter_length * filter_length
        half = filter_length // 2
        new_image = self.new_image()

        for y in range(half, self.height-half):
            self.update(y+half)
            for x in range(half, self.width-half):
                total = 0
                for a in _Filter.filter_range(filter_length):
                    for b in _Filter.filter_range(filter_length):
                        total += self.im[y+a][x+b] * self.filter_matrix[a+half][b+half]
                total = round(total/filter_total)
                if display_averages:
                    print("%d" % (total))
                if self.threshold is not None:
                    if total >= self.threshold:
                        new_image[y][x] = 255
                else:
                    new_image[y][x] = total

        return new_image


class EdgeFilter(_Filter):

    """Edge detection filter"""

    def __init__(self, im, filter_matrix, show_progress_bar=True, edge_grower=None):
        """Build an edge filter

        :im: TODO
        :filter_matrix: TODO

        """
        _Filter.__init__(self, im, filter_matrix[0], show_progress_bar=show_progress_bar)

        self.filter_matrix_left  = filter_matrix[0]
        self.filter_matrix_right = filter_matrix[1]
        self.filter_matrix_up    = filter_matrix[2]
        self.filter_matrix_down  = filter_matrix[3]
        self.edge_grower = edge_grower


    def filter(self):
        filter_length = len(self.filter_matrix)
        half = filter_length//2
        im_l = self.new_image()
        im_r = self.new_image()
        im_u = self.new_image()
        im_d = self.new_image()
        new_image = self.new_image()
        sum_lookup = [0, 51, 102, 153, 204]
        for y in range(half, self.height-half):
            self.update(y+half)
            for x in range(half, self.width-half):
                left  = 0
                right = 0
                up    = 0
                down  = 0
                for a in _Filter.filter_range(filter_length):
                    for b in _Filter.filter_range(filter_length):
                        left  += self.im[y+a][x+b] * self.filter_matrix_left[a+half][b+half]
                        right += self.im[y+a][x+b] * self.filter_matrix_right[a+half][b+half]
                        up    += self.im[y+a][x+b] * self.filter_matrix_up[a+half][b+half]
                        down  += self.im[y+a][x+b] * self.filter_matrix_down[a+half][b+half]

                if self.edge_grower is None:
                    sumup = 0
                    if left > 0:
                        sumup += 1
                    if right > 0:
                        sumup += 1
                    if up > 0:
                        sumup += 1
                    if left > 0:
                        sumup += 1
                    new_image[y][x] = sum_lookup[sumup]
                else:
                    im_l[y][x] = left
                    im_r[y][x] = right
                    im_u[y][x] = up
                    im_d[y][x] = down

        if self.edge_grower is not None:
            new_image = self.edge_grower.grow_edges(new_image, {'left': im_l, 'right': im_r, 'up': im_u, 'down': im_d } )

        return new_image


class ImageLoader(object):

    """Loads an image file into an array"""

    def __init__(self, filename, show_progress_bar=True, delimiter=' '):
        """Build an object to load various images
        :filename: the filename of the image
        :delimiter: the field delimiter on the image
        :message: the message to display while loading

        """
        self.filename = filename
        self.im = []
        self.delimiter = delimiter
        self.show_progress_bar = show_progress_bar
        self.load_image()


    def load_image(self):
        """loads the image at spot 'filename'
        :returns: TODO

        """
        with open(self.filename) as data:
            count = sum([1 for _ in data])
            data.seek(0)
            self.progress_bar = ProgressBar(count)
            x,y = 0,0
            for line in data:
                data_line = []
                self.update(y+1)
                for num in line.split(self.delimiter):
                    try:
                        n = int(num)
                    except:
                        continue
                    data_line.append(n)
                    x += 1
                self.im.append(data_line)
                y += 1
                x  = 0


    def get_image(self):
        return self.im


    def update(self, n):
        """Display an updating progress bar in terminal

        :n: TODO
        :returns: TODO

        """
        if self.show_progress_bar:
            self.progress_bar.update(n)


class BlackAlphaImageSaver(object):

    """Docstring for BlackAlphaImageSaver. TODO"""

    def __init__(self, im, colorstyle='RGBA' , rgba=(255, 255, 255, 0), display_progress_bar=True):
        """TODO: to be defined1.

        :image: TODO

        """

        self.image = Image.new(colorstyle, (len(im[0]), len(im)), rgba)
        self.display_progress_bar = display_progress_bar

        self.progress = ProgressBar(len(im))
        for y in range(len(im)):
            if self.display_progress_bar:
                self.progress.update(y+1)
            for x in range(len(im[0])):
                self.image.putpixel((x,y), (0, 0, 0, im[y][x]))


    def save(self, name):
        self.image.save(name)   


class ProgressBar(object):

    """Docstring for ProgressBar. TODO"""

    def __init__(self, size, barLength=40):
        """TODO: to be defined1.

        :size: TODO

        """
        self.size = size
        self.barLength = barLength

    def update(self, n):
        self._drawProgressBar(n / self.size, self.barLength)


    @staticmethod
    def _drawProgressBar(percent_done, barLength):
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



def usage(name, message=''):
    if message != '':
        print(message)
    print()
    print('Usage: python ', name, ' --data=sample.txt --alg=Edge <options>')
    print('Options are:')
    print('  -d, --data          the road data file being analyzed')
    print('  -a, --alg           comma seperated list of algorithms to apply listed in the order of application, Edge,Blur,Floodfill... etc')
    print('  -e, --edge-filter   the edge detection filter to apply default is Sobel. Options are Sobel, Kirsch, and Prewitt')
    print('  -b, --blur-filter   the blue filter to apply default is Simple5. Options Simple3, Simple5, Inner5, Simple7, Inner7, HardInner7, Simple15')
    print('  -t, --threshold     if alg=Floodfill the default is 0, else if alg=Edge then the default is None')
    print('  -i, --image         tell the program to save an image at the end')
    print('  -p, --progress      tell the program to display progress bars and updates')
    print('  -g, --growth        how many pixels grace on object connectivity when doing floodfill')
    print('  -h, --help          display usage')
    print()
    print()
    exit(1)


def main():

    show_progress = False
    data = ''
    alg = 'edge'
    edge_type = 'Sobel'
    blur_type = 'Simple5'
    threshold = None
    growth_limit = 1
    image = False

    name = sys.argv[0]
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d::a::e:b:t:iphg:", ["data=", "alg=", "edge-filter=", "blur-filter=", "threshold=", "image", "progress", "help", "growth="])
    except getopt.GetoptError:
        usage(name)

    for o,a in opts:
        if o in ('-a', '--alg'):
            alg = a
        elif o in ('-d', '--data'):
            data = a
        elif o in ('-e', '--edge-filter'):
            edge_type = a
        elif o in ('-b', '--blur-filter'):
            blur_type = a
        elif o in ('-t', '--threshold'):
            try:
                threshold = int(a)
            except ValueError:
                usage(name, "Threshold must be an integer")
        elif o in ('-i', '--image'):
            image = True
        elif o in ('-p', '--progress'):
            show_progress = True
        elif o in ('-h', '--help'):
            usage(name)
        elif o in ('-g', '--growth'):
            try:
                growth_limit = int(a)
            except ValueError:
                usage(name, "Growth must be an integer")
        else:
            usage(name)

    #TODO make this not crappy, should probably use os 
    #split unix filepaths 
    filename = data.split('/')[-1]
    #split windows filepaths
    filename = filename.split(r'\\')[-1]
    #remove file_extension
    filename = filename.split('.')[0]

    if edge_type not in edge_masks:
        usage(name, "Available edge filters are " + ", ".join(edges.keys()))
    edge_filter = edge_masks[edge_type]

    if blur_type not in blurs:
        usage(name, "Available blur filters are " + ", ".join(blurs.keys()))
    blur_filter = blurs[blur_type]

    if show_progress:
        print('Loading Image %s \n' % data)

    im = ImageLoader(data, show_progress_bar=show_progress).get_image()

    if show_progress:
        print('\n')

    algorithms = [s.strip() for s in alg.split(',')]
    if not algorithms:
        usage()

    #quickly validate algs before doing any processing so we don't do too much work
    for algorithm in algorithms:
        if algorithm not in ('edge', 'floodfill', 'blur'):
            usage('%s not a known algorithm know algorithms are edge, blur and floodfill' % algorithm)

    for algorithm in algorithms:
        if show_progress:
            print("Applying %s algorithm..." % algorithm)

        if algorithm == 'floodfill':

            defaults = {
                    0: 7, # outer ring gets set to a zero if it's blurred
                    5: 7, # outside of road to a 7
                    4: 8, # inside of road to an 8
                    1: 9, # line on road to a 9
                    }

            ff = FloodFiller(im, growth_limit, defaults, show_progress_bar=show_progress)
            ff.fill()
            if show_progress:
                print('\n')
                print("Applying color to image...")
            imsav = ff.to_image()
            if show_progress:
                print('\n')
                print("Saving image...")
            imsav.save('images/%s_%s_%d.png' % (filename, '+'.join(algorithms), growth_limit))
            exit(0)

        elif algorithm == 'edge':
            im = EdgeFilter(im, edge_filter, show_progress_bar=show_progress).filter()
            if show_progress:
                print('\n')

        elif algorithm == 'blur':
            im = SimpleBlurFilter(im, blur_filter, threshold=threshold, show_progress_bar=show_progress).filter(display_averages=False)
            if show_progress:
                print('\n')

    if edge_type is None:
        edge_type = 'None'
    if blur_type is None:
        blur_type = 'None'
    threshold = str(threshold)

    if image:
        if show_progress:
            print('Saving images...')
        imsav = BlackAlphaImageSaver(im)
        #save edge image
        imsav.save('images/%s_%s_%s_%s.png' % (filename, edge_type, blur_type, threshold))
        if show_progress:
            print('\n')
            print('Done...')
    else:
        if show_progress:
            print("Saving data...")
        with open('data/%s_%s_%s_%s.txt' % (filename, edge_type, blur_type, threshold), 'w') as im_file:
            for line in im:
                im_file.write(' '.join([str(x) for x in line]))
                im_file.write('\n')
        if show_progress:
            print("Done...")


if __name__ == '__main__':
    main()

