# Oscilloscope
An oscilloscope for python that just works™


### It's fucking simple to use

*This*

```python3
import random
from time import sleep

import oscilloscope


osc = oscilloscope.Osc()

@osc.updater
def random_signal(update):
    while True:
        update(random.random())
        sleep(0.1)
        
osc.start()
```

*Gives you this*

<img src="https://i.imgur.com/jB3wzgT.png" height="300" />

### Parallel compute in-built

Each `osc.updater` gets it's own process.

*This*

```python3
import random
from time import sleep

osc = Osc(nrows=2, ncols=3)

@osc.updater
def signal1(update):
    while True:
        update(random.random())
        sleep(0.1)

@osc.updater
def signal2(update):
    while True:
        update(random.random(), row=1, col=2)
        sleep(0.1)

osc.start()
```

*Gives you this*

<img src="https://i.imgur.com/JWHQ9Da.png" height="300" />
