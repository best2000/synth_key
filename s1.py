import keyboard, winsound
class synth_key:
    def __init__(self):
        self.mode = 1
        keyboard.add_hotkey('1', lambda: self.change_mode(1))
        keyboard.add_hotkey('2', lambda: self.change_mode(2))
        keyboard.add_hotkey('3', lambda: self.change_mode(3))

        keyboard.add_hotkey('a', lambda: self.beep()) 

    def beep(self):
        winsound.Beep(self.mode*1000, 10)

    def change_mode(self, m):
        self.mode = m

s = synth_key()

while True:
    pass