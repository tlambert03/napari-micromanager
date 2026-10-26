# Scripting napari-micromanager

`napari-micromanager` uses the global [`CMMCorePlus.instance()`][pymmcore_plus.CMMCorePlus.instance],
so anything you can do with [pymmcore-plus](../pymmcore-plus/index.md) can be
combined with the GUI.

## Launching napari from a script

For complex scripting you will likely want to launch napari from a script or a
Jupyter notebook:

```python linenums="1" title="examples/launch_from_script.py"
--8<-- "examples/launch_from_script.py"
```

## Using the integrated napari console

After launching napari and starting the `napari-micromanager` plugin, open the
napari console and get a reference to the same core object that the plugin
uses:

```python
from pymmcore_plus import CMMCorePlus

mmc = CMMCorePlus.instance()
```
