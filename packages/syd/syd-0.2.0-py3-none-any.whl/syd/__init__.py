from typing import Callable, Optional
from .viewer import Viewer

__version__ = "0.2.0"


def make_viewer(plot_func: Optional[Callable] = None):
    viewer = Viewer()
    if plot_func is not None:
        viewer.set_plot(plot_func)
    return viewer
