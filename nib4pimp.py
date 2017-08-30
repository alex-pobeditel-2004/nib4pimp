import os
import sys
import math
import argparse
import cairo

import fonts
# TODO: MANUAL HEX COLORS
# TODO: Paper presets
# TODO: Type name in the corner

def main():
    '''Get args from command line'''
# Parser description:
    parser = argparse.ArgumentParser(
        description="Let's create the grid!",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # debug: remove default, add required later
    parser.add_argument("-f", "--font", type=str, metavar="FONT", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"], default="1",
        help="Font which you want generate a grid for. Accepted values:\n" +
             "1 - Roman square capitals\n" +
             "2 - Antiqua Sans\n" +
             "3 - Blackletter\n" +
             "4 - Italic\n" +
             "5 - Copperplate (ignores nib size)\n" +
             "6 - Rustic\n" +
             "7 - Insular script, Uncial, Ustav\n" +
             "8 - Half-ustav\n" +
             "9 - Caroline minuscule")
    parser.add_argument("-n", "--nib-size", type=float, metavar="NUMBER", required=True,
        help="Width of nib in millimeters. Accepted values:\n" +
             "0.2 ... 30")
    parser.add_argument("-o", "--output-file", type=str, metavar="FILEPATH", required=True)
    parser.add_argument("-t", "--type", type=str, metavar="FILETYPE", choices=["PDF", "PNG", "SVG"], default="PDF",
        help="Output filetype. Accepted values:\n" +
             "PDF (default), PNG, SVG")
    parser.add_argument("-x", "--x-paper", type=float, metavar="NUMBER", default=210,
        help="Paper width in millimeters. Accepted values:\n" +
             "50 ... 5000, default: 210")
    parser.add_argument("-y", "--y-paper", type=float, metavar="NUMBER", default=297,
        help="Paper heigth in millimeters. Accepted values:\n" +
             "50 ... 5000, default: 297")
    parser.add_argument("-r", "--resolution", type=int, metavar="NUMBER", default=300,
        help="DPI value for PNG/SVG images Accepted values:\n" +
             "1 ... 2400, default: 300")
    args = parser.parse_args()

# Argument checks:
    error_flag = 0

    try:
        if os.path.isfile(args.output_file):
            test_output = open(args.output_file, "r+")
            test_output.close()
        else:
            test_output = open(args.output_file, "w")
            test_output.close()
            os.remove(args.output_file)
    except:
        print("[ERROR] Cannot write to the output file, check path existence or your write permissions")
        error_flag = 1

    if not 0.2 <= args.nib_size <= 30:
        print("[ERROR] Wrong nib size")
        error_flag = 1
    if (not 50 <= args.x_paper <= 5000) or (not 50 <= args.y_paper <= 5000):
        print("[ERROR] Wrong paper size")
        error_flag = 1

    if (not 1 <= args.resolution <= 2000):
        print("[ERROR] Wrong print resolution")
        error_flag = 1

    if error_flag != 0:
        sys.exit(1)

    # Ignore the nib size user decision if copperplate chosen:
    if args.font == "5":
        args.nib_size = 8.75

    return args


def prepare(raw_args):
    '''Transform values from millimeters to proper dimensions'''
    if raw_args.type == "PDF":
        # Computer points
        raw_args.nib_size = round(raw_args.nib_size/0.3527)
        raw_args.x_paper = round(raw_args.x_paper/0.3527)
        raw_args.y_paper = round(raw_args.y_paper/0.3527)
    else:
        # Pixels
        raw_args.nib_size = round(raw_args.nib_size*raw_args.resolution/25.4)
        raw_args.x_paper = round(raw_args.x_paper*raw_args.resolution/25.4)
        raw_args.y_paper = round(raw_args.y_paper*raw_args.resolution/25.4)

    return raw_args


def create_surface(paper_size, filetype, output):
    '''Create proper surface based on chosen output file format'''
    if filetype == "PDF":
        surface = cairo.PDFSurface(output, *paper_size)
    elif filetype == "PNG":
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *paper_size)
    else:
        surface = cairo.SVGSurface(output, *paper_size)

    context = cairo.Context(surface)

    return surface, context


def draw_grid(surface, context, font, nib_size, field):
    '''Choose proper draw function based on chosen font'''
    if font == "1":
        surface, context = fonts.roman_square_capitals(surface, context, nib_size, field)
    elif font == "2":
        surface, context = fonts.antiqua_sans(surface, context, nib_size, field)
    elif font == "3":
        surface, context = fonts.blackletter(surface, context, nib_size, field)
    elif font == "4":
        surface, context = fonts.italic(surface, context, nib_size, field)
    elif font == "5":
        surface, context = fonts.copperplate(surface, context, nib_size, field)
    elif font == "6":
        # Rustic
        surface, context = fonts.rustic_ustav_minuscule(surface, context, nib_size, field, 6)
    elif font == "7":
        # Ustav
        surface, context = fonts.rustic_ustav_minuscule(surface, context, nib_size, field, 5)
    elif font == "8":
        # Half-ustav
        surface, context = fonts.rustic_ustav_minuscule(surface, context, nib_size, field, 4)
    elif font == "9":
        # Minuscule
        surface, context = fonts.rustic_ustav_minuscule(surface, context, nib_size, field, 3)
    else:
        sys.exit()

    return surface, context


def save_result(surface, context, filetype, output):
    '''Choose proper save function based on chosen output file format'''
    if filetype in ["PDF", "SVG"]:
        context.show_page()
    else:
        surface.write_to_png(output)


if __name__ == "__main__":
    raw_args = main()
    args = prepare(raw_args)
    surface, context = create_surface((args.x_paper, args.y_paper), args.type, args.output_file)
    surface, context = draw_grid(surface, context, args.font, args.nib_size, (args.x_paper, args.y_paper))
    save_result(surface, context, args.type, args.output_file)