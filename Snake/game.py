# game.py

import pygame
import sys
import random
from config import *

from __init__ import *


class Game:
    """
    Lớp đại diện cho trò chơi Snake.

    Attributes:
        width (int): Chiều rộng của cửa sổ trò chơi.
        height (int): Chiều cao của cửa sổ trò chơi.
        square_size (int): Kích thước của một ô vuông trong trò chơi.
        snake (Snake): Đối tượng rắn trong trò chơi.
        food (Food): Đối tượng thức ăn trong trò chơi.
        special_food (SpecialFood): Đối tượng thức ăn đặc biệt trong trò chơi.
        poisons (list): Danh sách các đối tượng chất độc trong trò chơi.
        score (int): Điểm số của trò chơi.
        lives (int): Số mạng của người chơi.
        time (int): Thời gian đã trôi qua trong trò chơi.
        special_food_timer (int): Bộ đếm thời gian cho thức ăn đặc biệt.
        poison_timer (int): Bộ đếm thời gian cho chất độc.
        food_eaten (int): Số lượng thức ăn đã ăn.
        start_time (int): Thời gian bắt đầu trò chơi.
        direction_changed (bool): Cờ để kiểm tra hướng di chuyển đã thay đổi.
    """

    def __init__(self, width, height, square_size):
        self.width = width
        self.height = height
        self.square_size = square_size
        self.snake = Snake(120, 60, square_size, WIDTH, HEIGHT)
        self.food = Food(square_size)
        self.special_food = None
        self.poisons = []
        self.score = 0
        self.lives = 3
        self.time = 0
        self.special_food_timer = 0
        self.poison_timer = 0
        self.food_eaten = 0
        self.start_time = 0
        self.direction_changed = False

    def handle_events(self):
        """
        Xử lý các sự kiện từ bàn phím và cửa sổ trò chơi.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not self.direction_changed:  # Chỉ thay đổi hướng nếu chưa có thay đổi nào trước đó
                    if event.key == pygame.K_UP or event.key == ord("w"):
                        self.snake.change_direction("UP")
                    elif event.key == pygame.K_DOWN or event.key == ord("s"):
                        self.snake.change_direction("DOWN")
                    elif event.key == pygame.K_LEFT or event.key == ord("a"):
                        self.snake.change_direction("LEFT")
                    elif event.key == pygame.K_RIGHT or event.key == ord("d"):
                        self.snake.change_direction("RIGHT")
                    self.direction_changed = True

    def update(self):
        """
        Cập nhật trạng thái của trò chơi.
        """
        self.snake.move()
        head_pos = self.snake.body[0]
        # check xem rắn đã ăn thức ăn chưa
        if head_pos == self.food.pos:
            self.score += 1
            sound_food.play()
            self.food.respawn()
            self.food_eaten += 1
            # Kiểm tra xem thức ăn có được tạo ra trên cơ thể rắn không
            while self.food.pos in self.snake.body:
                self.food.respawn()
        else:
            self.snake.body.pop()

        # Kiểm tra xem con rắn có đâm vào thân hay không
        if head_pos in self.snake.body[1:]:
            self.lives -= 1
            if self.lives > 1:
                self.snake.body = [self.snake.body[0]]
            else:
                self.show_game_over()
            sound_snake_hit_self.play()
        # Update time
        self.time = pygame.time.get_ticks() // 1000

        # tăng thời gian thức ăn đặc biệt
        self.special_food_timer += 0.5
        self.poison_timer += 1

        # Tạo thức ăn đặc biệt sau khi rắn đã ăn 5 thức ăn thường
        if self.food_eaten == 5:
            if self.special_food_timer >= 20:
                self.special_food = SpecialFood(self.square_size)
                self.special_food.respawn()
                # Kiểm tra xem thức ăn đặc biệt đc tạo trên thân con rắn hay không
                while self.special_food.pos in self.snake.body:
                    self.special_food.respawn()
                self.special_food_timer = 0
            self.food_eaten = 0

        # Ẩn đi thức ăn đặc biệt sau 2.5
        if self.special_food and self.special_food_timer >= 25:
            self.special_food = None
        # Tạo độc sau mỗi 5 giây
        if self.poison_timer == 50:
            num_poisons = random.randint(2, 6)
            self.poisons = []
            for _ in range(num_poisons):
                new_poison = Poison(self.square_size)
                new_poison.respawn()
                ''' Mỗi lần vòng lặp chạy, nó tạo ra một chất độc mới và sau đó kiểm tra xem 
                chất độc đó có xuất hiện trên cơ thể của con rắn (snake body), 
                gần với đầu rắn (snake head), gần thức ăn đặc biệt (special food) hoặc trên thức ăn (food) hay không. 
                Nếu có bất kỳ điều kiện nào không đáp ứng, chất độc sẽ được tạo lại (respawn). 
                Điều này đảm bảo rằng các chất độc không xuất hiện ở những vị trí gây rủi ro cho người chơi. 
                Sau khi tất cả các chất độc được tạo ra và đảm bảo rằng chúng không gây rủi ro, đồng hồ đếm thời gian cho chất độc được đặt lại về 0
                '''

                while (new_poison.pos in self.snake.body) or \
                    (abs(new_poison.pos[0] - head_pos[0]) < self.square_size * 2 and
                     abs(new_poison.pos[1] - head_pos[1]) < self.square_size * 2) or\
                    (self.special_food and abs(new_poison.pos[0] - self.special_food.pos[0]) < self.square_size * 2 and
                     abs(new_poison.pos[1] - self.special_food.pos[1]) < self.square_size * 2) or\
                    (abs(new_poison.pos[0] - self.food.pos[0]) < self.square_size * 2 and
                     abs(new_poison.pos[1] - self.food.pos[1]) < self.square_size * 2):
                    new_poison.respawn()
                self.poisons.append(new_poison)
            self.poison_timer = 0

        # check xem rắn ăn thức ăn đặc biệt hay không
        if self.special_food and head_pos == self.special_food.pos:
            if self.lives < 5:
                self.lives += 1
            self.score += 5
            sound_special_food.play()
            self.special_food = None

        # Check xem rắn ăn độc hay không
        for poison in self.poisons:
            if poison and head_pos == poison.pos:
                if self.lives > 1:
                    self.lives -= 1
                else:
                    self.show_game_over()
                    continue
                sound_poison.play()
                self.poisons.remove(poison)

        # Reset direction_changed flag
        self.direction_changed = False

    def format_time(self):
        """
        Định dạng thời gian chơi từ khi bắt đầu lại.

        Returns:
            str: Chuỗi thời gian đã định dạng.
        """
        # Thời gian đã trôi qua từ lúc chơi lại
        elapsed_time = pygame.time.get_ticks() // 1000 - self.start_time
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        return "{:02d}:{:02d}".format(minutes, seconds)

    def show_info(self):
        """
        Hiển thị thông tin trò chơi như điểm số, số mạng và thời gian.
        """
        font = pygame.font.SysFont('consolas', 20)
        score_surface = font.render("Score: " + str(self.score), True, WHITE)
        game_window.blit(score_surface, (WIDTH / 40, 50))
        lives_surface = font.render("Lives: " + str(self.lives), True, WHITE)
        game_window.blit(lives_surface, (WIDTH / 40, 10))
        time_surface = font.render("Time: " + self.format_time(), True, WHITE)
        game_window.blit(time_surface, (WIDTH / 40, 90))

    def show_game_over(self):
        """
        Hiển thị màn hình kết thúc trò chơi và xử lý sự kiện cho phép người chơi chơi lại or thoát.
        """
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.handle_events()
                        self.update()
                        self.draw()
                        self.format_time()
                        pygame.display.update()
                        fps_controller.tick(10)
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            game_window.fill(BLACK)
            font = pygame.font.SysFont('arial', 30)
            line1 = font.render(
                f"Game over! Your score is {self.score}", True, (255, 255, 255))
            line2 = font.render(
                "To play again press Enter. To exit press Escape!", True, (255, 255, 255))
            game_window.blit(line1, (200, 300))
            game_window.blit(line2, (200, 350))
            final_score = font.render(
                f"Final Score: {self.score}", True, (255, 255, 255))
            game_window.blit(final_score, (200, 400))
            pygame.display.flip()

    def draw(self):
        """
        Vẽ tất cả các thành phần của trò chơi lên bề mặt trò chơi.
        """
        game_window.fill(BLACK)
        self.snake.draw(game_window)
        self.food.draw(game_window)
        if self.special_food:
            # Hiển thị thức ăn đặc biệt
            self.special_food.draw(game_window)
            # Hiển thị thời gian đếm ngược trên thức ăn đặc biệt
            font = pygame.font.SysFont('consolas', 20)
            countdown_surface = font.render(
                str(int(24 - self.special_food_timer)), True, WHITE)
            countdown_rect = countdown_surface.get_rect(center=(
                self.special_food.pos[0] + self.square_size // 2, self.special_food.pos[1] + self.square_size // 2))
            game_window.blit(countdown_surface, countdown_rect)
        for poison in self.poisons:
            if poison:
                poison.draw(game_window)
        self.show_info()

    def reset_game(self):
        """
        Đặt lại trạng thái trò chơi để bắt đầu lại từ đầu.
        """
        # Reset game state
        self.snake = Snake(120, 60, self.square_size, WIDTH, HEIGHT)
        self.food = Food(self.square_size)
        self.special_food = None
        self.poisons = []
        self.score = 0
        self.lives = 3
        self.time = 0
        self.start_time = pygame.time.get_ticks() // 1000  # Đặt lại thời gian bắt đầu
        self.special_food_timer = 0
        self.poison_timer = 0
        self.food_eaten = 0

    def show_intro(self):
        """
        Hiển thị màn hình giới thiệu trước khi bắt đầu trò chơi.
        """
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        intro = False

            game_window.fill(BLACK)
            font = pygame.font.SysFont('arial', 50)
            intro_text = font.render("Welcome to Snake Game", True, WHITE)
            start_text = font.render("Press Enter to Start", True, WHITE)
            game_window.blit(intro_text, (WIDTH / 4, HEIGHT / 3))
            game_window.blit(start_text, (WIDTH / 4, HEIGHT / 2))
            pygame.display.flip()

    def run(self):
        """
        Chạy trò chơi Snake.
        """
        self.show_intro()  # Show màn hình bắt đầu
        while True:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            fps_controller.tick(10)


if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT, 60)
    game.run()
