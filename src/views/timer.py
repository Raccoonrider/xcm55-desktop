from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

from ui.timer_ui import RideTimerUI
from api.data import event

class RideTimerWidget(RideTimerUI):
    start_time:datetime

    def __init__(self, parent=None):
        super().__init__(parent)
        self.halfmarathon = False
        self.start_button.clicked.connect(self.start)
        self.reset_button.clicked.connect(self.reset)

        self.refresh_timer = QtCore.QTimer(self)
        self.refresh_timer.setSingleShot(False)
        self.refresh_timer.setInterval(100)
        self.refresh_timer.timeout.connect(self.refresh_time)
        self.refresh_timer.start()

    def start(self):
        self.start_button.setEnabled(False)

        if self.halfmarathon:
            event.halfmarathon_start_time = datetime.now()
            distance = min(event.routes)

            for rider in event.riders: 
                if rider.distance == distance:
                    rider.start_time = event.halfmarathon_start_time
        else:
            event.marathon_start_time = datetime.now()
            distance = max(event.routes)

            for rider in event.riders: 
                if rider.distance == distance:
                    rider.start_time = event.marathon_start_time

        
    def reset(self):
        if self.halfmarathon:
            event.halfmarathon_start_time = None
            distance = min(event.routes)
        else:
            event.marathon_start_time = None
            distance = max(event.routes)

        for rider in event.riders: 
            if rider.distance == distance:
                rider.start_time = None

        self.start_button.setEnabled(True)


    def refresh_time(self):
        if self.halfmarathon:
            if event.halfmarathon_start_time is None:
                self.time_label.setText("--:--:--")
                return
            t = round((datetime.now() - event.halfmarathon_start_time).total_seconds())

        else:
            if event.marathon_start_time is None:
                self.time_label.setText("--:--:--")
                return
            t = round((datetime.now() - event.marathon_start_time).total_seconds())


        h, t = divmod(t, 3600)
        m, s = divmod(t, 60)

        self.time_label.setText(F"{h:02d}:{m:02d}:{s:02d}")    