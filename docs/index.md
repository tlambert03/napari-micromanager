# napari-micromanager

`napari-micromanager` is a [napari](https://napari.org) plugin that turns napari
into a microscope control application, powered by
[pymmcore-plus](../pymmcore-plus/index.md) and
[pymmcore-widgets](../pymmcore-widgets/index.md).  Images you snap or acquire show up
as napari layers, right next to whatever analysis you do in napari.

!!! note "Development has moved to pymmcore-gui"

    `napari-micromanager` continues to be maintained, but current development is
    focused on [pymmcore-gui](../pymmcore-gui/index.md), a napari-independent
    application (using [ndv](https://github.com/pyapp-kit/ndv) for viewing),
    for reasons of performance and fewer dependencies.  If you don't need napari,
    start with pymmcore-gui.

![napari-micromanager](https://github.com/pymmcore-plus/napari-micromanager/assets/1609449/e1f395cd-2d57-488e-89e2-b1923310fc2a){ loading=lazy }

- [Installing and launching](getting_started.md) the plugin.
- [Scripting](scripting.md): drive napari-micromanager from Python.
