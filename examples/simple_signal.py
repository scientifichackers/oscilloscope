"""https://i.imgur.com/BMeYoXG.png"""

import random
from time import sleep

from oscilloscope import Osc

osc = Osc()


@osc.signal
def simple_random_signal(update):
    while True:
        update(random.random())
        sleep(0.1)


osc.start()
