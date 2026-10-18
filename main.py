import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame


from constants import Window
from player import Player


FPS = 30

pygame.init()
pygame.display.set_caption('Chess')

clock = pygame.time.Clock()
screen = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT))
board = pygame.image.load('assets/boards/maple.jpg')

players = {
        'w' : Player('w'),
        'b' : Player('b')
        }


# Set piece images
for player in players.values():
    for filename, piece in zip(player.get_piece_img_filenames(), player.get_piece_objects()):
        piece.set_img(pygame.image.load(os.path.join('assets', 'piece_sets', 'cburnett', filename)))


# Game loop
wait_for_promotion = False
move_count = 0
running = True
while running:
    clock.tick(FPS)
    screen.blit(board, (0, 0))

    color_to_move, opponent_color = ('b', 'w') if move_count%2 else ('w', 'b')

    for idx, piece in enumerate(players[color_to_move].get_piece_objects()):
        if piece.find_legal_moves(players['w'], players['b'], color_to_move):
            break

    # No break
    else:
        king = players[color_to_move].get_piece_objects()[0]
        if king.check_for_checks(ally=players[color_to_move], opponent=players[opponent_color], position=king.get_position(), color_to_move=color_to_move):
            print(f'Checkmate, {opponent_color} wins!')
            running = False
        else:
            print('Stalemate. Draw.')
            running = False

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            break

        if wait_for_promotion:
            if not event.type == pygame.KEYDOWN:
                continue

            # 1 = queen, 2 = rook, 3 = knite, 4 = bishop
            promotion_options = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]
            if event.key not in promotion_options:
                continue
            new_piece = players[color_to_move].promote(promotion_options.index(event.key)+1)
            new_piece.set_img(pygame.image.load(os.path.join('assets', 'piece_sets', 'cburnett', new_piece.get_img_filename())))
            wait_for_promotion = False
            move_count += 1
            break


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            square_position = int(mouse_x//(Window.WIDTH/8)), int(mouse_y//(Window.HEIGHT/8))
            players[color_to_move].set_en_passant_capturable(players[opponent_color].get_en_passant_capturable())

            if not players[color_to_move].check_for_piece_selection(square_position):
                if players[color_to_move].move_selected_piece(players[opponent_color], square_position):
                    if players[color_to_move].is_to_promote():
                        wait_for_promotion = True
                        print('To promote press: 1 (Queen), 2 (Rook), 3 (Knite), 4 (Bishop)')
                        continue
                    move_count += 1


    # Draw pieces
    for player in players.values():
        for piece in player.get_piece_objects():
            position = piece.get_position()
            position = (position[0]*Window.WIDTH/8, position[1]*Window.HEIGHT/8)
            screen.blit(piece.get_img(), position)

    # Draw legal moves of selected piece
    selected_piece = players[color_to_move].get_selected_piece()
    if selected_piece is not None:
        for move in selected_piece.find_legal_moves(players['b'], players['w'], color_to_move):
            pygame.draw.circle(screen, (0, 255, 0), ((.5+move[0])*Window.WIDTH/8, (.5+move[1])*Window.HEIGHT/8), 10)

    pygame.display.flip()


pygame.quit()

