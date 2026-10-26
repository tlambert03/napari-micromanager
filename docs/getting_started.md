# Getting Started

## Installation

### Installing napari-micromanager

```sh
pip install napari-micromanager PyQt6
# you may also pick PySide6 for your Qt backend
```

You will then also need to grab the `Micro-Manager` device adapters

```sh
mmcore install
```

See [Installing Micro-Manager device adapters](../pymmcore-plus/install.md#installing-micro-manager-device-adapters) for details on the `mmcore` helper command.

## Usage

```sh
napari-micromanager
```

This will open a new napari window with the micromanager plugin enabled.

Select a MM Config file at the top left of the window, then click load.

Then ... much of the rest is hopefully self explanatory :smile:.

Underlying napari-micro-manager is the `pymmcore-plus` package, which is a
python wrapper around `pymmcore` and the C++ CMMCore library (*not*
pycro-manager and not the Java-based MMStudio).  See the [User Guide](../guide/index.md) for
more on `pymmcore-plus`; the widgets in the GUI are all powered by
[`pymmcore-widgets`](../pymmcore-widgets/widgets/index.md).
