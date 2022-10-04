import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMGS_DIR = os.path.join(ASSETS_DIR, 'imgs')

VS_IMG = os.path.join(IMGS_DIR, 'vs.png')
CHOOSE_ATTACK_IMG = os.path.join(IMGS_DIR, 'choose_attack.png')
CHOOSE_POKEMON_IMG = os.path.join(IMGS_DIR, 'choose_pokemon.png')
EVOLVING_IMG = os.path.join(IMGS_DIR, 'evolving.png')
LEARN_MOVE_IMG = os.path.join(IMGS_DIR, 'learn_move.png')
NO_IMG = os.path.join(IMGS_DIR, 'no.png')
YES_IMG = os.path.join(IMGS_DIR, 'yes.png')
IN_FIGHT_IMG = os.path.join(IMGS_DIR, 'in_fight.png')

THEMES_DIR = os.path.join(ASSETS_DIR, 'themes')
DARK_THEME = os.path.join(THEMES_DIR, 'dark.css')
DARKBLUE_THEME = os.path.join(THEMES_DIR, 'darkblue.css')
