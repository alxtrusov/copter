import RPi.GPIO as GPIO
import os
import time

P7 = 7 # Открыть закрыть задвижку
P9 = 9 # ground

# получение данных с датчиков расстояния
class Robot:
    def __init__(self, db, mediator, pins):
        self.db = db
        self.mediator = mediator
        self.TYPES = mediator.getTypes()
        self.PINS = pins
        # Проинициализировать GPIO
        GPIO.setmode(GPIO.BCM)
        # engine move
        GPIO.setup(self.PINS['DROP_PRESENT'], GPIO.OUT)
        GPIO.output(self.PINS['DROP_PRESENT'], False)

        print('start work! GPIO.VERSION=' + GPIO.VERSION)

        # подписки на события
        self.mediator.subscribe(self.TYPES['SHUTDOWN'], self.shutdown)
        self.mediator.subscribe(self.TYPES['REBOOT'], self.reboot)
        self.mediator.subscribe(self.TYPES['FIRE_DROP_PRESENT'], self.dropPresent)

    def __del__(self):
        GPIO.cleanup()
        print('GPIO cleanup')

    # выключиться
    def shutdown(self, options = None):

        print('shutdown')

        #call("sudo nohup shutdown -h now", shell=True)
        os.system("poweroff")
        return True

    # перезагрузка
    def reboot(self, options = None):

        print('reboot')

        #call("sudo nohup shutdown -r now", shell=True)
        os.system('reboot')
        return True

    def dropPresent(self, options = None):
        GPIO.output(self.PINS['DROP_PRESENT'], True)
        #time.sleep(2)
        #GPIO.output(self.PINS['DROP_PRESENT'], False)
        print('dropPresent')
        return True

