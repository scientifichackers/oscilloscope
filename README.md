# Oscilloscope
An oscilloscope for python that just works™

```python3
import random
from time import sleep

import oscilloscope


osc = oscilloscope.Osc(nrows=3, ncols=3)

@osc.updater()
def signal1(update):
    while True:
        update(random.random())
        sleep(0.1)

@osc.updater()
def signal2(update):
    while True:
        update(random.random(), row=1, col=2)
        sleep(0.1)

osc.start()
```

![Image](https://i.imgur.com/JWHQ9Da.png)
