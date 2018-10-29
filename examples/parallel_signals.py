"""https://i.imgur.com/PPC7z4m.png"""

import random
from time import sleep

from oscilloscope import Osc


osc = Osc(nrows=2, ncols=3)


@osc.signal
def signal1(state):
    while True:
        state.draw(random.random())
        sleep(0.1)


@osc.signal
def signal2(state):
    while True:
        state.draw(random.random(), row=1, col=2)
        sleep(0.1)


osc.start()
