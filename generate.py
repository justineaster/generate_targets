from PIL import Image,ImageDraw,ImageFont,ImageColor,ImageOps,ImageFilter
import random as rand
import math
import argparse
import Target
import os
import sys

def get_color(color_name='random'):
    '''Generate random color unless specified
    Args:
        color_name: color name string

    Returns:
        color_code: hue, saturation, luminance string
        color_name: color name string
    '''

    if color_name == 'random':
        color_name = rand.choice(Target.Color)

    saturation = rand.randint(50, 100)
    luminance = rand.randint(40, 60)

    if color_name == 'red':
        hue = rand.randint(0, 4)
    elif color_name == 'orange':
        hue = rand.randint(9, 33)
    elif color_name == 'yellow':
        hue = rand.randint(43, 55)
    elif color_name == 'green':
        hue = rand.randint(75, 120)
    elif color_name == 'blue':
        hue = rand.randint(200, 233)
    elif color_name == 'purple':
        hue = rand.randint(266, 291)
    elif color_name == 'brown':
        hue = rand.randint(13, 20)
        saturation = rand.randint(25, 50)
        luminance = rand.randint(22, 40)
    elif color_name == 'black':
        hue = rand.randint(0, 360)
        saturation = rand.randint(0, 12)
        luminance = rand.randint(0, 13)
    elif color_name == 'gray':
        hue = rand.randint(0, 360)
        saturation = rand.randint(0, 12)
        luminance = rand.randint(25, 60)
    elif color_name == 'white':
        hue = rand.randint(0, 360)
        saturation = rand.randint(0, 12)
        luminance = rand.randint(75, 100)
    else:
        sys.exit('color not found')
    color_code = 'hsl(%d, %d%%, %d%%)' % (hue, saturation, luminance)
    return color_code, color_name

def draw_rectangle(draw, size, color_code):
    rectangle_width = size[0]*rand.randint(50,65)/100
    rectangle_height = size[0]*rand.randint(85,97)/100

    border_width = (size[0] - rectangle_width)/2
    border_height = (size[0] - rectangle_height)/2
    top=(border_width, border_height)
    bottom=(size[0]-border_width, size[0]-border_height)
    draw.rectangle([top, bottom], fill=color_code)


def draw_text(draw, size, color_code):
    '''Draw random alphanumeric

    Args:
        draw: ImageDraw.Draw
        size: max size of target in pixels
        color_code: hsl color string

    Returns:
        text: the alphanumeric that was drawn
    '''
    font_location="FreeSansBold.ttf"
    font = ImageFont.truetype(font_location, size=int(size[0]*50/100))
    text = rand.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    text_width, text_height = draw.textsize(text, font)
    text_pos = ((size[0]-text_width)/2, (size[1]-text_height)/2)
    draw.text(text_pos, text, fill=color_code, font=font)
    return text

def create_target(size, background, save_name):
    im = Image.new('RGBA', size, color=(0,0,0,0))
    draw = ImageDraw.Draw(im)
    shape_color_code, shape_color = get_color('white')
    text_color_code, text_color = get_color()

    shape = draw_rectangle(draw, size, shape_color_code)
    text = draw_text(draw, size, text_color_code)
    im = ImageOps.expand(im, border=int(size[0]*10/100), fill=(0))
    orientation=rand.randint(0,355)
    im = im.rotate(orientation)
    im = im.filter(ImageFilter.GaussianBlur(radius=args.blur))

    crop_left = rand.randint(0, background.width - im.width)
    crop_right = crop_left + im.width
    crop_top = rand.randint(0, background.height - im.height)
    crop_bottom = crop_top + im.height
    crop_box = (crop_left, crop_top, crop_right, crop_bottom)
    cropped_background = background.crop(crop_box)
    im = Image.alpha_composite(cropped_background, im)
    im = im.convert('RGB')
    del draw # done drawing
    im.save(save_name + '.png', 'PNG')
    return shape_color, text_color, shape, text, orientation

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'generate targets')

    parser.add_argument('-s', '--size', type=int, default = 50,
            help='max size in pixels of target')

    parser.add_argument('-n', '--number', type=int, default = 1,
            help='number of targets to generate')

    parser.add_argument('-b', '--blur', type=int, default = 1,
            help='gaussian blur pixel radius')

    args = parser.parse_args()
    size = (args.size, args.size)
    f = open('imgpath_label.txt', 'w')
    script_path = os.path.dirname(os.path.abspath(__file__))
    background = Image.open(script_path + "/background.jpg").convert('RGBA')
    cwd = os.getcwd()
    for n in range(args.number):
        save_name = "target" + str(n).zfill(8)
        shape_color, text_color, shape, text, orientaion = create_target(size, background, save_name)
        f.write(cwd + '/' + save_name + '.png' + '\n')

    f.close()
