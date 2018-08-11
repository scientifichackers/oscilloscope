# Oscilloscope
**An oscilloscope for python that just works™**


### It's fucking simple to use

*This*

```python3
import random
from time import sleep

from oscilloscope import Osc


osc = Osc()

@osc.signal
def random_signal(s):
    while True:
        s(random.random())
        sleep(0.1)
        
osc.start()
```

*Gives you this*

<img src="https://i.imgur.com/jB3wzgT.png" height="300" />

### Parallel compute in-built

Each `osc.signal` gets it's own process.

*This*

```python3
import random
from time import sleep

from oscilloscope import Osc


osc = Osc(nrows=2, ncols=3)

@osc.signal
def signal1(s):
    while True:
        s(random.random())
        sleep(0.1)

@osc.signal
def signal2(s):
    while True:
        s(random.random(), row=1, col=2)
        sleep(0.1)

osc.start()
```

*Gives you this*

<img src="https://i.imgur.com/JWHQ9Da.png" height="300" />

### Automatic normalization built-in

*This*
```python3
import random
from time import sleep

from oscilloscope import Osc


# increase the time scale so we can see clearly
osc = Osc(time_scale_sec=10)  

@osc.signal
def irregular_signal(s):
    for _ in range(10):
        s(random.randint(0, 1))
        sleep(0.1)

    s(0.5)
    print("So I'm totally gonna fuck up after a sec")
    sleep(5)

    while True:
        s(random.randint(0, 1000))
        sleep(0.1)

osc.start()
```

*Gives you this*
<img src="https://i.imgur.com/8TYCaaK.png" height="300" />

Notice, how, after the 5 sec pause, the range of input changes drastically, but the graph still retains its coherence.
