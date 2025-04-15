import time, os

class animation:
    def __init__(self, time_sec: float):
        self.time_sec = time_sec

    def clear_cmd(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def single_line_text(self, text: str) -> None:
        letters = list(text)
        word = ""
        for letter in letters:
            self.clear_cmd()
            print(word + letter)
            word += letter
            time.sleep(self.time_sec)