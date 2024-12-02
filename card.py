import pygame
from io import BytesIO
import requests
from PIL import Image

class Card(pygame.sprite.Sprite):
    def __init__(self, pos, url):
        super().__init__()
        self.rsp = requests.get(url)
        self.pilimage = Image.open(BytesIO(self.rsp.content)).convert("RGBA")
        self.image = pygame.image.fromstring(self.pilimage.tobytes(), self.pilimage.size, self.pilimage.mode)
        self.image = pygame.transform.scale_by(self.image, 0.33)
        self.rect = self.image.get_rect(topleft = pos)
