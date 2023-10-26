from app_model import Action, Application
from pymmcore_plus import CMMCorePlus
from qtpy.QtCore import QThreadPool

app = Application.get_or_create("napari-micromanager")
app.injection_store.register_provider(CMMCorePlus.instance, CMMCorePlus)


def snap_in_thread(core: CMMCorePlus) -> None:
    if core.isSequenceRunning():
        core.stopSequenceAcquisition()
    QThreadPool.globalInstance().start(core.snap)


ACTIONS: list[Action] = [
    Action(
        id="snap_image",
        title="Snap",
        icon="mdi6.camera_outline",
        callback=snap_in_thread,
    )
]
for action in ACTIONS:
    app.register_action(action)
