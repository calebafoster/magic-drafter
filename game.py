import pygame
import sys
from picker import Picker
from card import Card


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Ethans Birthday Game')
        self.clock = pygame.time.Clock()

        self.state = 'commander_choice'
        self.can_choose = False

        self.picker = Picker('commander-oracle-cards.json')
        self.commander = None

        self.choice = None
        self.deck = []
        self.deck_count = 0
        self.color_identity = ['W','U','B','R','G']

        self.card_group = pygame.sprite.Group()
        self.choices = pygame.sprite.Group()

    def create_choices(self, choices):
        sprite_group = []
        prev_card = None

        for index, card in enumerate(choices):
            sprite_group.append(Card((0, 0), card, self.card_group))
            print(f"{index + 1}. {card['name']}")

            if index == 0:
                prev_card = sprite_group[index]
            elif index == 3:
                sprite_group[index].rect.topleft = sprite_group[0].rect.bottomleft
                prev_card = sprite_group[index]
            else:
                sprite_group[index].rect.topleft = prev_card.rect.topright
                prev_card = sprite_group[index]

            self.choices.add(sprite_group[index])
            self.choices.draw(self.display_surface)

            pygame.display.update()

    def choose_card(self):
        self.can_choose = False

        for card in self.choices:
            if card.is_clicked():
                print(f"{card.name} was chosen")
                self.choice = card

    def choice_sanity(self):
        if not pygame.mouse.get_pressed()[0]:
            self.can_choose = True

    def cleanup(self):
        for card in self.choices:
            if not card.name == self.choice.name:
                card.kill()

        self.choice = None
        self.choices.empty()

    def commander_choice(self):
        if not self.choices:
            choices = self.picker.get_commander_choices(6)
            self.create_choices(choices)

        self.choices.draw(self.display_surface)

        self.choose_card()

        if self.choice:
            self.commander = self.choice
            self.color_identity = self.commander.dict['color_identity']
            self.commander.rect.topright = (1280, 0)

            self.deck.append(self.choice)

            self.state = 'nonland_choice'
            self.cleanup()

    def nonland_choices(self):
        if not self.choices:
            self.display_surface.blit(self.commander.image, self.commander.rect.topleft)
            choices = self.picker.get_nonlands(self.color_identity)
            self.create_choices(choices)

        self.choices.draw(self.display_surface)
        self.display_surface.blit(self.commander.image, self.commander.rect.topleft)

        if self.can_choose:
            self.choose_card()

        if self.choice:
            self.deck.append(self.choice)

            self.cleanup()

    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surface.fill('black')

            self.deck_count = len(self.deck)

            if self.state == 'commander_choice':
                self.commander_choice()

            elif self.state == 'nonland_choice' and self.deck_count < 60 - 24:
                self.nonland_choices()

            self.choice_sanity()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
