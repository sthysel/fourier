import math

import click
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pixels = []


def draw_points(points):
    win = pygame.display.get_surface()
    for point in points:
        point[0] += 1
        win.set_at(point, WHITE)


def draw_circles(terms: int, radius: int):
    win = pygame.display.get_surface()
    w, h = win.get_size()
    X, Y = w // 2, h // 2
    tick = pygame.time.get_ticks() / 1000
    centres = [(radius + 200, h // 2)]
    freq = 20
    xx, yy = 0, 0
    for k in range(terms):
        n = 2 * k + 1  # change for different functions
        _radius = round(radius * (4 / (n * (math.tau / 2))))
        angle = round(math.tau * freq * tick * n)
        xx = centres[k][0] + math.cos(math.radians(angle)) * _radius
        yy = centres[k][1] + math.sin(math.radians(angle)) * _radius
        pygame.draw.circle(win, WHITE, centres[k], _radius, 1)
        xx = round(xx)
        yy = round(yy)
        pygame.draw.line(win, WHITE, centres[k], (xx, yy), 1)
        centres.insert(k + 1, (xx, yy))

    pygame.draw.line(win, WHITE, (xx, yy), (w // 2, yy), 1)
    Y = yy
    pixels.append([X, Y])


def redraw(font, terms: int, radius: int):
    win = pygame.display.get_surface()
    w, h = win.get_size()
    win.fill(BLACK)
    text = font.render(f"{terms}", 1, WHITE)
    win.blit(text, (w // 2 - text.get_width() // 2, 50))
    draw_circles(terms, radius)
    draw_points(pixels)
    pygame.display.update()


def get_terms(terms):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_j, pygame.K_DOWN):
                terms -= 1
            if event.key in (pygame.K_k, pygame.K_UP):
                terms += 1
            if event.type == pygame.QUIT:
                pygame.quit()

    return terms


@click.command(context_settings=dict(max_content_width=120))
@click.option(
    "-t",
    "--terms",
    default=3,
    help="Number of terms",
    show_default=True,
)
@click.option(
    "-r",
    "--radius",
    default=100,
    help="Radius",
    show_default=True,
)
@click.version_option()
def cli(terms, radius):
    pygame.init()
    font = pygame.font.SysFont("consolas", 30, True)
    window_width, window_height = 1200, 800
    pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Fourier")
    clock = pygame.time.Clock()

    while True:
        clock.tick(120)
        terms = get_terms(terms)
        redraw(font, terms=terms, radius=radius)
