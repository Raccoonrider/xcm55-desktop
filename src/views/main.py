from datetime import datetime

from PySide6 import QtCore, QtWidgets, QtGui

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

from ui.main_ui import MainUI
from api.data import event, save_cache, save_json
from api.signal_router import router

class MainWindow(MainUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        categories = {x.age_group for x in event.riders}
        for age_group, widget in zip(sorted(categories, key=str), self.age_groups):
            widget.set_agegroup(age_group)

        self.timer_full.halfmarathon = False
        self.timer_half.halfmarathon = True

        self.timer_half.start_button.clicked.connect(self.start_halfmarathon)
        self.timer_full.start_button.clicked.connect(self.start_marathon)

        self.autobackup_timer = QtCore.QTimer(self)
        self.autobackup_timer.setSingleShot(False)
        self.autobackup_timer.setInterval(1000)#1000 * 60 * 5)
        self.autobackup_timer.timeout.connect(save_cache)
        self.autobackup_timer.start()

        router.rider_finished.connect(save_json)
        router.rider_place.connect(save_json)


    
    def start_marathon(self):
        t = datetime.now()
        distance = max(event.routes)
        for rider in event.riders: 
            if rider.distance == distance:
                rider.start_time = t

                if not rider.started:
                    router.rider_finished.emit(rider)
    
    def start_halfmarathon(self):
        t = datetime.now()
        distance = max(event.routes)
        for rider in event.riders: 
            if rider.distance == distance:
                rider.start_time = t
              
                if not rider.started:
                    router.rider_finished.emit(rider)



