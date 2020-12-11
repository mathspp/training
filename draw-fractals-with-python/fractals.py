import decimal
import math
import pygame as pg
import sys

def iterate(c, maxiter):
    i = 0
    z = 0
    while i <= maxiter and abs(z) < 2:
        z = z**2 + c
        i += 1
    return i

def sigmoid(x):
    exp = math.exp(x)
    return exp / (1 + exp)

def sigmoid_factory(from_, to):
    """Return a sigmoid function with an adjusted range."""
    return lambda x: from_ + sigmoid(x)*(to - from_)

def make_gray_palette(maxiter):
    """Create a palette in maxiter shades of gray."""

    palette = []
    for i in range(maxiter + 1):
        gray = int(255*(1 - i/(1 + maxiter)))
        palette.append(pg.Color(gray, gray, gray))
    palette.append(pg.Color(0, 0, 0))
    return palette

def make_palette(maxiter):
    """Create a palette with maxiter+1 colours dependant on the zoom level."""

    base_color = pg.Color(10, 115, 207)
    h, _, _, _ = base_color.hsva
    palette = []
    colour = pg.Color(0, 0, 0)
    for i in range(maxiter + 1):
        colour.hsva = (
            360 / math.exp(i/maxiter),
            70, 50, 100
        )
        palette.append(
            (colour.r, colour.g, colour.b)
        )
    palette.append(pg.Color(0, 0, 0))
    return palette

def compute_parameters(centre, width, height):
    """Compute a series of parameters from the central point, width and height."""
    left = centre.real - (width/2)
    up = centre.imag + (height/2)
    return left, up

if __name__ == "__main__":
    # Set display informations.
    WIDTH = 640
    HEIGHT = 480
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen_array = pg.PixelArray(screen)
    # Set parameters for fractal window.
    width = 2                           # Width along the real axis inside the image.
    height = width*(HEIGHT/WIDTH)       # Height ...
    centre = complex(-0.5, 0)           # Center of the image.
    left, up = compute_parameters(centre, width, height)
    # Set parameters for the displacement between consecutive computed points.
    dx = math.sqrt(2)                   # Displacement along the real axis.
    dy = (1 + math.sqrt(5))/2           # Displacement along the imaginary axis.
    c = centre                          # Point we will start at.
    # Set zooming parameters.
    zoom_level = 1                      # How many times zoom has been made.
    zoom_multiplier = 2                 # By how much we decrease width/height upon zooming.
    zooms = 0                           # How many times we zoomed in.
    # Set parameters for the calculations.
    maxiter = 50                        # How many iterations per point.
    palette = make_palette(maxiter)     # Create the colour palette.
    points_per_frame = int(WIDTH*HEIGHT/250) # How many points to compute per frame.
    save_frames = False
    frame_number = 1

    pg.init()
    pg.display.set_caption(f"Zoom level: {zoom_level}, centre = {centre}")

    while True:
        for _ in range(points_per_frame):
            c = complex(
                ((c.real + dx - left) % width) + left,
                up - ((up - c.imag - dy) % height)
            )
            i = iterate(c, maxiter)
            colour = palette[i]
            x = int(WIDTH*(c.real - left)/width)
            y = int(HEIGHT*(up - c.imag)/height)
            try:
                screen_array[x, y] = colour
            except Exception as e:
                print(x, y)
                print(left, up)
                raise e

        pg.display.flip()
        if save_frames:
            pg.image.save(screen_array.make_surface(), f"imgbin/frame_{frame_number:05}.png")
            frame_number += 1

        for ev in pg.event.get():
            # Quit pygame.
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit
            # Screenshot or toggle `save_frames`.
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_s:
                    pg.image.save(screen_array.make_surface(), f"imgbin/mandelbrot_{zoom_level}_{pg.time.get_ticks()}.png")
                elif ev.key == pg.K_f:
                    save_frames = not save_frames
            # Zoom in.
            elif ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
                px, py = ev.pos
                real = left + width*px/WIDTH
                imag = up - height*py/HEIGHT
                centre = complex(real, imag)
                width /= zoom_multiplier
                height /= zoom_multiplier
                dx /= zoom_multiplier
                dy /= zoom_multiplier
                zoom_level *= zoom_multiplier
                maxiter *= zoom_multiplier
                palette = make_palette(maxiter)
                left, up = compute_parameters(centre, width, height)
                pg.display.set_caption(f"Zoom level: {zoom_level}, centre = {centre}")
