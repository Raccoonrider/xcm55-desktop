from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

from api.data import event
from api.signal_router import router
from ui.agegroup_ui import AgeGroupUI
from views.rider_detail import RiderDetailWidget
from models import Rider, Event, AgeGroup
from enums import *
import config

class AgeGroupWidget(AgeGroupUI):
    results: list[Rider]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.age_group = None
        self.results = []
        self.rider_windows = []

        self.table.doubleClicked.connect(self.table_double_clicked)
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
            if rider.started:
                for result in self.results:
                    if rider.number == result.number and rider.last_name == result.last_name:
                        self.results.remove(result)
                        self.results.append(rider)
                        break
                else:
                    self.results.append(rider)

                self.results.sort(key=Rider.sort_key)
                for place, rider in enumerate(self.results, start=1):
                    rider.place = place
                    router.rider_place.emit(rider)

            self.update_table()

    def update_table(self):
        self.table.setRowCount(len(self.results))
        row = 0
        for rider in self.results:
            self.table.setItem(row, 0,
                QtWidgets.QTableWidgetItem(str(rider.number)))
            self.table.setItem(row, 1, 
                QtWidgets.QTableWidgetItem(rider.format_name()))
            self.table.setItem(row, 2, 
                QtWidgets.QTableWidgetItem(rider.render_result()))
            row += 1

        finished = len(self.results)
        total = sum(1 for rider in event.riders if rider.age_group == self.age_group and rider.started)
        en_route = total - finished

        self.en_route_label.setText(str(en_route))
        self.total_label.setText(str(total))
        self.finished_label.setText(str(finished))


    def table_double_clicked(self, index):
        rider = self.results[index.row()]

        rider_window = RiderDetailWidget()
        rider_window.set_data(rider)
        rider_window.show()

        self.rider_windows.append(rider_window)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = AgeGroupWidget()
    w.show()
    w.header_label.setText("М 16-29")

    sys.exit(app.exec())