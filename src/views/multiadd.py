from datetime import datetime
import re

from PySide6 import QtCore, QtWidgets, QtGui

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

from ui.multiadd_ui import MultiAddUI
from api.signal_router import router
from api.data import event


class MultiAddWidget(MultiAddUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pattern = re.compile(f"\d+")
        self.finish_button.clicked.connect(self.finish)
        self.dnf_button.clicked.connect(self.dnf)
        self.dsq_button.clicked.connect(self.dsq)

        self.clear_status_timer = QtCore.QTimer(self)
        self.clear_status_timer.setSingleShot(True)
        self.clear_status_timer.setInterval(6000)
        self.clear_status_timer.timeout.connect(self.status_label.clear)
        self.text_edit.installEventFilter(self)

    def eventFilter(self, obj, event):
        if (isinstance(event, QtGui.QKeyEvent)
            and event.type() == QtCore.QEvent.Type.KeyRelease
            and obj is self.text_edit
            and self.text_edit.hasFocus()
            and self.text_edit.toPlainText() != ""
        ):
            if (event.key() in [QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter]):
                self.finish()
        return super().eventFilter(obj, event)


    def parse(self):
        strings = self.pattern.findall(self.text_edit.toPlainText())
        numbers = [int(s.lstrip('0')) for s in strings]
        riders = [x for x in event.riders if x.number in numbers]
        QtCore.QTimer.singleShot(500, self, self.text_edit.clear)

        return riders


    def finish(self):
        riders = self.parse()
        t = datetime.now()

        for rider in riders:
            rider.finish()
            router.rider_finished.emit(rider)
            
        message = "Зафиксированы: " + ", ".join([x.format_surname_number() for x in riders])
        self.send_status(message)

    def dnf(self):
        riders = self.parse()

        for rider in riders:
            rider.did_not_finish()
            router.rider_finished.emit(rider)

        message = "DNF: " + ", ".join([x.format_surname_number() for x in riders])
        self.send_status(message)


    def dsq(self):
        riders = self.parse()

        for rider in riders:
            rider.disqualify()
            router.rider_finished.emit(rider)

        message = "DSQ: " + ", ".join([x.format_surname_number() for x in riders])
        self.send_status(message)
        
        
    def send_status(self, status:str):
        self.status_label.setText(status)
        self.clear_status_timer.stop()
        self.clear_status_timer.setInterval(5000)
        self.clear_status_timer.timeout.connect(self.status_label.clear)
        self.clear_status_timer.start()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = MultiAddWidget()
    w.show()

    sys.exit(app.exec())