from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

from api.data import event
from api.signal_router import router
from ui.agegroup_ui import AgeGroupUI
from models import Rider, Event, AgeGroup
from enums import *
import config

class AgeGroupWidget(AgeGroupUI):
    results: list[Rider]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.age_group = None
        self.results = []

        router.rider_finished.connect(self.rider_finished)
        router.rider_added.connect(self.rider_added)

    def set_agegroup(self, age_group: AgeGroup|str):
        self.age_group = age_group
        self.header_label.setText(str(age_group))

    @QtCore.Slot(Rider)
    def rider_added(self, rider:Rider):
        if rider.age_group == self.age_group:
            if rider not in self.riders:
                self.riders.append(rider)

    @QtCore.Slot(Rider)
    def rider_finished(self, rider:Rider):
        if rider.age_group == self.age_group:
            if rider.started and rider.finish_time:
                for result in self.results:
                    if rider.number == result.number and rider.last_name == result.last_name:
                        self.results.remove(result)
                        self.results.append(rider)
                        break
                else:
                    self.results.append(rider)

                self.results.sort(key=lambda x: x.finish_time)
                rider.place = self.results.index(rider) + 1
                router.rider_place.emit(rider)

            self.update_table()

    def update_table(self):
        row = 0
        for rider in self.results:

            if (rider.dnf == False 
                and rider.dsq == False
                and rider.started 
                and rider.start_time
                and rider.finish_time
                and row < 3):

                self.table.setItem(row, 1, 
                    QtWidgets.QTableWidgetItem(rider.format_surname_number()))
                self.table.setItem(row, 2, 
                    QtWidgets.QTableWidgetItem(rider.render_result()))
                row += 1

        self.table.setItem(3, 2, 
            QtWidgets.QTableWidgetItem(str(len(self.results))))

        total = sum(1 for rider in event.riders if rider.age_group == self.age_group and rider.started)

        self.table.setItem(4, 2, 
            QtWidgets.QTableWidgetItem(str(total - len(self.results))))
        
        self.table.setItem(5, 2, 
            QtWidgets.QTableWidgetItem(str(total)))
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = AgeGroupWidget()
    w.show()
    w.header_label.setText("М 16-29")

    sys.exit(app.exec())