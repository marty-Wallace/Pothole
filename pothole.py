import sys
from PIL import Image



masks = {
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

blurs = {
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


}




class _Filter(object):

    """Base Class for a Filter"""

    def __init__(self, im, filter_matrix):
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


    def update(self, n):
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



class EdgeGrower(object):

    """Docstring for EdgeGrower. """

    def __init__(self, im):
        """TODO: to be defined1.

        :im: TODO

        """
        self._im = im


    def update(self, n):
        self.progress_bar.update(n+1)
        

    def grow(self, threshold):
        pass
        


class SimpleBlurFilter(_Filter):

    """Docstring for SimpleBlurFilter. """

    def __init__(self, im, filter_matrix, threshold=None):
        """Init for SimpleBlurFilter

        :im: TODO
        :filter_matrix: TODO

        """
        _Filter.__init__(self, im, filter_matrix)
        self.threshold = threshold


    def filter(self):
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
                total //= filter_total
                if self.threshold is not None:
                    if total >= self.threshold:
                        new_image[y][x] = 255
                else:
                    new_image[y][x] = total
        
        return new_image


class EdgeFilter(_Filter):

    """Edge detection filter"""

    def __init__(self, im, filter_matrix):
        """Build an edge filter

        :im: TODO
        :filter_matrix: TODO

        """
        _Filter.__init__(self, im, filter_matrix[0])

        self.filter_matrix_left  = filter_matrix[0]
        self.filter_matrix_right = filter_matrix[1]
        self.filter_matrix_up    = filter_matrix[2]
        self.filter_matrix_down  = filter_matrix[3]


    def filter(self):
        filter_length = len(self.filter_matrix)
        half = filter_length//2
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

        return new_image



class ImageLoader(object):

    """Loads an image file into an array"""

    def __init__(self, filename, delimiter=' '):
        """Build an object to load various images
        :filename: the filename of the image
        :delimiter: the field delimiter on the image
        :message: the message to display while loading

        """
        self.filename = filename
        self.im = []
        self.delimiter = delimiter
        
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
                self.progress_bar.update(y+1)
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
        print()


    def get_image(self):
        return self.im
            

    def update(self, n, c):
        """Display an updating progress bar in terminal

        :n: TODO
        :returns: TODO

        """
        self.progress_bar.update(n/c)


class BlackAlphaImageSaver(object):

    """Docstring for BlackAlphaImageSaver. """

    def __init__(self, im, colorstyle='RGBA' , rgba=(255, 255, 255, 0)):
        """TODO: to be defined1.

        :image: TODO

        """

        self.image = Image.new(colorstyle, (len(im[0]), len(im)), rgba)
        progress = ProgressBar(len(im))
        for y in range(len(im)):
            progress.update(y+1)
            for x in range(len(im[0])):
                self.image.putpixel((x,y), (0, 0, 0, im[y][x]))
    

    def save(self, name):
        self.image.save(name)   


class ProgressBar(object):

    """Docstring for ProgressBar. """

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




def main():

    IMAGE_NAME = 'data/road.txt'
    if len(sys.argv) > 1:
        IMAGE_NAME = sys.argv[1]

    mask_type = 'Prewitt'
    if len(sys.argv) > 2:
        mask_type = sys.argv[2]

    mask_filter = masks[mask_type]

    blur_type = 'Inner5'
    if len(sys.argv) > 3:
        blur_type = sys.argv[3]

    blur_filter = blurs[blur_type]

    threshold=100
    if len(sys.argv) > 4:
        threshold = int(sys.argv[4])


    print("Loading image %s..." % IMAGE_NAME)
    im = ImageLoader(IMAGE_NAME).get_image()
    print('\n')

    print("Applying edge filter %s..." % mask_type)
    im = EdgeFilter(im, mask_filter).filter()
    print('\n')

    print("Applying Blur filter %s..." % blur_type)
    im = SimpleBlurFilter(im, blur_filter, threshold=100).filter()
    print('\n')

    print("Saving image")
    imsav = BlackAlphaImageSaver(im)
    print('\n')


    #TODO make this not crappy
    #split unix filepaths 
    filename = IMAGE_NAME.split('/')[-1]
    #split windows filepaths
    filename = filename.split(r'\\')[-1]
    #remove file_extension
    filename = filename.split('.')[0]

    #save edge image
    imsav.save('images/%s_%s_%s_%d.png' % (filename, mask_type, blur_type, threshold))
    print("Done...")

if __name__ == '__main__':
    main()

