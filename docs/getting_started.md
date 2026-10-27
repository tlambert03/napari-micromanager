# Installing and Launching napari-micromanager

## Installation

### Installing napari-micromanager

```sh
pip install "napari-micromanager[PyQt6]"
# or, for the PySide6 Qt backend: pip install "napari-micromanager[PySide6]"
```

(The quotes keep zsh, the default shell on macOS, from complaining about the square
brackets.)  If you've already installed napari with a Qt backend in this environment
(e.g. `pip install "napari[all]"`), plain `pip install napari-micromanager` is enough.

You will then also need to grab the Micro-Manager device adapters:

```sh
mmcore install
```

See [Installing Micro-Manager device adapters](../pymmcore-plus/install.md#installing-micro-manager-device-adapters)
for details on the `mmcore` helper command.

## Usage

```sh
napari-micromanager
```

This will open a new napari window with the micromanager plugin enabled.  To load a
configuration file right away, pass it with `-c`:

```sh
napari-micromanager -c path/to/config.cfg
napari-micromanager -c MMConfig_demo.cfg  # Micro-Manager's demo devices
```

Otherwise, select a MM Config file at the top left of the window, then click load.
(You can also add the plugin to a napari window that's already open, from the
**Plugins** menu, or start napari with it: `napari -w napari-micromanager`.)

The plugin adds a row of toolbars along the top of the napari window: the
configuration file, the channel group and channel, the objective, the shutters, Snap
and Live, and the exposure time.  The buttons at the end of the row open more panels,
docked in the napari window: the device property browser, configuration groups and
presets, illumination, stage control, camera ROI, pixel size, and **MDA** for
multi-dimensional acquisitions.  Snapped and live images go to a napari layer called
"preview", and each acquisition gets layers of its own, so you can use any napari tool
or plugin on them.  A **MinMax** panel shows the minimum and maximum pixel values of
the layers.  Then ... much of the rest is hopefully self explanatory :smile:.

Underlying napari-micromanager is the `pymmcore-plus` package, which is a
python wrapper around `pymmcore` and the C++ CMMCore library (*not*
pycro-manager and not the Java-based MMStudio).  See the [User Guide](../guide/index.md) for
more on `pymmcore-plus`; the widgets in the GUI are all powered by
[`pymmcore-widgets`](../pymmcore-widgets/widgets/index.md).
