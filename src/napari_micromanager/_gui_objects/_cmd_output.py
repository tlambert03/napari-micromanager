import subprocess
import sys

from qtpy.QtCore import QThread, Signal
from qtpy.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class CommandRunner(QThread):
    output_received = Signal(str)
    process_finished = Signal(int)

    def __init__(self, cmd: list[str]) -> None:
        super().__init__()
        self.cmd = cmd
        self.process = None

    def run(self) -> None:
        self.process = subprocess.Popen(
            self.cmd,  # noqa: S603
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )
        for line in self.process.stdout:
            self.output_received.emit(line)
        self.process_finished.emit(self.process.returncode)

    def stop(self) -> None:
        if self.process:
            self.process.terminate()


class CommandOutputWidget(QWidget):
    def __init__(self, cmd: list[str]) -> None:
        super().__init__()
        self.cmd = cmd

        self.text_edit = QLabel(self)
        self.run_button = QPushButton("Run Command", self)
        self.run_button.clicked.connect(self.run_command)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_command)

        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.run_button)
        layout.addWidget(self.cancel_button)

        self.runner: CommandRunner | None = None

    def run_command(self) -> None:
        self.run_button.setEnabled(False)
        self.run_button.setText("Running...")

        self.runner = CommandRunner(self.cmd)
        self.runner.output_received.connect(self.display_output)
        self.runner.process_finished.connect(self._on_command_finished)
        self.runner.start()

    def cancel_command(self) -> None:
        if isinstance(self.runner, CommandRunner):
            self.runner.stop()

    def display_output(self, text: str) -> None:
        self.text_edit.setText(text)

    def _on_command_finished(self, returncode: int) -> None:
        # Re-enable the run button when the command is finished
        self.run_button.setText("Run Command")
        self.run_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CommandOutputWidget(["mmcore", "install", "--plain-output"])
    window.show()
    sys.exit(app.exec())
