import pygame

# Initialize pygame
pygame.init()
# Kích thước màn hình
WIDTH = 1380
HEIGHT = 840

# Các màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Đường dẫn tới các tệp âm thanh
SOUND_FOOD = "food.mp3"
SOUND_POISON = "poison.mp3"
SOUND_SPECIAL_FOOD = "special_food.mp3"
SOUND_SNAKE_HIT_SELF = "poison.mp3"
# Load các tệp âm thanh vào bộ nhớ
sound_food = pygame.mixer.Sound(SOUND_FOOD)
sound_poison = pygame.mixer.Sound(SOUND_POISON)
sound_special_food = pygame.mixer.Sound(SOUND_SPECIAL_FOOD)
sound_snake_hit_self = pygame.mixer.Sound(SOUND_SNAKE_HIT_SELF)


# Khởi tạo cửa sổ game
game_window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Đồng hồ kiểm soát FPS
fps_controller = pygame.time.Clock()
