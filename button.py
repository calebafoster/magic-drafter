import pygame

class Reroll(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        self.image = pygame.image.load('reroll.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.33)
        self.rect = self.image.get_rect(topleft = pos)
        
        self.clicked = False

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action

    def placement(self, choices):
        if not choices:
            self.rect.topleft = (0,0)

        else:
            for card in choices:
                if card.rect.right > self.rect.left:
                    self.rect.topleft = card.rect.topright

    def update(self, choices, commander):
        self.placement(choices)


class Stats(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.image = pygame.image.load('stats.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 7.50)
        self.rect = self.image.get_rect(topleft = pos)

        self.clicked = False

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action

    def placement(self, commander):
        if not commander:
            self.rect.topright = (0,0)

        else:
            self.rect.topleft = commander.rect.bottomleft

    def update(self, choices, commander):
        self.placement(commander)


class Draft(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.image = pygame.image.load('draft.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 7.50)
        self.rect = self.image.get_rect(topleft = pos)

        self.clicked = False

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action

    def placement(self, commander):
        if not commander:
            self.rect.topright = (0,0)

        else:
            self.rect.topleft = commander.rect.bottomleft

    def update(self, choices, commander):
        self.placement(commander)
