import os
import sys
import math
import argparse
import cairo

# TODO: MANUAL HEX COLORS
# TODO: Paper presets
# TODO: Type name in the corner

main_line = [0.6, 0.6, 0.6, 1]
aux_line =  [0.933, 0.933, 0.933, 1]

def main():
    '''Get args from command line'''
# Parser description:
    parser = argparse.ArgumentParser(
        description="Let's create the grid!",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # debug: remove default, add required later
    parser.add_argument("-f", "--font", type=str, metavar="FONT", choices=["trojan", "antiqua"], default="trojan",
        help="Font which you want generate a grid for.\n" +
             "Accepted values: trojan, antiqua")
    parser.add_argument("-n", "--nib-size", type=float, metavar="NUMBER", required=True, help="Width of nib in millimeters (0.2...30)")
    parser.add_argument("-o", "--output-file", type=str, metavar="FILEPATH", required=True)
    parser.add_argument("-t", "--type", type=str, metavar="FILETYPE", choices=["PDF", "PNG", "SVG"], default="PDF",
        help="Output filetype.\n" + 
             "Accepted values: PDF, PNG, SVG")
    parser.add_argument("-x", "--x-paper", type=float, metavar="NUMBER", default=210, help="Paper width in millimeters (50...5000)")
    parser.add_argument("-y", "--y-paper", type=float, metavar="NUMBER", default=297, help="Paper heigth in millimeters (50...5000)")
    parser.add_argument("-r", "--resolution", type=int, metavar="NUMBER", default=300, help="DPI value for PNG/SVG images (1...2400)")
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
    if font == "trojan":
        surface, context = trojan(surface, context, nib_size, field)
    elif font == "antiqua":
        surface, context = antiqua(surface, context, nib_size, field)

    return surface, context


def trojan(surface, context, step, field):
    '''This function realizes the grid for the trojan font'''
    xpos = 0
    ypos = 0
    context.set_line_width(1)
    context.set_line_join(cairo.LINE_JOIN_MITER)
    while ypos < field[1]:
        while xpos < field[0]:
            context.set_source_rgba(*aux_line)
            # Surrounding rectangles:
                # x, y, width, height
            for args in [(step,      0,     10*step, step),
                         (step,    11*step, 10*step, step),
                         (0,       step,    step,    10*step),
                         (11*step, step,    step,    10*step)]:
                context.rectangle(xpos + args[0], ypos + args[1], args[2], args[3])
                context.stroke()

            context.set_line_width(0.5)
            # Circles:
                # x, y
            for args in [(1*step,    2*step),
                           (4*step,    2*step),
                           (8*step,    2*step),
                           (11*step,   2*step),
                           (1*step,    10*step),
                           (4*step,    10*step),
                           (8*step,    10*step),
                           (11*step,   10*step)]:
                context.arc(xpos + args[0], ypos + args[1], step*0.96, 0, 2*math.pi)
                context.stroke()
            
            context.set_line_width(1)
            # Small squares:
            for y in range(0,10):
                for x in range(0,10):
                    context.rectangle(xpos + (1 + x)*step, ypos + (1 + y)* step, step, step)
                    context.stroke()

            context.set_source_rgba(*main_line)
            # Main squares:
            context.rectangle(xpos + step, ypos + step, 10*step, 10*step)
            context.stroke()

            # Main lines:
            context.move_to(xpos + 6*step, ypos)
            context.line_to(xpos + 6*step, ypos + 12*step)
            context.move_to(xpos, ypos + 6*step)
            context.line_to(xpos + 12*step, ypos + 6*step)
            context.stroke()

            xpos += 12*step
        xpos = 0
        ypos += 12*step

    return surface, context


def antiqua(surface, context, step, field):
    '''This function realizes the grid for the antiqua font'''
    xpos = 0
    ypos = 0
    # Define multiplier for this grid:
    multiplier = math.cos(math.radians(25))
    # Find the vertical delta for a 25 degrees line for chosen paper:
    y_delta = field[0]*math.tan(math.radians(25))

    context.set_source_rgba(*aux_line)
    context.set_line_width(1)
    context.set_line_join(cairo.LINE_JOIN_MITER)

    # Diagonal lines:
    while ypos < field[1] + y_delta:
        context.move_to(0, ypos + multiplier*step)
        context.line_to(field[0], ypos - y_delta)
        context.stroke()
        ypos += multiplier*step

    ypos = 0
    while ypos < field[1]:
        while xpos < field[0]:
            # Aux vertical lines:
            context.set_source_rgba(*aux_line)
            context.move_to(xpos + 2*multiplier*step, ypos + 2*multiplier*step)
            context.line_to(xpos + 2*multiplier*step, ypos + 8*multiplier*step)
            context.move_to(xpos + 3*multiplier*step, ypos + 2*multiplier*step)
            context.line_to(xpos + 3*multiplier*step, ypos + 8*multiplier*step)
            context.stroke()
            xpos += 6*multiplier*step
        xpos = 0
        # Main horizontal lines:
        context.set_source_rgba(*main_line)
        context.move_to(0, ypos + 2*multiplier*step)
        context.line_to(field[0], ypos + 2*multiplier*step)
        context.move_to(0, ypos + 8*multiplier*step)
        context.line_to(field[0], ypos + 8*multiplier*step)
        context.stroke()
        ypos += 8*multiplier*step

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