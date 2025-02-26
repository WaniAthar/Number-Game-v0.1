import pygame, json
import os, platform
import highscore as hs
import globalvar as gv
import time


class Text:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_space = 20
        self.text_data = []

        # font
        self.chary = pygame.font.Font(gv.chary_font, 20)

    def append_text_data(self, text, color):
        self.text_data.append([text, color])

    def render(self, screen):
        for i, (text, color) in enumerate(self.text_data):
            text_obj = self.chary.render(text, True, color)
            screen.blit(text_obj, (self.x, i * self.y_space + self.y))

        self.text_data = []


class BootText(Text):
    def draw(self, screen):
        self.append_text_data("8b  8                 8                  .d88b  ", gv.LIME)
        self.append_text_data("8Ybm8 8   8 8d8b.d8b. 88b. .d88b 8d8b    8P www .d88 8d8b.d8b. .d88b  ", gv.LIME)
        self.append_text_data("""8  "8 8b d8 8P Y8P Y8 8  8 8.dP' 8P      8b  d8 8  8 8P Y8P Y8 8.dP'""", gv.LIME)
        self.append_text_data("8   8 `Y8P8 8   8   8 88P' `Y88P 8       `Y88P' `Y88 8   8   8 `Y88P", gv.LIME)
        self.append_text_data("#------------------------------------------------------------------#", gv.WHITE)
        self.append_text_data("Made by R0merol", gv.BLUE)
        self.append_text_data(f"booting up number-game.py", gv.CREAM)
        self.append_text_data(
            f'pygame {pygame.__version__} (SDL {".".join(map(str, pygame.get_sdl_version()))}, Python {platform.python_version()})', gv.CREAM)
        self.append_text_data(f'[Running] python -u "{os.path.dirname(__file__)}/main.py"', gv.CREAM)
        self.append_text_data("#------------------------------------------------------------------#", gv.WHITE)
        self.append_text_data("Loading /", gv.RED)
        self.append_text_data(".", gv.WHITE)
        self.append_text_data(".", gv.WHITE)
        self.append_text_data(".", gv.WHITE)
        self.append_text_data("Complete!", gv.LIME)
        self.append_text_data("", gv.WHITE)
        self.append_text_data("-- Press any key to start --", gv.CREAM)

        self.render(screen)


class ClueText(Text):
    def draw(self, screen):
        if gv.game_state == 'won' or gv.game_state == 'lost' or gv.game_state == 'main_game':
            self.append_text_data(f"Guess the 4 digit number combination! You have {gv.remaining_attempts} "
                                  f"attempts left", gv.CREAM)

            for i in range(gv.attempts):
                self.append_text_data(f"> Attempt #{i + 1}: {gv.correct_num[i]} correct numbers, "
                                      f"{gv.correct_pos[i]} are in the correct position. [{gv.combinations[i]}]",
                                      gv.BLUE)

        if gv.game_state == 'won':
            self.append_text_data(f"You win! The correct number was {gv.secret_num}", gv.LIME)
            self.append_text_data("Press the restart button to play again", gv.RED)

            # check if player is worthy of entering the higscores
            highscore = hs.load_hs()["highscore"]
            is_player_worthy = False
            if len(highscore) == 0:
                is_player_worthy = True
            for i in range(len(highscore)):
                if i + 1 < gv.MAX_HIGHSCORE_LIST:
                    if highscore[i][1] > gv.lapped_time:
                        is_player_worthy = True
                        break
                    elif i + 1 == len(highscore):
                        is_player_worthy = True
                        break

            if is_player_worthy:
                self.append_text_data(f"Enter your name! ({gv.MAX_TEXT_LENGTH} letters): {gv.text_input}", gv.ORANGE)
                last_text = self.text_data[-1][0]
                self.render_blinking_cursor(screen, last_text, gv.ORANGE)
                if time.time() % 1 > 0.5 and len(gv.text_input) > 0:
                    self.append_text_data("---Press Enter---", gv.CREAM)

        if gv.game_state == 'lost':
            self.append_text_data(f"You have run out of attempt! You lost. The correct number was {gv.secret_num}",
                                  gv.RED)
            self.append_text_data("Press the restart button to play again", gv.RED)

        self.render(screen)

    def render_blinking_cursor(self, screen, text, color):
        text_obj = self.chary.render(text, False, color)
        text_rect = text_obj.get_rect(bottomleft=(self.x, self.y + len(self.text_data) * self.y_space))
        cursor_width = 9
        cursor_height = text_rect.height + 2
        cursor = pygame.Rect(text_rect.topright, (cursor_width, cursor_height))

        if time.time() % 1 > 0.5 and len(gv.text_input) != gv.MAX_TEXT_LENGTH:
            cursor.midleft = text_rect.midright
            pygame.draw.rect(screen, color, cursor)


class TimerText(Text):
    def draw(self, screen):
        self.append_text_data(f"T+: {gv.hours}:{gv.minutes}:{gv.seconds}", gv.WHITE)
        self.render(screen)


class HighscoreText(Text):
    def draw(self, screen):
        if gv.game_state == 'highscore':
            self.append_text_data("Highscores!", gv.BLUE)

            highscore = hs.load_hs()["highscore"]
            for index, [player_name, player_time] in enumerate(highscore):
                formatted_player_time = self.reformat_time(player_time)
                formatted_player_name = self.reformat_name(player_name)
                if index < gv.MAX_HIGHSCORE_LIST:
                    self.append_text_data(f"#{index + 1}: {formatted_player_name} - Time: {formatted_player_time}",
                                          gv.WHITE)

            if len(highscore) < gv.MAX_HIGHSCORE_LIST:
                for i in range(gv.MAX_HIGHSCORE_LIST - len(highscore)):
                    dashes = "-" * gv.MAX_TEXT_LENGTH
                    self.append_text_data(f"#{i + len(highscore) + 1}: {dashes} - Time: --:--", gv.WHITE)

        self.render(screen)

    @staticmethod
    def reformat_name(name):
        text_length = len(name)
        if text_length < gv.MAX_TEXT_LENGTH:
            for i in range(gv.MAX_TEXT_LENGTH - text_length):
                name += " "
            return name
        else:
            return name

    @staticmethod
    def reformat_time(miliseconds):
        def add_0(num):
            if len(str(num)) == 1:
                return f"0{num}"
            else:
                return f"{num}"

        seconds = miliseconds // 1000
        str_seconds = add_0(str(seconds % 60))
        str_minutes = add_0(str(seconds // 60))
        return f"{str_minutes}:{str_seconds}"


class AchievementText(Text):
    def draw(self, screen):
        if gv.game_state == 'achievement':
            
            data_json = open("data.json", "r")
            data_json_object = json.load(data_json)

            achievements = data_json_object["achievement"]

            self.append_text_data("Achievements!", gv.LIME)
            self.append_text_data(f"-[{achievements['achv01']}]- I did it!: Finish the puzzle for the first time",
                                  gv.WHITE)
            self.append_text_data(f"-[{achievements['achv02']}]- Quick Solver: Finish the puzzle in less than 1 minute",
                                  gv.WHITE)
            self.append_text_data(
                f"-[{achievements['achv03']}]- Speedrunner: Finish the puzzle in less than 10 seconds", gv.WHITE)
            self.append_text_data(f"-[{achievements['achv04']}]- The Dragon: Solve the puzzle in one attempt", gv.WHITE)
            self.append_text_data(f"-[{achievements['achv05']}]- Sloth: Finish the puzzle in more than an hour",
                                  gv.WHITE)
            self.append_text_data(f"-[{achievements['achv06']}]- AFK: Leave the game running for a day", gv.WHITE)

            self.render(screen)
