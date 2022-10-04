"""
Control the keyboard and mouse to play.
"""


import typing
from src import constants


class Backend:
    def __init__(self) -> None:
        self.screenshot = None
        self.running = False
        self.envolving = False

        self.vs_img = constants.VS_IMG
        self.choose_attack_img = constants.CHOOSE_ATTACK_IMG
        self.choose_pokemon_img = constants.CHOOSE_POKEMON_IMG
        self.evolving_img = constants.EVOLVING_IMG
        self.no_img = constants.NO_IMG
        self.yes_img = constants.YES_IMG

        self.logs = []
        self.moves = ['1', '2', '3', '4']
        self.pokemons = ['1', '2', '3', '4', '5', '6']
        self.logs_size = 100
        self.defeated = 0
        self.last_update = 0
        self.time_running = 0

    def update_screenshot(self) -> None:
        """
        Update `screenshot` attribute.
        """
        from cv2 import cvtColor
        from cv2 import COLOR_RGB2GRAY 
        from numpy import array
        from PIL import ImageGrab

        screenshot = ImageGrab.grab(bbox=None)
        screenshot_array = array(screenshot)
        screenshot_gray = cvtColor(screenshot_array, COLOR_RGB2GRAY)
        self.screenshot = screenshot_gray

    def insert_log(self, log: str) -> None:
        """
        Insert a new log message.
        """
        from datetime import datetime

        now = datetime.now()
        system_time = now.strftime('%H:%M:%S')
        system_date = now.strftime('%Y/%m/%d')
        system_date_time = f'{system_date} {system_time}'
        self.logs.append(f'{system_date_time} -> {log}')
        if len(self.logs) > self.logs_size:
            self.logs.pop(0)

    def print_logs(self) -> None:
        """
        Print all logs messages.
        """
        from os import system
        from time import perf_counter

        lapsed = round(perf_counter() - self.time_running, 2)

        system('clear')
        print(f'{"logs":=^30}')
        print(f'Lapsed: {lapsed} second(s)')
        print(f'Defeated: {self.defeated} pokemon(s)')
        print('-'*30)
        for log in self.logs:
            print(f'|{log}')
        print('='*30)

    def image_on_screenshot(self, image: str) -> typing.Tuple[int, int]:
        """
        Verify with a image appear in the `screenshot` attribute.

        https://www.geeksforgeeks.org/template-matching-using-opencv-in-python/
        """
        from cv2 import imread
        from cv2 import matchTemplate
        from cv2 import TM_CCOEFF_NORMED
        from numpy import where
        
        # loading the image.
        template = imread(image, 0)
        height, width = template.shape
        
        # match
        res = matchTemplate(self.screenshot, template, TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = where(res >= threshold)

        if loc[0].size and loc[1].size:
            initial_x = loc[1][0]
            initial_y = loc[0][0]

            center_x = int(initial_x + (width/2))
            center_y = int(initial_y + (height/2))

            return (center_x, center_y)

        return None

    def update(self) -> None:
        """
        Update things that need be updated.
        """
        from time import perf_counter

        while self.running:
            delay = perf_counter() - self.last_update
            if delay >= 1:
                self.last_update = perf_counter()
                self.update_screenshot()
                self.print_logs()

    def is_fighting(self) -> bool:
        """
        Verify if the player is fighting.
        """
        if self.image_on_screenshot(self.vs_img):
            return True

        return False

    def is_choosing_pokemon(self) -> bool:
        """
        Verify if the player is choosing another pokemon.
        """
        if self.image_on_screenshot(self.choose_pokemon_img):
            return True

        return False

    def check_evolving(self) -> None:
        """
        Check evolving.
        """
        from pyautogui import moveTo
        from pyautogui import click
        from pyautogui import easeInQuad

        if self.image_on_screenshot(self.evolving_img) is not None:
            yes_loaction = self.image_on_screenshot(self.yes_img)
            no_loaction = self.image_on_screenshot(self.no_img)
            self.insert_log('Your pokemon is trying to evolving.')

            if self.envolving:
                self.insert_log('Evolving not working for now.')
                self.insert_log('Stoping the bot.')

            elif not self.envolving:
                self.insert_log('Trying stop the evolve.')
                moveTo(*no_loaction, 1, easeInQuad)
                click()

    def find_wild_pokemon(self) -> None:
        from pyautogui import press
        
        # while not self.is_fighting():
        while self.running:
            self.update_screenshot()
            self.check_evolving()
            self.insert_log('Finding wild pokemon.')
            for _ in range(10):
                press('left', _pause=.05)
                press('right', _pause=.05)

            if self.is_fighting():
                break

        self.insert_log('Wild pokemon finded.')

    def battle_wild_pokemon(self) -> None:
        from pyautogui import press

        current_move = 0
        current_pokemon = 0
        self.insert_log('Starting battle against wild pokemon.') 

        while self.running:
            self.update_screenshot()

            # if choose pokemon is visible, choose next pokemon.
            if self.image_on_screenshot(self.choose_pokemon_img) is not None:
                press(self.pokemons[current_pokemon], _pause=1.0)
                current_pokemon = (current_pokemon+1) % len(self.pokemons)
                current_move = 0
                self.insert_log(f'Choosing the {current_pokemon}th pokemon.')

            # if choose attack is not visible, press `1`.
            elif self.image_on_screenshot(self.choose_attack_img) is None:
                press('1', _pause=1.0)

            # if choose move is visible, attack.
            elif self.image_on_screenshot(self.choose_attack_img) is not None:
                press(self.moves[current_move], _pause=1.0)
                self.insert_log(f'Attacking with {self.moves[current_move]}th move.')
                current_move  = (current_move+1) % len(self.moves)

            # battle ended.

            if not self.is_fighting():
                break
            


        # upadte total pokemons defeated.
        self.defeated += 1

    def start(self) -> None:
        """
        Start the bot.
        """
        from time import perf_counter
        if not self.running:
            self.running = True
            self.defeated = 0
            self.logs = []
            self.time_running = perf_counter()
            self.update_screenshot()
            try:
                while self.running:
                    self.find_wild_pokemon()
                    self.battle_wild_pokemon()
            except Exception as exception:
                print(exception)
                self.running = False
    
    def stop(self) -> None:
        """
        Stop the bot.
        """
        self.running = False
