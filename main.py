import pygame
import sys
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font("Bond Story.ttf", 35)
score_surface = title_font.render("Score", True, Colors.green)
highscore_surface = title_font.render("Highscore", True, Colors.green)
next_surface = title_font.render("Next", True, Colors.green)

score_rect = pygame.Rect(320, 60, 170, 60)
highscore_rect = pygame.Rect(320, 170, 170, 60)
next_rect = pygame.Rect(320, 290, 170, 180)


image_over = pygame.image.load("gameover1.jpg")
new_width = 630
new_height = 620
scaled_image_over = pygame.transform.scale(image_over, (new_width, new_height))
image_tetris = pygame.image.load("tetris1.png")
new_width = 500
new_height = 640
scaled_image = pygame.transform.scale(image_tetris, (new_width, new_height))


image_pause = pygame.image.load("pause.png")
new_width = 60
new_height = 60
image_pause = pygame.transform.scale(image_pause, (new_width, new_height))


screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
game_speed = 250
pygame.time.set_timer(GAME_UPDATE, game_speed)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.save_state()
            game.save_highscore()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not game.running:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            else:
                if game.game_over:
                    if event.key == pygame.K_RETURN:
                        game.reset()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_LEFT:
                        game.move_left()
                    if event.key == pygame.K_RIGHT:
                        game.move_right()
                    if event.key == pygame.K_DOWN:
                        game.move_down()
                        game.update_score(0, 1)
                    if event.key == pygame.K_UP:
                        game.rotate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.paused:
                game.handle_pause_event(event)
            else:
                if game.pause_rect.collidepoint(event.pos):
                    game.handle_pause()
                elif not game.running:
                    if game.showing_tutorial:
                        if game.back_rect.collidepoint(event.pos):
                            game.showing_tutorial = False
                    else:
                        if game.continue_rect.collidepoint(event.pos):
                            game.load_state()
                            game.running = True
                        elif game.start_rect.collidepoint(event.pos):
                            game.reset()
                            game.running = True
                        elif game.tutorial_rect.collidepoint(event.pos):
                            game.showing_tutorial = True
                        elif game.exit_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                elif game.game_over:
                    if game.retry_rect.collidepoint(event.pos):
                        game_speed = 250
                        pygame.time.set_timer(GAME_UPDATE, game_speed)
                        game.reset()
                    elif game.exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        if game.running and not game.game_over and not game.paused:
            if event.type == GAME_UPDATE:
                game.move_down()

    # Drawing
    if game.paused:
        screen.fill(Colors.dark_blue)
        game.draw_pause_menu(screen)
    else:
        score_value_surface = title_font.render(str(game.score), True, Colors.white)
        highscore_value_surface = title_font.render(str(game.highscore), True, Colors.white)

        if game.running:
            if game.game_over:
                screen.blit(scaled_image_over, (-80, 0))
                game.draw_game_over_menu(screen)
            else:
                screen.fill(Colors.dark_blue)
                screen.blit(score_surface, (365, 22))
                screen.blit(highscore_surface, (335, 132))
                screen.blit(next_surface, (375, 252))

                pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
                screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
                pygame.draw.rect(screen, Colors.light_blue, highscore_rect, 0, 10)
                screen.blit(highscore_value_surface, highscore_value_surface.get_rect(centerx=highscore_rect.centerx, centery=highscore_rect.centery))
                pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
                game.draw(screen, image_pause)

                # Check if score has reached 1000 and double the speed
                if game.score >= 300 and game_speed == 250:
                    game_speed = 150
                    pygame.time.set_timer(GAME_UPDATE, game_speed)
        else:
            screen.blit(scaled_image, (0, -20))

            if game.showing_tutorial:
                game.draw_tutorial(screen)
            else:
                game.draw_menu(screen)

    pygame.display.update()
    clock.tick(60)
