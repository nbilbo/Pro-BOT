import threading
import constants


class Auto:
    def __init__(self) -> None:
        self.vs_img = constants.VS_IMG 
        self.choose_attack_img = constants.CHOOSE_ATTACK_IMG
        self.choose_pokemon_img = constants.CHOOSE_POKEMON_IMG
        self.evolving_img = constants.EVOLVING_IMG
        self.learn_move_img = constants.LEARN_MOVE_IMG
        self.no_img = constants.NO_IMG
        self.yes_img = constants.YES_IMG

        self.time_started = 0
        self.time_last_log = 0
        self.running = False

        self.moves = ['1', '2', '3', '4']
        self.pokemons = ['1', '2', '3', '4', '5', '6']
        self.evolving = False
        self.defeated = 0
        self.logs_size = 10 
        self.logs = []

    def current_date_time(self) -> str:
        from datetime import datetime

        system_date = datetime.now().strftime('%Y/%m/%d')
        system_time = datetime.now().strftime('%H:%M:%S')
        return f'{system_date} {system_time}'
    
    def image_on_screen(self, image: str) -> bool:
        """
        Return if a image is on screen.
        """
        from cv2 import cvtColor
        from cv2 import imread
        from cv2 import matchTemplate
        from cv2 import COLOR_RGB2GRAY 
        from cv2 import TM_CCOEFF_NORMED 
        from PIL import ImageGrab
        from numpy import array
        from numpy import where 

        # taking screen shot
        screenshot = ImageGrab.grab(bbox=None)
        screenshot_array = array(screenshot)
        screenshot_gray = cvtColor(screenshot_array, COLOR_RGB2GRAY)

        # https://www.geeksforgeeks.org/template-matching-using-opencv-in-python/
        image_gray = cvtColor(imread(image), COLOR_RGB2GRAY)
        result = matchTemplate(screenshot_gray, image_gray, TM_CCOEFF_NORMED)
        localization = where(result >= .8)
        return len(localization[0])  > 0
    
    def find_enemy(self) -> None:
        """
        Move the player until the `vs image` is visible.
        """
        from random import randint
        from time import sleep
        from pyautogui import press
        
        self.insert_log(f'{self.current_date_time()} finding enemy.')
        while not self.image_on_screen(self.vs_img):
            for _ in range(randint(5, 15)):
                # press(['left' for _ in range(randint(2, 5))], _pause=0.05)   
                # press(['right' for _ in range(randint(2, 5))], _pause=0.05)   
                press('right', _pause=0.05)   
                press('left', _pause=0.05)   
            self.verify_evolving()
            self.verify_learn_move()

    def verify_evolving(self) -> None:
        """
        Verify if some pokemon is evolving. 
        Depending on if `evolving` attribute, 
        he will try evolve or will avoid.
        """
        from pyautogui import click
        from pyautogui import easeOutQuad
        from pyautogui import locateCenterOnScreen
        from pyautogui import moveTo 

        evolving_finded = self.image_on_screen(self.evolving_img)

        if evolving_finded:
            self.insert_log(f'{self.current_date_time()} Your pokemon is trying to evolve.')

            if not self.evolving:
                self.insert_log(f'{self.current_date_time()} Trying avoid the evolving.')
                no_position = locateCenterOnScreen(self.no_img)
                moveTo(no_position[0], no_position[1], 0.5, easeOutQuad)
                click()

    def verify_learn_move(self) -> None:
        """
        Verify if some pokemon is learning move. 
        he will try dont learn the move.
        """
        from time import sleep
        from pyautogui import click
        from pyautogui import easeOutQuad
        from pyautogui import locateCenterOnScreen
        from pyautogui import moveTo

        learn_position = locateCenterOnScreen(self.learn_move_img)

        if learn_position:
            self.insert_log(f'{self.current_date_time()} Your pokemon is trying learn a new move.')
            self.insert_log(f'{self.current_date_time()} Trying don\'t learn the move.')

            moveTo(learn_position[0], learn_position[1], 0.5, easeOutQuad)
            click()

            yes_position = locateCenterOnScreen(self.yes_img, confidence=0.8)
            moveTo(yes_position[0], yes_position[1], 0.5, easeOutQuad)
            click()

    def attack_enemy(self) -> None:
        """
        While in batle, the player 
        will continue attacking.
        """
        from pyautogui import press

        current_move = 0
        current_pokemon = 0
        self.insert_log(f'{self.current_date_time()} enemy finded.')

        while self.image_on_screen(self.vs_img):
            # choose another pokemon
            if self.image_on_screen(self.choose_pokemon_img):
                self.insert_log(f'{self.current_date_time()} choosing next pokemon.') 
                press(self.pokemons[current_pokemon], _pause=1)
                current_pokemon = (current_pokemon+1) % len(self.pokemons)
                current_move = 0

            # enabling choose attack.
            elif not self.image_on_screen(self.choose_attack_img):
                press('1', _pause=0.5)

             # attacking
            elif self.image_on_screen(self.choose_attack_img):
                self.insert_log(f'{self.current_date_time()} attacking with {current_move+1}º move.')
                press(self.moves[current_move], _pause=0.5)
                current_move = (current_move+1) % len(self.moves)

        # updating total pokemons defated.
        self.defeated += 1

    def insert_log(self, log: str) -> None:
        self.logs.append(log) 
        if len(self.logs) > self.logs_size:
            self.logs.pop(0)

    def print_logs(self) -> None:
        from os import system
        from time import perf_counter


        while self.running:
            log_delay = round(perf_counter() - self.time_last_log)
            if log_delay >= 1:
                system('clear')
                print(f'{"logs":=^30}')
                print(f'defeated: {self.defeated}')
                print(f'time spent: {round(perf_counter() - self.time_started, 2)} second(s)')
                print('-'*30)
                for log in self.logs:
                    print(f'|{log}')
                print('='*30)
                self.time_last_log = perf_counter()
        
    def start(self) -> None:
        from time import sleep
        from time import perf_counter 
        from pyautogui import locateCenterOnScreen

        if not self.running: 
            try:
                # reseting
                self.running = True
                self.time_started = perf_counter()
                self.time_last_log = perf_counter()

                # starting log thread
                log_thread = threading.Thread(target=self.print_logs)
                log_thread.start()

                # starting bot
                while self.running:
                    self.find_enemy()
                    self.attack_enemy()

            except Exception as error:
                print(error)
                self.running = False
        
if __name__ == '__main__':
    import pyautogui
    auto = Auto()
    auto.start()
    # print(auto.image_on_screen(auto.evolving_img))
    # print(list(pyautogui.locateAllOnScreen(auto.evolving_img, confidence=.8)))
    # print(list(pyautogui.locateAllOnScreen(auto.no_img, confidence=.8)))
    # print(list(pyautogui.locateAllOnScreen(auto.yes_img, confidence=.8)))

