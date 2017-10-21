import os
import sys
import math
import argparse
import cairo

import fonts

# TODO: Paper presets
# TODO: Shashechki

font_dict = {
    "1": "Roman square capitals",
    "2": "Antiqua Sans",
    "3": "Blackletter",
    "4": "Italic",
    "5": "Copperplate",
    "6": "Rustic",
    "7": "Insular script, Uncial, Ustav",
    "8": "Half-ustav",
    "9": "Caroline minuscule"
}

def main():
    '''Get args from command line'''
# Parser description:
    parser = argparse.ArgumentParser(
        description="Let's create the grid!",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-f", "--font", type=str, metavar="FONT", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"], required=True,
        help="Font which you want generate a grid for. Accepted values:\n" +
             "1 - " + font_dict["1"] + "\n" +
             "2 - " + font_dict["2"] + "\n" +
             "3 - " + font_dict["3"] + "\n" +
             "4 - " + font_dict["4"] + "\n" +
             "5 - " + font_dict["5"] + "\n" +
             "6 - " + font_dict["6"] + "\n" +
             "7 - " + font_dict["7"] + "\n" +
             "8 - " + font_dict["8"] + "\n" +
             "9 - " + font_dict["9"])
    parser.add_argument("-n", "--nib-size", type=float, metavar="NUMBER", required=True,
        help="Width of nib in millimeters. Accepted values:\n" +
             "0.2 ... 30")
    parser.add_argument("-o", "--output-file", type=str, metavar="FILEPATH", required=True)
    parser.add_argument("-t", "--type", type=str, metavar="FILETYPE", choices=["PDF", "PNG", "SVG"], default="PDF",
        help="Output filetype. Accepted values:\n" +
             "PDF (default), PNG, SVG")
    parser.add_argument("-x", "--x-paper", type=float, metavar="NUMBER", default=210,
        help="Paper width in millimeters. Accepted values:\n" +
             "100 ... 5000, default: 210")
    parser.add_argument("-y", "--y-paper", type=float, metavar="NUMBER", default=297,
        help="Paper heigth in millimeters. Accepted values:\n" +
             "100 ... 5000, default: 297")
    parser.add_argument("-m", "--margins", type=int, metavar="NUMBER", default=15,
        help="Margin size in millimeters (common for all edges). Actual only for PDF. Accepted values:\n" +
             "5 ... 30, default: 15")
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
    if (not 100 <= args.x_paper <= 5000) or (not 100 <= args.y_paper <= 5000):
        print("[ERROR] Wrong paper size")
        error_flag = 1

    if (not 5 <= args.margins <= 30):
        print("[ERROR] Wrong margin size")
        error_flag = 1

    if (not 1 <= args.resolution <= 2000):
        print("[ERROR] Wrong print resolution")
        error_flag = 1

    if error_flag != 0:
        sys.exit(1)

    # Ignore the nib size user decision if copperplate chosen:
    if args.font == "5":
        args.nib_size = 8.75
        print("[INFO] Nib size is ignored for copperplate grid")

    # Do not add margins if output format differs from PDF:
    if args.type != "PDF":
        if args.margins != 15:
            print("[INFO] Margins aren't used in formats other than PDF")
        args.margins = 0

    # Preserve the nib size to show it in the info string:
    global nib_mm
    nib_mm = args.nib_size

    return args


def prepare(raw_args):
    '''Transform values from millimeters to proper dimensions'''
    if raw_args.type == "PDF":
        # Computer points
        raw_args.nib_size = round(raw_args.nib_size/0.3527)
        raw_args.x_paper = round(raw_args.x_paper/0.3527)
        raw_args.y_paper = round(raw_args.y_paper/0.3527)
        raw_args.margins = round(raw_args.margins/0.3527)
    else:
        # Pixels
        raw_args.nib_size = round(raw_args.nib_size*raw_args.resolution/25.4)
        raw_args.x_paper = round(raw_args.x_paper*raw_args.resolution/25.4)
        raw_args.y_paper = round(raw_args.y_paper*raw_args.resolution/25.4)
        raw_args.margins = round(raw_args.margins*raw_args.resolution/25.4)

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


def draw_grid(surface, context, font, nib_size, field, margins):
    '''Choose proper draw function based on chosen font'''
    context.save()

    if font == "1":
        surface, context = fonts.roman_square_capitals(surface, context, nib_size, field, margins)
    elif font == "2":
        surface, context = fonts.antiqua_sans(surface, context, nib_size, field, margins)
    elif font == "3":
        surface, context = fonts.blackletter(surface, context, nib_size, field, margins)
    elif font == "4":
        surface, context = fonts.italic(surface, context, nib_size, field, margins)
    elif font == "5":
        surface, context = fonts.copperplate(surface, context, nib_size, field, margins)
    elif font == "6":
        # Rustic
        surface, context = fonts.rustic_ustav_minuscule(surface, context, nib_size, field, margins, 6)
    elif font == "7":
        # Ustav
        surface, context = fonts.rustic_ustav_minuscule(surface, context, nib_size, field, margins, 5)
    elif font == "8":
        # Half-ustav
        surface, context = fonts.rustic_ustav_minuscule(surface, context, nib_size, field, margins, 4)
    elif font == "9":
        # Minuscule
        surface, context = fonts.rustic_ustav_minuscule(surface, context, nib_size, field, margins, 3)
    else:
        sys.exit()

    context.restore()

    return surface, context


def draw_margins(surface, context, field, margins):
    '''Draw margins for PDF documents'''
    context.save()

    context.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    context.set_source_rgba(1, 1, 1, 1)
    context.rectangle(0 + margins, 0 + margins, field[0] - 2*margins, field[1] - 2*margins)
    context.rectangle(0, 0, field[0], field[1])
    context.stroke_preserve()
    context.fill()

    context.restore()

    return surface, context


def write_info(surface, context, font, nib_size, margins):
    '''Write the information about chosen grid and nib'''
    context.save()

    context.set_source_rgba(*fonts.main_line)
    text_props = context.text_extents("{}; {} mm".format(font_dict[font], nib_size))
    v_text_center = math.ceil(text_props[2]) # Width
    context.move_to(margins - 3, v_text_center + margins + 3)
    context.rotate(math.radians(270))
    context.show_text("{}; {} mm".format(font_dict[font], nib_size))

    context.restore()

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
    surface, context = draw_grid(surface, context, args.font, args.nib_size, (args.x_paper, args.y_paper), args.margins)
    if args.type == "PDF":
        surface, context = draw_margins(surface, context, (args.x_paper, args.y_paper), args.margins)
        surface, context = write_info(surface, context, args.font, nib_mm, args.margins)
    save_result(surface, context, args.type, args.output_file)