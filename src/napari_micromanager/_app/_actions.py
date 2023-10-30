from app_model import Action, Application
from pymmcore_plus import CMMCorePlus
from qtpy.QtCore import QThreadPool

app = Application.get_or_create("napari-micromanager")
app.injection_store.register_provider(CMMCorePlus.instance, CMMCorePlus)


def snap_in_thread(core: CMMCorePlus) -> None:
    if core.isSequenceRunning():
        core.stopSequenceAcquisition()
    QThreadPool.globalInstance().start(core.snap)


def toggle_live(core: CMMCorePlus) -> None:
    if core.isSequenceRunning():
        core.stopSequenceAcquisition()
    else:
        core.startContinuousSequenceAcquisition()


ACTIONS: list[Action] = [
    Action(
        id="snap_image",
        title="Snap",
        icon="mdi6.camera_outline",
        callback=snap_in_thread,
    ),
    Action(
        id="toggle_live",
        title="Live",
        icon="mdi6.video",
        callback=toggle_live,
        toggled=True,
    ),
]
for action in ACTIONS:
    app.register_action(action)
