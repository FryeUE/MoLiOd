from RPLCD import *
from RPLCD.i2c import CharLCD
import subprocess
import os
from time import sleep
from pynput import keyboard

from SplashCol import Splash0

class MoLiOd:
    def __init__(self):
        self.lcd = CharLCD('PCF8574', 0x27)
        self.TestFlag = False
        self.BStr = ''
#Bootup Splash
        splash0 = Splash0(self)
#Keyboard Listener (non-blocking)
        self.Listener()
#FSM Initialize
        self.SetCurState(0)
        self.RunningMachina()

#State Machine Handler
    def SetCurState(self, CurState):
        #self.lcd.clear()
        self.CurState = CurState

    def FSM(self):
        StCol = [self.Status,self.StrPush, self.BashMachina, self.BashMachina2]
        return StCol[self.CurState]()

    def RunningMachina(self):
        while True:
            self.FSM()
 
#Keyboard Handlers
    def Listener(self):
        self.listener = keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+a': self.hot_launch,
        '<ctrl>+<alt>+o': self.hot_launch})
        #print('made it this far')
        self.listener.start()
    
    def hot_launch(self):
        if self.CurState == 3:
            self.SetCurState(0)
        else :
            self.SetCurState(2)
    
        
        #self.listener = keyboard.Listener(on_press=self.on_press)
        #self.listener.start()

    def on_press(self, key):
        self.TestFlag = True
        try:
            if key.char == 'p':
                self.SetCurState(1)
            elif key.char == 'l':
 #               self.lcd.clear()
                self.SetCurState(2)
        except AttributeError:
            if key == 'esc':
                print('escaper')
#elif key.char == 'e':
             #   self.SetCurState(2)

#Screens/States
    def Status(self):
        bork = self.StringCenter('MoLiOd v.00')
        self.lcd.home()
        Temperature_Value = self.StringCenter(subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True).stdout[5:9])
        Current_Date = self.StringCenter(subprocess.run(['date', '+%D'], capture_output=True, text=True).stdout[:-1])
        Current_Time = self.StringCenter(subprocess.run(['date', '+%T'], capture_output=True, text=True).stdout[:-1])

        self.lcd.write_string(bork)
        self.lcd.write_string(Current_Date)
        self.lcd.write_string(Current_Time)
        self.lcd.write_string(Temperature_Value)
        
    def StrPush(self):
        StateCheck = 'Mona Lisa Overdrive'
        self.lcd.home() 
        self.lcd.write_string(StateCheck)
        Temperature_Value = self.StringCenter(subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True).stdout[5:9])
        Current_Date = self.StringCenter(subprocess.run(['date', '+%D'], capture_output=True, text=True).stdout[:-1])
        Current_Time = self.StringCenter(subprocess.run(['date', '+%T'], capture_output=True, text=True).stdout[:-1])
        self.lcd.write_string(Current_Date)
        self.lcd.write_string(Current_Time)
        self.lcd.write_string(Temperature_Value)

    def BashMachina(self):
        self.lcd.home()
        Current_Dir = subprocess.check_output(['pwd'])
        NewStr = self.StringLeft(str(Current_Dir))
        self.lcd.write_string(NewStr) #wwwos.getcwd())
        BashBump = '$: '
        TerStr = self.TerminalStr(BashBump)
        self.lcd.write_string(TerStr)
        self.SetCurState(3)
    
    
    def BashMachina2(self):
        self.lcd.cursor_pos = (1,3)
        self.lcd.write_string(self.BStr)
        with keyboard.Listener(on_press=self.BComBuilder) as listen2:
            listen2.join()

    def BComBuilder(self, key):
        try:
            self.BStr = self.BStr + key.char
            self.FSM()
        except AttributeError:
            if key == key.backspace:
                self.BStr = self.BStr[:-1]
                self.FSM()
            elif key == key.space:
                spece = ' '
                self.BStr = self.BStr + spece
                self.FSM()
            elif key == key.enter:
                if self.CurState == 3:
                    #print('runnah')
                    #tempVal = self.BStr.split()
                    nook = subprocess.run(self.BStr, text=True, shell=True)
                    spece = ' '
                    clear = self.TerminalStr(spece)
                    self.lcd.home()
                    self.lcd.write_string(clear)
                    self.BStr = ''
                    self.SetCurState(2)
                    self.FSM()
                else :
                    self.FSM()
            else:
                self.FSM()
                #print('special key {0} pressed'.format(
                 #   key))


#String Handler
    def StringCenter(self, inStr):
        spece = ' '
        if len(inStr) < 20:
            tLen = 20 - len(inStr)
            lLen = tLen // 2
            inStr = str((spece * lLen) + inStr + (spece * lLen))
        return inStr

    def StringRight(self, inStr):
        spece = ' '
        if len(inStr) < 20:
            tLen = 20 - len(inStr)
            inStr = str((spece * tLen) + inStr)
            print(inStr)
        return inStr

    def StringLeft(self, inStr):
        spece = ' '
        inStr = inStr[2:-3]
        if len(inStr) < 20:
            tlen = 20 - len(inStr)
            inStr = str(inStr + (spece * tlen))
        return(inStr)

    def TerminalStr(self, inStr):
        spece = ' '
        if len(inStr) < 60:
            tlen = 60 - len(inStr)
            inStr = str(inStr + (spece * tlen))
        return inStr

    def TerminalBWrite(self, inStr):
        spece = ' '
        if len(inStr) < 57:
            tlen = 57 - len(inStr)
            inStr = str(inStr + (spece * tlen))
        return inStr

if __name__ == '__main__':
    print('mnr')
    hooda = MoLiOd()




