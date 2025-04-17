from .new_visuals import _NewVisuals

def _init_visuals():
    global new_plots
    new_plots = _NewVisuals()


_init_visuals()