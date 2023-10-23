"""Run napari-micromanager as a script with ``python -m napari_micromanager``."""
from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

import napari
import pymmcore_widgets as mmcw
from pymmcore_plus import CMMCorePlus, install
from pymmcore_widgets.hcwizard import ConfigWizard
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QMenu,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)
from superqt.utils import thread_worker

if TYPE_CHECKING:
    from qtpy.QtWidgets import QMainWindow, QMenuBar, QWidget


def _recenter(widget: QWidget) -> None:
    if screen := QApplication.primaryScreen():
        screenGeometry = screen.geometry()
        x = (screenGeometry.width() - widget.width()) // 2
        y = (screenGeometry.height() - widget.height()) // 2
        widget.move(x, y)


class MMLibDownloader(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.version = QComboBox()
        self.version.addItem("latest")
        if hasattr(install, "_available_versions"):
            self.version.addItems(
                sorted(install._available_versions(), reverse=True)[:40]
            )

        self._buttons = QDialogButtonBox()
        self._buttons.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
        self._install_btn = self._buttons.addButton(
            "Install", QDialogButtonBox.ButtonRole.ApplyRole
        )
        self._install_btn.clicked.connect(self._install)
        self._buttons.rejected.connect(self.reject)
        self._buttons.accepted.connect(self.reject)

        self._progress = QProgressBar()
        self._progress.hide()
        self._message = QLabel()
        self._message.hide()

        layout = QVBoxLayout(self)
        layout.addWidget(self.version)
        layout.addWidget(self._progress)
        layout.addWidget(self._message)
        layout.addWidget(self._buttons)
        _recenter(self)

    def _install(self) -> None:
        self._progress.show()
        self._message.show()

        @thread_worker(start_thread=True, connect={"finished": self._success})
        def doit() -> None:
            install.install(
                report_hook=self._update_bar,
                release=self.version.currentText(),
                log_msg=self._update_msg,
            )
            print("DONE")

        doit()

    def _success(self) -> None:
        self._progress.hide()
        self._message.setText("Done!")
        self._close_btn = self._buttons.addButton(
            "Close", QDialogButtonBox.ButtonRole.AcceptRole
        )

    def _update_msg(self, msg: str) -> None:
        self._message.setText(msg.split("]", 1)[-1].strip())

    def _update_bar(self, count: float, block_size: float, total_size: float) -> None:
        self._progress.setRange(0, int(total_size))
        self._progress.setValue(int(count * block_size))
        if count * block_size >= total_size:
            # set to indeterminate
            self._progress.setRange(0, 0)
        self._progress.update()


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
        self._act_download_mmlibs = self.addAction("Update Micro-Manager Libraries...")

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
        dialog = MMLibDownloader(parent=self)
        dialog.exec()


class MMNapari:
    """Wrapper around a napari viewer, with micromanager stuff added."""

    # TODO: use systemConfigurationFile() when available
    CONFIG_FILE: str = ""

    def __init__(self) -> None:
        self._mmcore = core = CMMCorePlus.instance()
        self._napari_viewer = viewer = napari.Viewer()
        self._qmain_window: QMainWindow = viewer.window._qt_window

        # Add micromanager menu
        menu_bar = cast("QMenuBar", self._qmain_window.menuBar())
        self._mm_menu = menu_bar.addMenu(DeviceMenu(core, self._qmain_window))


def main() -> None:
    """Create a napari viewer and add the MicroManager plugin to it."""
    _mm_napari = MMNapari()
    napari.run()


if __name__ == "__main__":
    main()
