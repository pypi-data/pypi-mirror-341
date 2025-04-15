from multiutils import all
from colorama import Fore, init

init(autoreset=True)

anim = all.animation(0.1)
anim.single_line_text(Fore.LIGHTCYAN_EX + "Hello World!")