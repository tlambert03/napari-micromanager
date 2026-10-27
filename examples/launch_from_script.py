import napari

v = napari.Viewer()
dw, main_window = v.window.add_plugin_dock_widget("napari-micromanager")

# the CMMCorePlus instance that napari-micromanager is driving
mmc = main_window.core

# do any complicated scripting you want here
...

# start napari
napari.run()
