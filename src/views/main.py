from datetime import datetime

from PySide6 import QtCore, QtWidgets, QtGui

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

from ui.main_ui import MainUI
from api.data import event, save_cache, save_json
from api.signal_router import router
from models import Rider

class MainWindow(MainUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        categories = {x.age_group for x in event.riders}
        for age_group, widget in zip(sorted(categories, key=str), self.age_groups):
            widget.set_agegroup(age_group)

        # Load agegroups
        for rider in event.riders: 
            rider.set_age_group(event=event)
            router.rider_finished.emit(rider)

        self.timer_full.halfmarathon = False
        self.timer_half.halfmarathon = True

        self.timer_half.start_button.clicked.connect(self.start_halfmarathon)
        self.timer_full.start_button.clicked.connect(self.start_marathon)
        self.timer_half.start_button.clicked.connect(save_cache)
        self.timer_full.start_button.clicked.connect(save_cache)

        
        self.autobackup_timer = QtCore.QTimer(self)
        self.autobackup_timer.setSingleShot(False)
        self.autobackup_timer.setInterval(1000 * 60 * 5)
        self.autobackup_timer.timeout.connect(save_cache)
        self.autobackup_timer.start()
        
        self.autobackup_json_timer = QtCore.QTimer(self)
        self.autobackup_json_timer.setSingleShot(False)
        self.autobackup_json_timer.setInterval(1000 * 60 * 5)
        self.autobackup_json_timer.timeout.connect(save_json)
        self.autobackup_json_timer.start()

        router.rider_finished.connect(self.log_finish)
        router.rider_finished.connect(save_cache)

        self.log_textedit.setText("\n".join(event.log))

    def log_finish(self, rider:Rider):
        text = f"Финиш: {rider.render_result()} {rider.format_name()}"
        self.log(text)

    def log(self, text:str):
        event.log.append(text)
        self.log_textedit.append(text)
        scrollbar = self.log_textedit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

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
        distance = min(event.routes)
        for rider in event.riders: 
            if rider.distance == distance:
                rider.start_time = t
              
                if not rider.started:
                    router.rider_finished.emit(rider)



