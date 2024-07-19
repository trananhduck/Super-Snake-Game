import pygame
import random
from config import *


class Snake:
    """
    Lớp đại diện cho con rắn trong trò chơi.

    Attributes:
        size (int): Kích thước của một ô vuông của con rắn.
        body (list): Danh sách tọa độ các phần thân của con rắn.
        direction (str): Hướng di chuyển hiện tại của con rắn.
        width (int): Chiều rộng của cửa sổ trò chơi.
        height (int): Chiều cao của cửa sổ trò chơi.
    """

    def __init__(self, x, y, size, width, height):
        self.size = size
        self.body = [[x, y]]
        self.direction = "RIGHT"
        self.width = width
        self.height = height

    def move(self):
        """
        Di chuyển con rắn theo hướng hiện tại.
        """
        head = self.body[0].copy()
        if self.direction == "UP":
            head[1] -= self.size
        elif self.direction == "DOWN":
            head[1] += self.size
        elif self.direction == "LEFT":
            head[0] -= self.size
        else:
            head[0] += self.size

        # Kiểm tra xem đầu con rắn vượt ra biên hay chưa
        if head[0] < 0:
            head[0] = self.width - self.size
        elif head[0] >= self.width:
            head[0] = 0
        elif head[1] < 0:
            head[1] = self.height - self.size
        elif head[1] >= self.height:
            head[1] = 0

        self.body.insert(0, head)

    def change_direction(self, direction):
        """
        Thay đổi hướng di chuyển của con rắn.

        Args:
            direction (str): Hướng mới ("UP", "DOWN", "LEFT", "RIGHT").
        """
        if direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
            if (direction == "UP" and self.direction != "DOWN") or \
               (direction == "DOWN" and self.direction != "UP") or \
               (direction == "LEFT" and self.direction != "RIGHT") or \
               (direction == "RIGHT" and self.direction != "LEFT"):
                self.direction = direction

    def draw(self, surface):
        """
        Vẽ con rắn lên bề mặt trò chơi.

        Args:
            surface (pygame.Surface): Bề mặt để vẽ con rắn lên.
        """
        for pos in self.body:
            pygame.draw.rect(
                surface, GREEN, (pos[0] + 2, pos[1] + 2, self.size - 2, self.size - 2))


class Food:
    """
    Lớp đại diện cho thức ăn trong trò chơi.

    Attributes:
        size (int): Kích thước của một ô vuông của thức ăn.
        pos (list): Tọa độ của thức ăn.
        color (tuple): Màu sắc của thức ăn.
        timer (int): Bộ đếm thời gian của thức ăn.
    """

    def __init__(self, size):
        self.size = size
        self.pos = [random.randrange(0, WIDTH - self.size, self.size),
                    random.randrange(0, HEIGHT - self.size, self.size)]
        self.color = RED
        self.timer = 0

    def respawn(self):
        """
        Tạo lại vị trí ngẫu nhiên mới cho thức ăn.
        """
        self.pos = [random.randrange(0, WIDTH - self.size, self.size),
                    random.randrange(0, HEIGHT - self.size, self.size)]

    def draw(self, surface):
        """
        Vẽ thức ăn lên bề mặt trò chơi.

        Args:
            surface (pygame.Surface): Bề mặt để vẽ thức ăn lên.
        """
        pygame.draw.rect(surface, self.color,
                         (self.pos[0] + 2, self.pos[1] + 2, self.size - 2, self.size - 2))


class SpecialFood:
    """
    Lớp đại diện cho thức ăn đặc biệt trong trò chơi.

    Attributes:
        size (int): Kích thước của một ô vuông của thức ăn đặc biệt.
        pos (list): Tọa độ của thức ăn đặc biệt.
        color (tuple): Màu sắc của thức ăn đặc biệt.
    """

    def __init__(self, size):
        self.size = size
        self.pos = [random.randrange(0, WIDTH - self.size, self.size),
                    random.randrange(0, HEIGHT - self.size, self.size)]
        self.color = GREEN

    def respawn(self):
        """
        Tạo lại vị trí ngẫu nhiên mới cho thức ăn đặc biệt.
        """
        self.pos = [random.randrange(0, WIDTH - self.size, self.size),
                    random.randrange(0, HEIGHT - self.size, self.size)]

    def draw(self, surface):
        """
        Vẽ thức ăn đặc biệt lên bề mặt trò chơi.

        Args:
            surface (pygame.Surface): Bề mặt để vẽ thức ăn đặc biệt lên.
        """
        pygame.draw.rect(surface, self.color,
                         (self.pos[0] + 2, self.pos[1] + 2, self.size - 2, self.size - 2))


class Poison:
    """
    Lớp đại diện cho chất độc trong trò chơi.

    Attributes:
        size (int): Kích thước của một ô vuông của chất độc.
        pos (list): Tọa độ của chất độc.
        color (tuple): Màu sắc của chất độc.
    """

    def __init__(self, size):
        self.size = size
        self.pos = [random.randrange(0, WIDTH - self.size, self.size),
                    random.randrange(0, HEIGHT - self.size, self.size)]
        self.color = WHITE

    def respawn(self):
        """
        Tạo lại vị trí ngẫu nhiên mới cho chất độc.
        """
        self.pos = [random.randrange(0, WIDTH - self.size, self.size),
                    random.randrange(0, HEIGHT - self.size, self.size)]

    def draw(self, surface):
        """
        Vẽ chất độc lên bề mặt trò chơi.

        Args:
            surface (pygame.Surface): Bề mặt để vẽ chất độc lên.
        """
        pygame.draw.rect(surface, self.color,
                         (self.pos[0] + 2, self.pos[1] + 2, self.size - 2, self.size - 2))
