import matplotlib.pyplot as plt
import matplotlib_inline

matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
config = {
    "font.family": ["Times New Roman", "SimSun"],
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
    "svg.fonttype": "none",
    "font.size": 7.5,
    "lines.linewidth": 0.75,
}
plt.rcParams.update(config)


def cm(*args):
    return tuple(x / 2.54 for x in args)
