import time

import psutil

from oscilloscope import Osc

osc = Osc(nrows=2, ncols=2)


@osc.signal
def cpu_usage(state):
    # This will adjust graph to the max value, 100 and set the labels.
    state.draw(100, col=0, ylabel="core0")
    state.draw(100, col=1, ylabel="core1")

    while True:
        time.sleep(0.25)
        for i, cpu in enumerate(psutil.cpu_percent(percpu=True)):
            state.draw(cpu, col=i)


@osc.signal
def ram_usage(state):
    # This will adjust graph to the max value, 100 and set the labels.
    state.draw(100, row=1, ylabel="ram")

    while True:
        time.sleep(0.25)
        meminfo = psutil.virtual_memory()
        state.draw(meminfo.available / meminfo.total * 100, row=1)


@osc.signal
def combined_cpu(state):
    # This will adjust graph to the max value, 100 and set the labels.
    state.draw(100, row=1, col=1, ylabel="total cpu")

    while True:
        time.sleep(0.25)
        state.draw(psutil.cpu_percent(), row=1, col=1)


osc.start()
