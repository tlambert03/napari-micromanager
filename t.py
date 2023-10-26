from qtpy.QtWidgets import QApplication, QComboBox, QMainWindow, QWidget, QWidgetAction

app = QApplication([])


class MyWidgetAction(QWidgetAction):
    def __init__(self, parent=None):
        super().__init__(parent)
        cb = QComboBox()
        cb.addItems(["a", "b", "c"])
        self.setDefaultWidget(cb)

    def requestWidget(self, parent: QWidget | None) -> QWidget | None:
        print("requestWidget", parent)


main = QMainWindow()
tb = main.addToolBar("test")
tb2 = main.addToolBar("test2")
a = MyWidgetAction(None)
print("1")
tb.addAction(a)
print("2")
tb2.addAction(a)
print(a.requestWidget(None))

main.show()
app.exec_()
