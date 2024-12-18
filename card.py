import pygame
from io import BytesIO
import requests
from PIL import Image

class Text(pygame.sprite.Sprite):
    def __init__(self, text):
        super().__init__()

        self.text = text
        self.font = pygame.font.Font(None, 20)
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

    def is_hovering(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            return True

    def update(self):
        pass
