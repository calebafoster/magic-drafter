import pygame
from io import BytesIO
import requests
from PIL import Image

class Text(pygame.sprite.Sprite):
    def __init__(self, text, size = 20):
        super().__init__()

        self.text = text
        self.font = pygame.font.Font(None, size)
        self.generate_surfs()

    def generate_surfs(self):
        self.surf_list = []
        self.rect_list = []

        self.text = self.text.replace(".)", ")")

        self.text = self.text.replace(".", "\n")
        lines = self.text.splitlines()

        for line in lines:
            img = self.font.render(line, True, 'white')
            rect = img.get_rect(topleft = (0,0))
            self.surf_list.append(img)
            self.rect_list.append(rect)

    def draw_text(self, pos, display_surface):
        next_pos = None

        for index, surf in enumerate(self.surf_list):
            if index == 0 and pos[0] < 640:
                self.rect_list[index].topleft = pos
                next_pos = self.rect_list[index].bottomleft
            elif index == 0 and pos[0] >= 640:
                self.rect_list[index].topright = pos
                next_pos = self.rect_list[index].bottomright
            elif pos[0] >= 640:
                self.rect_list[index].topright = next_pos
                next_pos = self.rect_list[index].bottomright
            else:
                self.rect_list[index].topleft = next_pos
                next_pos = self.rect_list[index].bottomleft
                
            bg = pygame.Surface(self.rect_list[index].size)
            bg.set_alpha(120)
            bg.fill('black')

            display_surface.blit(bg, self.rect_list[index].topleft)
            display_surface.blit(surf, self.rect_list[index].topleft)


class Card(pygame.sprite.Sprite):
    def __init__(self, pos, card_dict, groups):
        super().__init__(groups)

        self.state = 0

        self.dict = card_dict
        self.name = card_dict['name']
        if "oracle_text" in card_dict:
            self.oracle = Text(card_dict["oracle_text"])
        else:
            self.oracle = Text(card_dict["name"])
        self.url = self.get_url(card_dict)

        self.rsp = requests.get(self.url)
        self.pilimage = Image.open(BytesIO(self.rsp.content)).convert("RGBA")
        self.image = pygame.image.fromstring(self.pilimage.tobytes(), self.pilimage.size, self.pilimage.mode)
        self.image = pygame.transform.scale_by(self.image, 0.33)
        self.images = [self.image]
        if 'card_faces' in card_dict and 'image_uris' not in card_dict:
            self.url = card_dict['card_faces'][1]['image_uris']['png']
            self.rsp = requests.get(self.url)
            self.pilimage = Image.open(BytesIO(self.rsp.content)).convert("RGBA")
            image = pygame.image.fromstring(self.pilimage.tobytes(), self.pilimage.size, self.pilimage.mode)
            image = pygame.transform.scale_by(image, 0.33)
            self.images.append(image)

        self.rect = self.image.get_rect(topleft = pos)
        self.clicked = False
        self.right_clicked = False

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

    def is_right_clicked(self):
        pos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[2] and not self.right_clicked:
                self.right_clicked = True
                action = True

        if not pygame.mouse.get_pressed()[2]:
            self.right_clicked = False

        return action

    def is_hovering(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            return True

    def state_check(self):
        if self.is_right_clicked():
            if self.state == 0:
                self.state = 1
            else:
                self.state = 0

        self.image = self.images[self.state]

    def update(self):
        if len(self.images) > 1:
            self.state_check()
