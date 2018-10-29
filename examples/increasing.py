"""https://i.imgur.com/r1vHcKH.png"""

import random
from time import sleep

from oscilloscope import Osc


# adjust window_sec and intensity to improve visibility
osc = Osc(window_sec=10, intensity=1)


@osc.signal
def increasing_signal(state):
    delta = 1

    while True:
        state.draw(random.randint(-delta, delta))
        delta += 5
        sleep(0.01)


osc.start()
