import argparse
import shutil
import os
import sys
import glob
import subprocess

DEFAULT_CROP_COMMAND = '%(in_image)s -trim %(out_image)s'


def make_parser():
    parser = argparse.ArgumentParser(description='Crop image with whitespace.', 
            epilog='The program requires `magick.exe` on environment variable '
            'Path. If it\'s not, error will be raised at the beginning of '
            'the program.')
    parser.add_argument('images', metavar='IMGPATH', nargs='+', 
            help='the path of image(s) to crop; support Python glob pattern')
    parser.add_argument('-o', metavar='PATH', dest='out_image', help='write '
            'the output to that file if there is only one input image; '
            'if there are multiple input images, the use of `-o` option '
            'terminates the program before raising error; if this option '
            'is not used, the output image(s) OVERWRITES the input image(s)')
    return parser

def gen_command(magick_path, crop_command, in_image, out_image=None):
    if out_image is None:
        out_image = in_image
    crop_command = crop_command % {'in_image': in_image, 
                                   'out_image': out_image}
    return [magick_path] + crop_command.split()

def crop(magick_command):
    subprocess.call(magick_command, cwd=os.path.abspath(os.path.curdir))

def main():
    args = make_parser().parse_args(sys.argv[1:])
    if os.name == 'nt':
        inputimages = []
        for globpattern in args.images:
            inputimages.extend(glob.glob(globpattern))
    else:
        inputimages = args.images
    if len(inputimages) > 1 and args.out_image is not None:
        print('Error: multiple input images crop to one output')
        sys.exit(1)
    
    magick_path = shutil.which('magick')
    if magick_path is None:
        print('`magick\' not found')
        sys.exit(1)

    for filename in inputimages:
        magick_command = gen_command(magick_path, DEFAULT_CROP_COMMAND, 
                                     filename, args.out_image)
        crop(magick_command)

if __name__ == '__main__':
    main()
