import pygame
import sys
from picker import Picker
from card import Card, Text
from button import Reroll, Stats, Draft
from exporter import Exporter


class Points(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.num = 1
        self.text = f"Points: {self.num}"
        self.font = pygame.font.Font(None, 40)
        self.image = self.font.render(self.text, True, 'white')
        self.rect = self.image.get_rect(topleft = pos)

    def draw(self, surface):
        self.text = f"Points: {self.num}"
        self.image = self.font.render(self.text, True, 'white')
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        surface.blit(self.image, self.rect.topleft)

    def validate(self, number):
        if self.num < number:
            return False
        elif self.num >= number:
            return True

    def spend(self, number):
        self.num = self.num - number


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Ethans Birthday Game')
        self.clock = pygame.time.Clock()

        self.state = 'commander_choice'
        self.previous_state = ''
        self.can_choose = False

        self.picker = Picker('commander-oracle-cards.json')
        self.commander = None

        self.choice = None
        self.deck = []
        self.deck_size = 10
        self.max_lands = 8
        self.deck_count = 0

        self.stats = None

        self.points = Points((0,0))
        self.points.rect.topright = (1280, 0)

        self.card_group = pygame.sprite.Group()
        self.menu_buttons = pygame.sprite.Group()
        self.choices = pygame.sprite.Group()
        self.all_buttons = pygame.sprite.Group()

        self.reroll_button = Reroll((0,0), self.menu_buttons)
        self.stats_button = Stats((0,0), self.menu_buttons)
        self.draft_button = Draft((0,0), self.all_buttons)

    def display_oracle(self):
        for card in self.card_group:
            if card.is_hovering() and hasattr(card, 'oracle'):
                card.oracle.draw_text(pygame.mouse.get_pos(), self.display_surface)

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
            self.menu_buttons.update(self.choices, self.commander)
            self.menu_buttons.draw(self.display_surface)
            self.points.draw(self.display_surface)

            pygame.display.update()

    def choose_card(self):
        self.can_choose = False

        for card in self.choices:
            if card.is_clicked():
                print(f"{card.name} was chosen")
                self.choice = card
                self.choice.rect.bottomright = (0,0)

    def reroll(self):
        self.can_choose = False
        cost = 1

        if self.reroll_button.is_clicked() and self.points.num >= cost:
            print("REROLL")
            self.points.spend(cost)
            self.cleanup()

    def stats_pressed(self):
        self.can_choose = False
        
        if self.stats_button.is_clicked():
            self.state = 'stats_page'

    def draft_pressed(self):
        if self.draft_button.is_clicked():
            return True

    def choice_sanity(self):
        if not pygame.mouse.get_pressed()[0]:
            self.can_choose = True

    def state_sanity(self):
        self.deck_count = len(self.deck)

        if self.deck_count == 0:
            self.state = 'commander_choice'
        elif self.deck_count >= self.deck_size - self.max_lands and self.points.num > 0 and not self.deck_count >= self.deck_size:
            self.previous_state = self.state
            self.state = 'land_choice'
        elif self.deck_count < self.deck_size - self.max_lands:
            self.previous_state = self.state
            self.state = 'nonland_choice'
        elif self.deck_count >= self.deck_size or self.points.num <= 0:
            self.previous_state = self.state
            self.state = 'export_deck'

    def cleanup(self):
        for card in self.choices:
            if hasattr(self.choice, 'name') and not card.name == self.choice.name:
                card.kill()
            elif not hasattr(self.choice, 'name'):
                card.kill()

        self.choice = None
        self.choices.empty()

    def commander_choice(self):
        if not self.choices:
            choices = self.picker.get_commander_choices(6)
            self.create_choices(choices)

        self.choices.draw(self.display_surface)
        self.menu_buttons.draw(self.display_surface)
        self.points.draw(self.display_surface)

        self.choose_card()
        self.reroll()

        if self.choice:
            self.commander = self.choice
            self.picker.color_identity = self.commander.dict['color_identity']
            self.commander.rect.topright = (1280, 0)
            
            self.points.rect.topright = self.commander.rect.topleft
            self.points.num = 9

            self.deck.append(self.choice)

            self.previous_state = 'commander_choice'
            self.state = 'nonland_choice'
            self.cleanup()

    def nonland_choices(self):
        if not self.choices:
            self.display_surface.blit(self.commander.image, self.commander.rect.topleft)
            choices = self.picker.get_nonlands()
            self.create_choices(choices)

        self.points.rect.topright = self.commander.rect.topleft

        self.choices.draw(self.display_surface)
        self.display_surface.blit(self.commander.image, self.commander.rect.topleft)
        self.menu_buttons.draw(self.display_surface)
        self.points.draw(self.display_surface)

        if self.can_choose:
            self.choose_card()
            self.reroll()
            self.stats_pressed()

        if self.choice:
            self.deck.append(self.choice)

            self.cleanup()

    def land_choices(self):
        self.picker.set_rarities(['u','r','m'])
        if not self.choices:
            self.display_surface.blit(self.commander.image, self.commander.rect.topleft)
            choices = self.picker.get_lands()
            self.create_choices(choices)

        self.points.rect.topright = self.commander.rect.topleft

        self.choices.draw(self.display_surface)
        self.display_surface.blit(self.commander.image, self.commander.rect.topleft)
        self.menu_buttons.draw(self.display_surface)
        self.points.draw(self.display_surface)

        if self.can_choose and self.points.validate(2):
            self.choose_card()
            self.reroll()
            self.stats_pressed()

        if self.choice and self.points.validate(2):
            self.deck.append(self.choice)
            self.points.spend(2)

            self.cleanup()
        elif not self.points.validate(2):
            self.points.num = 0

    def stats_page(self):
        if not self.stats:
            types = []
            type_dict = {}
            types_text = f"Total Deck Count: {self.deck_count}\n"

            for card in self.deck:
                type_line = card.dict['type_line'].split(' — ')[0]

                if 'card_faces' in card.dict:
                    temp = type_line.split(' // ')
                    type_line = ' '.join(temp)

                type_list = type_line.split(' ')

                for card_type in type_list:
                    types.append(card_type)

            for typ in types:
                if typ not in type_dict:
                    type_dict[typ] = 1
                else:
                    type_dict[typ] += 1

            for key, value in type_dict.items():
                types_text += f"{key}: {value}\n"


            self.stats = Text(types_text, 40)
            self.stats.generate_surfs()

            for card in self.choices:
                card.rect.bottomright = (0,0)

        self.draft_button.update(self.choices, self.commander)

        self.stats.draw_text((0,0), self.display_surface)
        self.display_surface.blit(self.commander.image, self.commander.rect.topleft)
        self.display_surface.blit(self.draft_button.image, self.draft_button.rect.topleft)
        
        if self.draft_pressed() and self.can_choose:
            self.state = self.previous_state
            self.stats = None

            prev_card = None
            anchor_pos = None
            for index, card in enumerate(self.choices):
            
                if index == 0:
                    card.rect.topleft = (0,0)
                    anchor_pos = card.rect.bottomleft
                    prev_card = card
                elif index == 3:
                    card.rect.topleft = anchor_pos
                    prev_card = card
                else:
                    card.rect.topleft = prev_card.rect.topright
                    prev_card = card

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

            elif self.state == 'nonland_choice':
                self.nonland_choices()

            elif self.state == 'land_choice':
                self.land_choices()

            elif self.state == 'stats_page':
                self.stats_page()

            elif self.state == 'export_deck':
                self.exporter = Exporter(self.deck)
                self.exporter.basics_fill(self.deck_size)
                self.exporter.export()

            self.choice_sanity()
            if self.state != 'stats_page':
                self.state_sanity()

            self.display_oracle()

            self.card_group.update()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
