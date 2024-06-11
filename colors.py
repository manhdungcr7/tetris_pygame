class Colors:
    """
    Lớp Colors chứa các màu RGB được sử dụng trong ứng dụng.

    Thuộc tính:
        dark_grey (tuple): Màu xám đậm với giá trị RGB (238, 162, 173).
        green (tuple): Màu xanh lá cây với giá trị RGB (0, 255, 0).
        red (tuple): Màu đỏ với giá trị RGB (255, 0, 0).
        orange (tuple): Màu cam với giá trị RGB (185, 69, 0).
        yellow (tuple): Màu vàng với giá trị RGB (255, 255, 0).
        purple (tuple): Màu tím với giá trị RGB (166, 0, 227).
        cyan (tuple): Màu xanh lơ với giá trị RGB (0, 0, 0).
        blue (tuple): Màu xanh dương với giá trị RGB (0, 0, 255).
        white (tuple): Màu trắng với giá trị RGB (250, 250, 210).
        dark_blue (tuple): Màu xanh đậm với giá trị RGB (255, 52, 179).
        light_blue (tuple): Màu xanh nhạt với giá trị RGB (50, 0, 100).
        menu (tuple): Màu xanh menu với giá trị RGB (36, 73, 200).

    Phương thức:
        get_cell_colors:
            Trả về danh sách các màu dùng để thể hiện các ô trong ứng dụng.

            Returns:
                list: Danh sách các tuple màu RGB.
                    Bao gồm các màu: cyan, green, red, dark_grey, menu, orange, yellow, purple, blue.
    """

    dark_grey = (238, 162, 173)
    green = (0, 255, 0)
    red = (255, 0, 0)
    orange = (185, 69, 0)
    yellow = (255, 255, 0)
    purple = (166, 0, 227)
    cyan = (0, 0, 0)
    blue = (0, 0, 255)
    white = (250, 250, 210)
    dark_blue = (255, 52, 179)
    light_blue = (50, 0, 100)
    menu = (36, 73, 200)

    @classmethod
    def get_cell_colors(cls):
        """
        Trả về danh sách các màu dùng để thể hiện các ô trong ứng dụng.

        Returns:
            list: Danh sách các tuple màu RGB.
                Bao gồm các màu: cyan, green, red, dark_grey, menu, orange, yellow, purple, blue.
        """
        return [cls.cyan, cls.green, cls.red, cls.dark_grey, cls.menu, cls.orange, cls.yellow, cls.purple, cls.blue]


help(Colors)