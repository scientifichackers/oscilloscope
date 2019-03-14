from functools import wraps
from typing import Union, Callable

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import zproc
from matplotlib.lines import Line2D

zproc_ctx = zproc.Context()
ZPROC_INTERNAL_NAMESPACE = "oscilloscope"


class Normalizer:
    def __init__(self, output_range: tuple = (0, 100)):
        self._input_min = 0
        self._input_max = 0

        self._output_min, self._output_max = output_range
        self._output_diff = self._output_max - self._output_min

        self._norm_factor = 0

    def _refresh_norm_factor(self):
        self._norm_factor = 1 / (self._input_max - self._input_min) * self._output_diff

    def _refresh_bounds(self, input_value):
        if input_value < self._input_min:
            self._input_min = input_value
            self._refresh_norm_factor()
        elif input_value > self._input_max:
            self._input_max = input_value
            self._refresh_norm_factor()

    def normalize(self, input_value):
        self._refresh_bounds(input_value)
        return (input_value - self._input_min) * self._norm_factor + self._output_min


def shift(ax, x):
    return np.delete(np.append(ax, x), 0)


class AnimationScope:
    def __init__(
        self,
        ax: plt.Axes,
        window_sec,
        frame_interval_sec,
        row_index,
        col_index,
        intensity,
        padding_percent,
    ):
        self.row_index = row_index
        self.col_index = col_index
        self.ax = ax
        self.padding_percent = padding_percent

        self.frame_interval_sec = frame_interval_sec
        self.num_frames = int(window_sec / self.frame_interval_sec)

        self.y_values = np.zeros([1, self.num_frames])
        self.x_values = np.linspace(-window_sec, 0, self.num_frames)

        self.line = Line2D(self.x_values, self.y_values, linewidth=intensity)
        self.ax.add_line(self.line)
        self.ax.set_xlim(-window_sec, 0)

        self.y_limits = np.array([0, np.finfo(np.float).eps])
        self.ax.set_ylim(self.y_limits[0], self.y_limits[1])

        self._internal_state = zproc_ctx.create_state(
            namespace=ZPROC_INTERNAL_NAMESPACE
        )

    def _adjust_ylim(self):
        padding = self.padding_percent * (self.y_limits[1] - self.y_limits[0]) / 100
        self.ax.set_ylim(self.y_limits[0] - padding, self.y_limits[1] + padding)

    def _adjust_ylim_if_req(self, amplitude):
        if amplitude < self.y_limits[0]:
            self.y_limits[0] = amplitude
            self._adjust_ylim()
        elif amplitude > self.y_limits[1]:
            self.y_limits[1] = amplitude
            self._adjust_ylim()

    def draw(self, _):
        try:
            amplitude, kwargs = self._internal_state[(self.row_index, self.col_index)]
        except KeyError:
            pass
        else:
            # set the labels
            self.ax.set(**kwargs)

            try:
                size = np.ceil(self.num_frames / len(amplitude))
                self.y_values = np.resize(
                    np.repeat(np.array([amplitude]), size, axis=1), [1, self.num_frames]
                )

                self._adjust_ylim_if_req(np.min(self.y_values))
                self._adjust_ylim_if_req(np.max(self.y_values))
            except TypeError:
                self.y_values = shift(self.y_values, amplitude)
                self._adjust_ylim_if_req(amplitude)

            # update line
            self.line.set_data(self.x_values, self.y_values)
        return [self.line]


def _signal_process(ctx: zproc.Context, fn: Callable, normalize: bool, *args, **kwargs):
    if normalize:
        normalizer = Normalizer()

        def _normalize(val):
            return normalizer.normalize(val)

    else:

        def _normalize(val):
            return val

    state = ctx.create_state()
    _internal_state = state.fork(namespace=ZPROC_INTERNAL_NAMESPACE)

    def draw(amplitude, *, row=0, col=0, **kwargs):
        amplitude = _normalize(amplitude)
        _internal_state[(row, col)] = amplitude, kwargs

    state.draw = draw
    fn(state, *args, **kwargs)


class Osc:
    def __init__(
        self,
        *,
        fps: Union[float, int] = 24,
        window_sec: Union[float, int] = 5,
        intensity: Union[float, int] = 2.5,
        normalize: bool = False,
        xlabel: str = "Time (sec)",
        ylabel: str = "Amplitude",
        nrows: int = 1,
        ncols: int = 1,
        padding_percent: Union[float, int] = 0,
    ):
        frame_interval_sec = 1 / fps

        self.nrows = nrows
        self.ncols = ncols
        self.normalize = normalize
        self.xlabel = xlabel
        self.ylabel = ylabel

        self.anim_scopes = {}
        self.gc_protect = []

        fig, axes = plt.subplots(self.nrows, self.ncols, squeeze=False)

        for row_index, row_axes in enumerate(axes):
            for col_index, ax in enumerate(row_axes):
                scope = AnimationScope(
                    ax=ax,
                    window_sec=window_sec,
                    frame_interval_sec=frame_interval_sec,
                    row_index=row_index,
                    col_index=col_index,
                    intensity=intensity,
                    padding_percent=padding_percent,
                )

                self.gc_protect.append(
                    animation.FuncAnimation(
                        fig, scope.draw, interval=frame_interval_sec * 1000, blit=True
                    )
                )

                self.anim_scopes[(row_index, col_index)] = scope

    def signal(self, fn=None, **process_kwargs):
        if fn is None:

            @wraps(fn)
            def wrapper(fn):
                return self.signal(fn, **process_kwargs)

            return wrapper

        process_kwargs["start"] = False
        process_kwargs["args"] = (fn, self.normalize, *process_kwargs.get("args", ()))

        return zproc_ctx.spawn(_signal_process, **process_kwargs)

    def start(self):
        zproc_ctx.start_all()
        plt.show()
        zproc_ctx.wait()

    def stop(self):
        zproc_ctx.stop_all()
        plt.close()
