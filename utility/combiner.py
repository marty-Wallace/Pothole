#!/bin/python

from PIL import Image


def combiner(images):
    im1 = images.pop(0)
    for im in images:
        im1.paste(im, (0, 0), im)
    return im1


def main(args):
    images = [Image.open(arg) for arg in args]
    
    new_image_name = '+'.join([name.split('/')[-1].split('.')[0] for name in args])

    image = combiner(images)
    image.show()
    image.save('images/%s.png' % new_image_name)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])


