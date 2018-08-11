# oscilloscope
An oscilloscope for python that just works™

```python3
import random
from time import sleep

osc = Oscilloscope(nrows=5, ncols=5)

@osc.updater()
def signal1(update):
    while True:
        update(row_index=0, col_index=0, amplitude=random.random())
        sleep(0.1)

@osc.updater()
def signal2(update):
    while True:
        update(4, 1, random.random())
        sleep(0.1)

osc.start()
```
