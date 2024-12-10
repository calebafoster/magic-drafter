import pygame
from io import BytesIO
import requests
from PIL import Image

class Card(pygame.sprite.Sprite):
    def __init__(self, pos, card_dict, groups):
        super().__init__(groups)

        self.dict = card_dict
        self.name = card_dict['name']
        self.url = self.get_url(card_dict)

        self.rsp = requests.get(self.url)
        self.pilimage = Image.open(BytesIO(self.rsp.content)).convert("RGBA")
        self.image = pygame.image.fromstring(self.pilimage.tobytes(), self.pilimage.size, self.pilimage.mode)
        self.image = pygame.transform.scale_by(self.image, 0.33)

        self.rect = self.image.get_rect(topleft = pos)
        self.clicked = False

    def get_url(self, card_dict):
        url = None

        if 'card_faces' in card_dict and 'image_uris' not in card_dict:
            url = card_dict['card_faces'][0]['image_uris']['png']
        else:
            url = card_dict['image_uris']['png']

        return url

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action
