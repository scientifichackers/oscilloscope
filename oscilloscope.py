import matplotlib

matplotlib.use("Qt5Agg")

from functools import wraps
from typing import Union

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import zproc
from matplotlib.lines import Line2D

ctx = zproc.Context()


class Normalizer:
    def __init__(self):
        self.bounds = [0, 0]
        self.norm_factor = 0

    def refresh_norm_factor(self):
        self.norm_factor = 1 / (self.bounds[1] - self.bounds[0]) * 100

    def adjust_norm_factor(self, val):
        if val < self.bounds[0]:
            self.bounds[0] = val
            self.refresh_norm_factor()
        elif val > self.bounds[1]:
            self.bounds[1] = val
            self.refresh_norm_factor()

    def normalize(self, val):
        self.adjust_norm_factor(val)

        return (val - self.bounds[0]) * self.norm_factor


class AnimationScope:
    def __init__(
        self,
        ax,
        window_sec,
        frame_interval_sec,
        xlabel,
        ylabel,
        row_index,
        col_index,
        intensity,
    ):
        self.row_index = row_index
        self.col_index = col_index
        self.ax = ax

        self.bounds = [0, 0]

        num_frames = int(window_sec / frame_interval_sec)
        self.time_axis = np.linspace(-window_sec, 0, num_frames)
        self.amplitude_axis = np.zeros([1, num_frames])

        self.line = Line2D(self.time_axis, self.amplitude_axis, linewidth=intensity)
        self.ax.add_line(self.line)
        self.ax.set(xlim=(-window_sec, 0), xlabel=xlabel, ylabel=ylabel)

    def refresh_ylim(self):
        self.ax.set_ylim(self.bounds)

    def adjust_ylim(self, amplitude):
        if amplitude < self.bounds[0]:
            self.bounds[0] = amplitude
            self.refresh_ylim()
        elif amplitude > self.bounds[1]:
            self.bounds[1] = amplitude
            self.refresh_ylim()

    def draw(self, n):
        amplitude = ctx.state.get((self.row_index, self.col_index), 0)

        # make adjustments to the ylim if required
        self.adjust_ylim(amplitude)

        # Add new amplitude to end
        self.amplitude_axis = np.append(self.amplitude_axis, amplitude)

        # remove old amplitude from start
        self.amplitude_axis = np.delete(self.amplitude_axis, 0)

        # update line
        self.line.set_data(self.time_axis, self.amplitude_axis)

        return (self.line,)


class Osc:
    def __init__(
        self,
        *,
        fps: Union[float, int] = 60,
        window_sec: Union[float, int] = 5,
        intensity: Union[float, int] = 2.5,
        normalize: bool = False,
        xlabel: str = "Time (sec)",
        ylabel: str = "Amplitude",
        nrows: int = 1,
        ncols: int = 1,
    ):
        frame_interval_sec = 1 / fps

        self.nrows = nrows
        self.ncols = ncols
        self.normalize = normalize

        self.scopes = []
        self.gc_protect = []

        fig, axes = plt.subplots(self.nrows, self.ncols, squeeze=False)

        for row_index, row_axes in enumerate(axes):
            for col_index, ax in enumerate(row_axes):
                scope = AnimationScope(
                    ax,
                    window_sec,
                    frame_interval_sec,
                    xlabel,
                    ylabel,
                    row_index,
                    col_index,
                    intensity,
                )

                self.gc_protect.append(
                    animation.FuncAnimation(
                        fig, scope.draw, interval=frame_interval_sec * 1000, blit=True
                    )
                )

                self.scopes.append(scope)

    def signal(self, fn):
        @wraps(fn)
        def _singal(state, nrows, ncols, normalize):
            if normalize:
                normalizer = Normalizer()

                def update_fn(amplitude, row=0, col=0):
                    if not 0 <= row < nrows:
                        raise ValueError(
                            f'"row" must be one of {list(range(0, nrows))}'
                        )
                    if not 0 <= col < ncols:
                        raise ValueError(
                            f'"col" must be one of {list(range(0, ncols))}'
                        )

                    state[(row, col)] = normalizer.normalize(amplitude)

            else:

                def update_fn(amplitude, row=0, col=0):
                    if not 0 <= row < nrows:
                        raise ValueError(
                            f'"row" must be one of {list(range(0, nrows))}'
                        )
                    if not 0 <= col < ncols:
                        raise ValueError(
                            f'"col" must be one of {list(range(0, ncols))}'
                        )

                    state[(row, col)] = amplitude

            fn(update_fn)

        return ctx.process(_singal, args=(self.nrows, self.ncols, self.normalize))

    def start(self):
        plt.show()

    def stop(self):
        ctx.stop_all()
        plt.close()
        print(ctx.process_list)
