import pygame
from colors import Colors

class Grid:
    def __init__(self):
        """
        Khởi tạo đối tượng Grid với số hàng, số cột và kích thước ô cố định.
        Tạo ra lưới ban đầu với các ô trống và lấy các màu sắc từ lớp Colors.
        """
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        """
        In ra lưới dưới dạng ma trận các số nguyên.
        """
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()

    def is_inside(self, row, column):
        """
        Kiểm tra xem ô (row, column) có nằm trong lưới hay không.

        Args:
            row (int): Chỉ số hàng.
            column (int): Chỉ số cột.

        Returns:
            bool: True nếu ô nằm trong lưới, ngược lại False.
        """
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False

    def is_empty(self, row, column):
        """
        Kiểm tra xem ô (row, column) có trống hay không.

        Args:
            row (int): Chỉ số hàng.
            column (int): Chỉ số cột.

        Returns:
            bool: True nếu ô trống, ngược lại False.
        """
        if self.grid[row][column] == 0:
            return True
        return False

    def is_row_full(self, row):
        """
        Kiểm tra xem hàng có đầy đủ các ô không (không có ô trống).

        Args:
            row (int): Chỉ số hàng.

        Returns:
            bool: True nếu hàng đầy đủ, ngược lại False.
        """
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    def clear_row(self, row):
        """
        Xóa tất cả các ô trong hàng (đặt tất cả các ô về giá trị 0).

        Args:
            row (int): Chỉ số hàng.
        """
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def clear_full_rows(self):
        """
        Xóa tất cả các hàng đầy đủ và di chuyển các hàng phía trên xuống.

        Returns:
            int: Số lượng hàng đã được xóa.
        """
        completed = 0
        for row in range(self.num_rows-1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    def move_row_down(self, row, num_rows):
        """
        Di chuyển hàng xuống vị trí mới sau khi các hàng bên dưới đã bị xóa.

        Args:
            row (int): Chỉ số hàng.
            num_rows (int): Số lượng hàng cần di chuyển xuống.
        """
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def reset(self):
        """
        Đặt lại lưới, tất cả các ô đều trở về giá trị 0.
        """
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def draw(self, screen):
        """
        Vẽ lưới lên màn hình.

        Args:
            screen (pygame.Surface): Bề mặt để vẽ lưới lên.
        """
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column * self.cell_size + 11, row * self.cell_size + 11, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

help(Grid)
