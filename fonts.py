import math
import cairo

main_line =  [0.6, 0.6, 0.6, 1]
aux_line =   [0.933, 0.933, 0.933, 1]
aux_line_2 = [0.733, 0.733, 0.733, 1]
bg_color =   [0.97, 0.97, 0.97, 1]

def roman_square_capitals(surface, context, step, field):
    '''This function realizes the grid for the roman square capitals'''
    xpos = 0
    ypos = 0

    context.set_line_width(0.5)
    context.set_line_cap(cairo.LINE_CAP_SQUARE)
    context.set_line_join(cairo.LINE_JOIN_MITER)

    while ypos < field[1]:
        while xpos < field[0]:
            # Surrounding rectangles:
            context.set_source_rgba(*aux_line)
                # x, y, width, height
            for args in [(step,    0,       10*step, step),
                         (step,    11*step, 10*step, step),
                         (0,       step,    step,    10*step),
                         (11*step, step,    step,    10*step)]:
                context.rectangle(xpos + args[0], ypos + args[1], args[2], args[3])
            context.stroke()

            # Circles:
            context.set_line_width(0.3)
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

            # Small squares:
            context.set_line_width(0.5)
            for y in range(0,10):
                for x in range(0,10):
                    context.rectangle(xpos + (1 + x)*step, ypos + (1 + y)* step, step, step)
            context.stroke()

            # Main squares:
            context.set_source_rgba(*main_line)
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


def antiqua_sans(surface, context, step, field):
    '''This function realizes the grid for the antiqua sans'''
    xpos = 0
    ypos = 0
    # Define multiplier for this grid:
    multiplier = math.cos(math.radians(25))

    context.set_line_width(0.5)
    context.set_line_cap(cairo.LINE_CAP_SQUARE)
    context.set_line_join(cairo.LINE_JOIN_MITER)

    # Find the vertical delta for a 25 degrees line for chosen paper:
    y_delta = field[0]*math.tan(math.radians(25))
    # Diagonal lines:
    context.set_source_rgba(*aux_line)
    while ypos < field[1] + y_delta:
        context.move_to(0, ypos + multiplier*step)
        context.line_to(field[0], ypos - y_delta)
        ypos += multiplier*step
    context.stroke()

    ypos = 0
    while ypos < field[1]:
        while xpos < field[0]:
            # Aux vertical lines:
            context.set_source_rgba(*aux_line)
            context.move_to(xpos + 2*multiplier*step, ypos + 2*multiplier*step)
            context.line_to(xpos + 2*multiplier*step, ypos + 8*multiplier*step)
            context.move_to(xpos + 3*multiplier*step, ypos + 2*multiplier*step)
            context.line_to(xpos + 3*multiplier*step, ypos + 8*multiplier*step)
            xpos += 6*multiplier*step
        context.stroke()
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


def blackletter(surface, context, step, field):
    '''This function realizes the grid for the blackletter'''
    xpos = 0
    ypos = 0
    # Define multiplier for this grid:
    multiplier = math.cos(math.radians(30))

    context.set_line_width(0.5)
    context.set_line_cap(cairo.LINE_CAP_SQUARE)
    context.set_line_join(cairo.LINE_JOIN_MITER)

    # Aux vertical lines:
    context.set_source_rgba(*aux_line)
    while xpos < field[0]:
        context.move_to(xpos, 0)
        context.line_to(xpos, field[1])
        xpos += multiplier*step
    context.stroke()

    while ypos < field[1]:
        # Aux horizontal lines:
        context.set_source_rgba(*aux_line)
        for arg in [0, 3, 4, 5, 6]:
            context.move_to(0, ypos + arg*multiplier*step)
            context.line_to(field[0], ypos + arg*multiplier*step)
        context.stroke()
        # Main horizontal lines:
        context.set_source_rgba(*main_line)
        context.move_to(0, ypos + 2*multiplier*step)
        context.line_to(field[0], ypos + 2*multiplier*step)
        context.move_to(0, ypos + 7*multiplier*step)
        context.line_to(field[0], ypos + 7*multiplier*step)
        context.stroke()
        ypos += 9*multiplier*step

    return surface, context


def copperplate(surface, context, step, field):
    '''This function realizes the grid for the copperplate'''
    ypos = 0

    context.set_line_width(0.5)
    context.set_line_cap(cairo.LINE_CAP_SQUARE)
    context.set_line_join(cairo.LINE_JOIN_MITER)

    # Find the vertical delta for a 66 degrees line for chosen paper:
    y_delta = field[0]*math.tan(math.radians(66))
    # Find the vertical delta between diagonal lines:
    y_step = 0.5*step*math.tan(math.radians(66))
    # Diagonal lines:
    context.set_source_rgba(*aux_line)
    while ypos < field[1] + y_delta:
        context.move_to(0, ypos)
        context.line_to(field[0], ypos - y_delta)
        ypos += y_step
    context.stroke()
    ypos = 0
    # Horizontal lines:
    while ypos < field[1]:
        context.move_to(0, ypos)
        context.line_to(field[0], ypos)
        ypos += step
    context.stroke()

    return surface, context


def italic(surface, context, step, field):
    '''This function realizes the grid for the italic'''
    xpos = 0
    ypos = 0

    context.set_line_width(0.5)
    context.set_line_cap(cairo.LINE_CAP_SQUARE)
    context.set_line_join(cairo.LINE_JOIN_MITER)

    # Find the vertical delta for a 45 degrees line for chosen paper:
    y_delta = field[0]*math.tan(math.radians(45))
    # Find the vertical delta between 45 degrees diagonal lines:
    y_step = 2.5*step*math.tan(math.radians(45))
    # 45 degrees diagonal lines:
    context.set_source_rgba(*aux_line_2)
    while ypos < field[1] + y_delta:
        context.move_to(0, ypos)
        context.line_to(field[0], ypos - y_delta)
        ypos += y_step
    context.stroke()
    ypos = 0

    # Filled rectangles:
    while ypos < field[1]:
        context.set_source_rgba(*bg_color)
        context.rectangle(0, ypos + 7.5*step, field[0], 5*step)
        context.fill()
        ypos += 15*step
    ypos = 0

    while ypos < field[1]:
        # Main lines:
        context.set_source_rgba(*main_line)
        context.set_dash([])
        context.move_to(0, ypos + 2.5*step)
        context.line_to(field[0], ypos + 2.5*step)
        context.stroke()
        # Dashed lines:
        context.set_source_rgba(*aux_line_2)
        context.set_dash([0.1, step/4])
        context.move_to(0, ypos + 5*step)
        context.line_to(field[0], ypos + 5*step)
        ypos += 5*step
        context.stroke()
    ypos = 0
    context.set_dash([])

    # Find the vertical delta for a 80 degrees line for chosen paper:
    y_delta = field[0]*math.tan(math.radians(80))
    # Find the vertical delta between 80 degrees diagonal lines:
    y_step = 5*step*math.tan(math.radians(80))
    # 80 degrees diagonal lines:
    context.set_source_rgba(*aux_line)
    while ypos < field[1] + y_delta:
        context.move_to(0, ypos)
        context.line_to(field[0], ypos - y_delta)
        ypos += y_step
    context.stroke()
    ypos = 0

    return surface, context

def rustic_ustav_minuscule(surface, context, step, field, multiplier):
    '''This function realizes the grid for the rustic, ustav, half-ustav and minuscule'''
    ypos = 0

    context.set_line_width(0.5)
    context.set_line_cap(cairo.LINE_CAP_SQUARE)
    context.set_line_join(cairo.LINE_JOIN_MITER)

    while ypos < field[1]:
        # Horizontal lines:
        context.set_source_rgba(*main_line)
        context.move_to(0, ypos + 1.5*step)
        context.line_to(field[0], ypos + 1.5*step)
        context.move_to(0, ypos + (multiplier + 1.5)*step)
        context.line_to(field[0], ypos + (multiplier + 1.5)*step)
        ypos += (multiplier + 3)*step
    context.stroke()

    return surface, context