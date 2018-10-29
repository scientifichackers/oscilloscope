# Oscilloscope
**An oscilloscope for python that just works™**

## Features

### Simple to use

[*This*](examples/simple_signal.py)
```python3
import random
from time import sleep

from oscilloscope import Osc

osc = Osc()


@osc.signal
def simple_random_signal(state):
    while True:
        state.draw(random.random())
        sleep(0.1)


osc.start()
```
*Gives you this*

<img src="https://i.imgur.com/BMeYoXG.png" height="300" />

### Parallel compute

Each `osc.signal` gets it's own process.

[*This*](examples/parallel_signals.py)
```python3
import random
from time import sleep

from oscilloscope import Osc


osc = Osc(nrows=2, ncols=3)


@osc.signal
def signal1(state):
    while True:
        state.draw((random.random())
        sleep(0.1)


@osc.signal
def signal2(state):
    while True:
        state.draw(random.random(), row=1, col=2)
        sleep(0.1)


osc.start()
```
*Gives you this*

<img src="https://i.imgur.com/PPC7z4m.png" height="300" />

P.S. Don't worry about race conditions, `state.draw()` is atomic. (See [zproc](https://github.com/pycampers/zproc))

### Dynamic axis scale

The Y-axis's scale is dynamic, meaning that the graph's y axis scales with your signal.

[*This*](examples/increasing.py)
```python3
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
```
*Gives you this*

<img src="https://i.imgur.com/r1vHcKH.png" height="300" />

### Automatic normalization

[*This*](examples/normalized.py)
```python3
import random
from time import sleep

from oscilloscope import Osc


# turn on normalization
osc = Osc(normalize=True)


@osc.signal
def increasing_signal(state):
    delta = 1

    while True:
        state.draw(random.randint(-delta, delta))
        delta += 5
        sleep(0.01)


osc.start()
```
*Gives you this*

<img src="https://i.imgur.com/Dlve8rJ.png" height="300" />

This was the same signal as the [last example](#dynamic-axis-scale), 
but it looks a lot like the [simple example](#simple-to-use), because we turned on normalization! 

The Y-axis will now show, % max-amplitude encountered at the time, not the raw value.


## Install


`pip install oscilloscope`

Licence: MIT<br>
Requires Python >= 3.6

---

<a href="https://www.buymeacoffee.com/u75YezVri" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/black_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

[🐍🏕️](http://www.pycampers.com/)
