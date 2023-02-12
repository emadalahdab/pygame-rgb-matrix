import aiohttp
import async_timeout
import feedparser
import logging
import pygame
import random

from wideboy.config import DEBUG, FT_SIZE

logger = logging.getLogger(__name__)


def intro_debug(description, version):
    logger.info(f"{description} v{version}")
    logger.info(f"Debug: {DEBUG}")
    logger.info(f"FT Panel Size: {FT_SIZE[0]}x{FT_SIZE[1]}")


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


async def async_fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def get_rss_items(loop, url):
    feed = None
    async with aiohttp.ClientSession(loop=loop) as session:
        html = await async_fetch(session, url)
        feed = feedparser.parse(html)
    return feed


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
