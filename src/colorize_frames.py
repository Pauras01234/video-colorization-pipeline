from pathlib import Path
import torch
import collections
import collections.abc

# Python 3.11 compatibility patch for old fastai
collections.Sized = collections.abc.Sized
collections.Iterable = collections.abc.Iterable
collections.Container = collections.abc.Container
collections.Callable = collections.abc.Callable

# PyTorch 2.6+ compatibility patch
_original_torch_load = torch.load

def patched_torch_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return _original_torch_load(*args, **kwargs)

torch.load = patched_torch_load

from deoldify.visualize import get_image_colorizer

_colorizer = None


def get_colorizer():
    global _colorizer
    if _colorizer is None:
        print("Loading DeOldify model...")
        _colorizer = get_image_colorizer(artistic=True)
    return _colorizer


def colorize_frames(input_dir: str, output_dir: str):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    colorizer = get_colorizer()

    frames = sorted(input_path.glob("*.png"))

    for frame in frames:
        colorizer.plot_transformed_image(
            path=str(frame),
            render_factor=35,
            results_dir=output_path,
            display_render_factor=False
        )