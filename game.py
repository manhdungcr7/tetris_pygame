import pygame
import sys
from grid import Grid
from blocks import *
import random
from colors import Colors
import json

class Game:
    def __init__(self):
        """
        Khởi tạo đối tượng Game.
        """
        self.running = False
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), SBlock(), TBlock(), ZBlock(), OBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.highscore = self.load_highscore()
        self.rotate_sound = pygame.mixer.Sound("rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("clear.ogg")

        pygame.mixer.music.load("music.ogg")
        pygame.mixer.music.play(-1)

        self.image_menu = pygame.image.load("menu.png")
        new_width = 240
        new_height = 100
        self.image_menu = pygame.transform.scale(self.image_menu, (new_width, new_height))



        self.menu_font = pygame.font.Font("Bond Story.ttf", 25)
        self.start_surface = self.menu_font.render("Start", True, Colors.yellow)
        self.continue_surface = self.menu_font.render("Continue", True, Colors.yellow)
        self.exit_surface = self.menu_font.render("Exit", True, Colors.yellow)
        self.retry_surface = self.menu_font.render("Retry", True, Colors.yellow)

        self.start_rect = self.image_menu.get_rect()
        self.start_rect.topleft=(10,460)
        self.continue_rect = self.image_menu.get_rect()
        self.continue_rect.topleft = (255, 460)
        self.exit_rect = self.image_menu.get_rect()
        self.exit_rect.topleft = (255, 530)
        self.retry_rect = self.image_menu.get_rect()
        self.retry_rect.topleft = (10, 530)

        self.tutorial_surface = self.menu_font.render("Tutorial", True, Colors.yellow)
        self.tutorial_rect = self.image_menu.get_rect()
        self.tutorial_rect.topleft = (10, 530)

        self.showing_tutorial = False

        self.pause_rect = pygame.Rect(420, 530, 60, 60)

        self.continuep_surface = self.menu_font.render("Continue", True, Colors.white)
        self.restart_surface = self.menu_font.render("Restart", True, Colors.white)
        self.exitp_surface = self.menu_font.render("Exit", True, Colors.white)

        self.continuep_rect = self.image_menu.get_rect()
        self.continuep_rect.center = (250, 200)
        self.exitp_rect = self.image_menu.get_rect()
        self.exitp_rect.center = (250, 400)
        self.restart_rect = self.image_menu.get_rect()
        self.restart_rect.center = (250, 300)


        self.back_surface = self.menu_font.render("Back", True, Colors.yellow)
        self.back_rect = self.image_menu.get_rect()
        self.back_rect.topleft = (10, 530)

        self.paused = False

    def update_score(self, lines_cleared, move_down_points):
        """
        Cập nhật điểm số dựa trên số hàng đã xóa và điểm di chuyển xuống.

        Args:
            lines_cleared (int): Số hàng đã xóa.
            move_down_points (int): Điểm số khi di chuyển xuống.
        """
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points
        if self.score > self.highscore:
            self.highscore = self.score

    def save_highscore(self):
        """
        Lưu highscore vào tệp.
        """
        with open('highscore.json', 'w') as file:
            json.dump({'highscore': self.highscore}, file)

    def load_highscore(self):
        """
        Tải highscore từ tệp.

        Returns:
            int: Highscore.
        """
        try:
            with open('highscore.json', 'r') as file:
                data = json.load(file)
                return data.get('highscore', 0)
        except FileNotFoundError:
            return 0

    def save_state(self):
        """
        Lưu trạng thái trò chơi hiện tại vào tệp.
        """
        state = {
            'running': self.running,
            'grid': self.grid.grid,
            'current_block': self.current_block.__class__.__name__,
            'next_block': self.next_block.__class__.__name__,
            'game_over': self.game_over,
            'score': self.score,
            'highscore': self.highscore
        }
        with open('savegame.json', 'w') as file:
            json.dump(state, file)

    def load_state(self):
        """
        Tải trạng thái trò chơi từ tệp.
        """
        try:
            with open('savegame.json', 'r') as file:
                state = json.load(file)
                self.running = state['running']
                self.grid.grid = state['grid']
                self.current_block = globals()[state['current_block']]()
                self.next_block = globals()[state['next_block']]()
                self.game_over = state['game_over']
                self.score = state['score']
                self.highscore = state['highscore']
        except FileNotFoundError:
            self.reset()

    def reset(self):
        """
        Đặt lại trò chơi.
        """
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), SBlock(), TBlock(), ZBlock(), OBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.game_over = False
        self.load_highscore()

    def get_random_block(self):
        """
        Lấy một khối ngẫu nhiên từ danh sách các khối.

        Returns:
            Block: Khối ngẫu nhiên.
        """
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), SBlock(), TBlock(), ZBlock(), OBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        """
        Di chuyển khối hiện tại sang trái.
        """
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        """
        Di chuyển khối hiện tại sang phải.
        """
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        """
        Di chuyển khối hiện tại xuống dưới.
        """
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        """
        Khóa khối hiện tại vào lưới và tạo khối mới.
        """

        i = 0
        while not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()
            i += 1
            if i == 4:
                self.current_block.move(-1, 0)
                break
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.game_over = True

    def block_fits(self):
        """
        Kiểm tra xem khối hiện tại có vừa trong lưới không.

        Returns:
            bool: True nếu khối vừa, ngược lại là False.
        """
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        """
        Xoay khối hiện tại.
        """
        self.current_block.rotate()
        i = 0
        while not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()
            i+=1
            if i == 4:
                self.current_block.move(-1, 0)
                return

        self.rotate_sound.play()

    def block_inside(self):
        """
        Kiểm tra xem khối hiện tại có nằm trong lưới không.

        Returns:
            bool: True nếu khối nằm trong lưới, ngược lại là False.
        """
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True


    def draw(self, screen, image_pause):
        """
        Vẽ lưới và khối hiện tại lên màn hình.

        Args:
            screen (pygame.Surface): Bề mặt để vẽ.
        """
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 257, 363)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 256, 354)
        else:
            self.next_block.draw(screen, 270, 350)

        self.draw_pause_button(screen, image_pause)
    def draw_menu(self, screen):
        """
        Vẽ menu lên màn hình.
        """
        screen.blit(self.image_menu, self.continue_rect.topleft)
        screen.blit(self.image_menu, self.start_rect.topleft)
        screen.blit(self.image_menu, self.tutorial_rect.topleft)
        screen.blit(self.image_menu, self.exit_rect.topleft)

        screen.blit(self.continue_surface, self.continue_surface.get_rect(center=self.continue_rect.center))
        screen.blit(self.start_surface, self.start_surface.get_rect(center=self.start_rect.center))
        screen.blit(self.tutorial_surface, self.tutorial_surface.get_rect(center=self.tutorial_rect.center))
        screen.blit(self.exit_surface, self.exit_surface.get_rect(center=self.exit_rect.center))

        pygame.display.update()

    def draw_tutorial(self, screen):
        """
        Vẽ màn hình hướng dẫn chơi.
        """
        screen.fill(Colors.menu)
        tutorial_font = pygame.font.Font(None, 30)
        tutorial_texts = [
            "Use arrow keys to move the blocks:",
            "Left Arrow: Move left",
            "Right Arrow: Move right",
            "Down Arrow: Move down faster",
            "Up Arrow: Rotate the block",
            "",
            "Press Back to go back to the main menu"
        ]

        for i, text in enumerate(tutorial_texts):
            tutorial_surface = tutorial_font.render(text, True, Colors.white)
            screen.blit(tutorial_surface, (50, 100 + i * 40))

        screen.blit(self.image_menu, self.back_rect.topleft)
        screen.blit(self.back_surface, self.back_surface.get_rect(center=self.back_rect.center))

        pygame.display.update()

    def draw_game_over_menu(self, screen):
        """
        Vẽ menu game over lên màn hình.
        """
        screen.blit(self.image_menu, self.exit_rect.topleft)
        screen.blit(self.image_menu, self.retry_rect.topleft)


        screen.blit(self.retry_surface, self.retry_surface.get_rect(center=self.retry_rect.center))
        screen.blit(self.exit_surface, self.exit_surface.get_rect(center=self.exit_rect.center))

        pygame.display.update()

    def draw_pause_button(self, screen, image_pause):
        """
        Vẽ nút tạm dừng lên màn hình.

        Args:
            screen (pygame.Surface): Bề mặt để vẽ.
            image_pause (pygame.Surface): Hình ảnh nút tạm dừng.
        """
        screen.blit(image_pause, (420, 530))

    def draw_pause_menu(self, screen):
        """
        Vẽ menu tạm dừng lên màn hình.

        Args:
            screen (pygame.Surface): Bề mặt để vẽ.
        """
        screen.blit(self.image_menu, self.exitp_rect.topleft)
        screen.blit(self.image_menu, self.continuep_rect.topleft)
        screen.blit(self.image_menu, self.restart_rect.topleft)

        screen.blit(self.continuep_surface, self.continuep_surface.get_rect(center=self.continuep_rect.center))
        screen.blit(self.restart_surface, self.restart_surface.get_rect(center=self.restart_rect.center))
        screen.blit(self.exitp_surface, self.exitp_surface.get_rect(center=self.exitp_rect.center))

    def handle_pause_event(self, event):
        """
        Xử lý sự kiện trong menu tạm dừng.

        Args:
            event (pygame.event.Event): Sự kiện được xử lý.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.continuep_rect.collidepoint(event.pos):
                self.paused = False
            elif self.restart_rect.collidepoint(event.pos):
                GAME_UPDATE = pygame.USEREVENT
                game_speed = 250
                pygame.time.set_timer(GAME_UPDATE, game_speed)
                self.reset()
                self.paused = False
            elif self.exitp_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    def handle_pause(self):
        """
        Xử lý sự kiện khi tạm dừng trò chơi.
        """
        self.paused = not self.paused

