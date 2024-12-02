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

        self.picker = Picker('commander-oracle-cards.json')

        self.choice = None
        self.deck = []
        self.deck_count = 0
        self.color_identity = ['W','U','B','R','G']

    def present_choices(self, choices):
        prev_x = 0
        prev_y = 0
        sprite_group = []

        for index, card in enumerate(choices):
            print(f"{index + 1}. {card['name']}")
            image = None

            if 'card_faces' in card and 'image_uris' not in card:
                image = card['card_faces'][0]['image_uris']['png']
            else:
                image = card['image_uris']['png']

            if index <= 2:
                card_img = Card((prev_x,0), image)
                prev_x = card_img.rect.right
                prev_y = card_img.rect.bottom
                sprite_group.append(card_img)
            if index == 2:
                prev_x = 0

            if index > 2:
                card_img = Card((prev_x,prev_y), image)
                prev_x = card_img.rect.right
                sprite_group.append(card_img)

            self.display_surface.blit(card_img.image, card_img.rect.topleft)


        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_1:
                        self.choice = choices[0]
                        run = False
                    if event.key == pygame.K_2:
                        self.choice = choices[1]
                        run = False
                    if event.key == pygame.K_3:
                        self.choice = choices[2]
                        run = False
                    if event.key == pygame.K_4:
                        self.choice = choices[3]
                        run = False
                    if event.key == pygame.K_5:
                        self.choice = choices[4]
                        run = False
                    if event.key == pygame.K_6:
                        self.choice = choices[5]
                        run = False

            pygame.display.update()

    def run(self):
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surface.fill('black')

            self.deck_count = len(self.deck)

            if self.state == 'commander_choice':
                self.present_choices(self.picker.get_commander_choices(6))
                self.deck.append(self.choice)
                self.color_identity = self.choice['color_identity']
                print(self.color_identity)
                print(self.deck)
                self.state = 'nonland_choice'

            elif self.state == 'nonland_choice' and self.deck_count < 62:
                self.present_choices(self.picker.get_nonlands(self.color_identity))
                self.deck.append(self.choice)
                print(self.deck[-1]['name'] + f' was the {self.deck_count + 1}th card added to the deck')

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
