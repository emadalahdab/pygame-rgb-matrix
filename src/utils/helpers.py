import feedparser
import logging
import numpy as np
import pygame
import random
from pandas.io.json import json_normalize
from PIL import Image
from config import LED_ROWS, LED_COLS, LED_CHAIN, LED_PARALLEL, PANEL_ROWS, PANEL_COLS


def setup_logger(debug=False):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)


# PyGame renders wall like this:
#
# | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
#
# We need to render to the LED panels (if using
# parallel chains and panels are arranged on a single row):
#
# | 0 | 1 | 2 | 3 |
# | 4 | 5 | 6 | 7 |
#


def render_led_matrix(screen, matrix=None):
    if not matrix:
        return
    led_surface = pygame.Surface((LED_COLS * LED_CHAIN, LED_ROWS * LED_PARALLEL))
    # Blit first 4 panels to top row
    led_surface.blit(
        screen,
        (0, 0),
        (0, 0, LED_COLS * LED_CHAIN, LED_ROWS * 1),
    )
    # Blit next 4 panels to next row
    led_surface.blit(
        screen,
        (0, 64),
        (LED_COLS * LED_CHAIN, 0, (LED_COLS * LED_CHAIN), 64),
    )
    led_array = np.flip(np.rot90(pygame.surfarray.array3d(led_surface), 1), 0)
    image_rgb = Image.fromarray(led_array, mode="RGB")
    matrix.SetImage(image_rgb)


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_rss_items(url):
    return feedparser.parse(url)
    flattened = json_normalize(feed.entries)
    return flattened


class JoyPad:
    def __init__(self, device_index):
        pygame.joystick.init()
        self.joypad = pygame.joystick.Joystick(device_index)
        self.joypad.init()
        self.button = None
        self.direction = (0, 0)

    def process_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            self.button = event.dict["button"]
        if event.type == pygame.JOYHATMOTION:
            self.direction = event.dict["value"]
