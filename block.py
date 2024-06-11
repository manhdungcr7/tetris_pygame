from colors import Colors
import pygame
from position import Position

class Block:
    def __init__(self, id):
        """
        Khởi tạo đối tượng Block với định danh, kích thước ô, offset hàng và cột,
        trạng thái xoay và các màu sắc từ lớp Colors.

        Args:
            id (int): Định danh của khối.
        """
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    def move(self, rows, columns):
        """
        Di chuyển khối bằng cách cập nhật offset hàng và cột.

        Args:
            rows (int): Số lượng hàng để di chuyển.
            columns (int): Số lượng cột để di chuyển.
        """
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        """
        Lấy danh sách các vị trí của ô sau khi đã áp dụng offset.

        Returns:
            list: Danh sách các đối tượng Position của các ô.
        """
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    def rotate(self):
        """
        Xoay khối, cập nhật trạng thái xoay.
        """
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        """
        Hoàn tác thao tác xoay khối, quay lại trạng thái xoay trước đó.
        """
        self.rotation_state -= 1
        if self.rotation_state == 0:
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen, offset_x, offset_y):
        """
        Vẽ khối lên màn hình.

        Args:
            screen (pygame.Surface): Bề mặt để vẽ khối lên.
            offset_x (int): Offset theo trục x.
            offset_y (int): Offset theo trục y.
        """
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size, offset_y + tile.row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)


help(Block)

