"""This module has napari-micromanager as a standalone app.

It directly modifies the napari experience, and is not intended as a plugin.
"""
from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

import napari
import pymmcore_widgets as mmcw
from pymmcore_plus import CMMCorePlus
from pymmcore_widgets import InstallWidget
from pymmcore_widgets.hcwizard import ConfigWizard
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QMenu,
    QPushButton,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from .._gui_objects import _toolbar as tb

if TYPE_CHECKING:
    from qtpy.QtWidgets import QMainWindow, QMenuBar


def _recenter(widget: QWidget) -> None:
    if screen := QApplication.primaryScreen():
        screenGeometry = screen.geometry()
        x = (screenGeometry.width() - widget.width()) // 2
        y = (screenGeometry.height() - widget.height()) // 2
        widget.move(x, y)


class MMInstallDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._main = InstallWidget(self)
        self._close = QPushButton("Close", self)
        self._close.clicked.connect(self.close)

        layout = QVBoxLayout(self)
        layout.addWidget(self._main)
        layout.addWidget(self._close)


class DeviceMenu(QMenu):
    """MM Device menu."""

    def __init__(self, mmcore: CMMCorePlus, parent: QWidget | None = None) -> None:
        self._mmcore = mmcore
        super().__init__("Devices", parent=parent)
        self._act_prop_browser = self.addAction("Device Property Browser...")
        self._act_calibrate_pix = self.addAction("Pixel Size Calibration...")
        self.addSeparator()
        self._act_hcwizard = self.addAction("Hardware Configuration Wizard...")
        self._act_load_config = self.addAction("Load Hardware Configuration...")
        self._act_reload_config = self.addAction("Reload Hardware Configuration")
        self._act_save_config = self.addAction("Save Hardware Configuration As...")
        self.addSeparator()
        self._act_download_mmlibs = self.addAction("Install Micro-Manager Libraries...")

        self._act_prop_browser.triggered.connect(self._show_prop_browser)
        self._act_hcwizard.triggered.connect(self._show_hc_wizard)
        self._act_load_config.triggered.connect(self._load_config)
        self._act_reload_config.setEnabled(False)
        self._act_reload_config.triggered.connect(self._reload_config)
        self._act_save_config.triggered.connect(self._save_config)
        self._act_calibrate_pix.triggered.connect(self._calibrate_pix)
        self._act_download_mmlibs.triggered.connect(self._download_mmlibs)

    def _show_prop_browser(self) -> None:
        if not hasattr(self, "_prop_browser"):
            self._prop_browser = mmcw.PropertyBrowser(parent=self)
            self._prop_browser.setWindowFlags(Qt.WindowType.Window)
        self._prop_browser.show()
        _recenter(self._prop_browser)

    def _show_hc_wizard(self) -> None:
        ConfigWizard(MMNapari.CONFIG_FILE, core=self._mmcore).exec()

    def _load_config(self) -> None:
        # get .cfg file
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Hardware Configuration", "", "Config Files (*.cfg)"
        )
        if path and os.path.isfile(path):
            MMNapari.CONFIG_FILE = path
            self._mmcore.loadSystemConfiguration(path)
            self._act_reload_config.setEnabled(True)

    def _reload_config(self) -> None:
        if MMNapari.CONFIG_FILE:
            self._mmcore.loadSystemConfiguration(MMNapari.CONFIG_FILE)

    def _save_config(self) -> None:
        # get .cfg file
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Hardware Configuration", "", "Config Files (*.cfg)"
        )
        if path:
            # could use pymmcore_plus microscope model instead ... like MMStudio does
            self._mmcore.saveSystemConfiguration(path)

    def _calibrate_pix(self) -> None:
        mmcw.PixelSizeWidget(mmcore=self._mmcore, parent=self).exec()

    def _download_mmlibs(self) -> None:
        dialog = MMInstallDialog(parent=self)
        dialog.exec()


class ToolMenu(QMenu):
    """MM Tool menu."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Tools", parent=parent)
        self.toolbars: list[QToolBar] = [
            tb.ConfigToolBar(parent),
            tb.ChannelsToolBar(parent),
            tb.ObjectivesToolBar(parent),
            tb.ShuttersToolBar(parent),
            tb.SnapLiveToolBar(parent),
            tb.ExposureToolBar(parent),
            # tb.ToolsToolBar(parent),
        ]
        for item in self.toolbars:
            self.addAction(item.toggleViewAction())


class MMNapari:
    """Wrapper around a napari viewer, with micromanager stuff added."""

    # TODO: use systemConfigurationFile() when available
    CONFIG_FILE: str = ""

    def __init__(self, viewer: napari.Viewer | None = None) -> None:
        self._mmcore = core = CMMCorePlus.instance()
        core.loadSystemConfiguration()
        if viewer is None:
            viewer = napari.Viewer()
        self._napari_viewer = viewer
        self._qmain_window: QMainWindow = self._napari_viewer.window._qt_window

        # Add micromanager menu
        menu_bar = cast("QMenuBar", self._qmain_window.menuBar())
        self._mm_menu = menu_bar.addMenu(DeviceMenu(core, self._qmain_window))
        self._tools = ToolMenu(self._qmain_window)
        for tbar in self._tools.toolbars:
            self._qmain_window.addToolBar(tbar)
            self._qmain_window.update()
            print(self._qmain_window.sizeHint())
            print(self._qmain_window.updateGeometry())
            print(self._qmain_window.width())
            print(self._qmain_window.geometry())

        # append toolbars to windows menu
        wm = (act.menu() for act in menu_bar.actions() if act.text().endswith("Window"))
        if win_menu := cast("QMenu | None", next(wm, None)):
            win_menu.addSeparator()
            win_menu.addMenu(self._tools)


def main() -> None:
    """Create a napari viewer and add the MicroManager plugin to it."""
    _mm_napari = MMNapari()
    napari.run()
