from time import sleep

class Splash0:
    def __init__(self, InObj):
        self.lcd = InObj.lcd
        self.lcd.backlight_enabled=False
        sleep(.5)
        self.lcd.backlight_enabled=True
        spece = ' '
        buff = '*'
        bork = 'MoLiOd v.00 Booting'
        self.lcd.home() 
        self.lcd.write_string(buff * 20)
        self.lcd.write_string(spece + bork)
        self.lcd.write_string(buff * 40)
        sleep(1)
        self.lcd.clear()