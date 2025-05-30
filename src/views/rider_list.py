from PySide6 import QtCore, QtWidgets, QtGui

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

from api.data import event
from api.signal_router import router
from ui.rider_list_ui import RiderListUI
from views.rider_detail import RiderDetailWidget
from models import Rider, Event, AgeGroup
from enums import *

class RiderListWidget(RiderListUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        for rider in event.riders:
            self.add_rider(rider=rider)

        self.add_button.clicked.connect(self.add_rider)
        router.rider_finished.connect(self.update_rider)
        router.rider_place.connect(self.update_rider_place)
        self.table.doubleClicked.connect(self.table_double_clicked)

        self.rider_windows = []


    def add_rider(self, *args, rider:Rider|None=None):
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)

        if rider is None:
            rider = Rider(
                number=int(self.number_edit.text()),
                first_name=self.first_name_edit.text().capitalize(),
                last_name=self.last_name_edit.text().capitalize(),
                gender=[Gender.M, Gender.F][self.female_checkbox.isChecked()],
                birthday=self.birthday_edit.date().toPython(),
                distance=(30,60)[self.marathon_radio.isChecked()],
                started=True,
                payment_confirmed=True,
                helmet_not_needed=True,
            )
            event.riders.append(rider)
            rider.set_age_group(event)
            self.clear_inputs()

        router.rider_added.emit(rider)
           
        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem("{:03d}".format(rider.number or 999)))
        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(rider.format_name())))

        started_checkbox = QtWidgets.QCheckBox(self)
        started_checkbox.setChecked(rider.started)
        started_checkbox.stateChanged.connect(rider.started_state_changed)
        self.table.setCellWidget(row, 2, started_checkbox)

        payment_confirmed_checkbox = QtWidgets.QCheckBox(self)
        payment_confirmed_checkbox.setChecked(rider.payment_confirmed)
        payment_confirmed_checkbox.stateChanged.connect(rider.payment_confirmed_state_changed)
        self.table.setCellWidget(row, 3, payment_confirmed_checkbox)

        helmet_not_needed_checkbox = QtWidgets.QCheckBox(self)
        helmet_not_needed_checkbox.setChecked(rider.helmet_not_needed)
        helmet_not_needed_checkbox.stateChanged.connect(rider.helmet_not_needed_state_changed)
        self.table.setCellWidget(row, 4, helmet_not_needed_checkbox)
        
        self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(rider.distance)))
        self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(rider.age_group)))
        self.table.setItem(row, 7, QtWidgets.QTableWidgetItem("{:02d}".format(rider.place) if rider.place else ''))
        self.table.setItem(row, 8, QtWidgets.QTableWidgetItem(rider.render_result()))

        finish_button = QtWidgets.QPushButton("Финиш", self)
        finish_button.clicked.connect(rider.finish)
        finish_button.clicked.connect(self.get_update_result_slot(rider))
        self.table.setCellWidget(row, 9, finish_button)

        dnf_button = QtWidgets.QPushButton("DNF", self)
        dnf_button.clicked.connect(rider.did_not_finish)
        dnf_button.clicked.connect(self.get_update_result_slot(rider))
        dnf_button.setFixedWidth(dnf_button.height())
        self.table.setCellWidget(row, 10, dnf_button)

        dsq_button = QtWidgets.QPushButton("DSQ", self)
        dsq_button.clicked.connect(rider.disqualify)
        dsq_button.clicked.connect(self.get_update_result_slot(rider))
        dsq_button.setFixedWidth(dsq_button.height())
        self.table.setCellWidget(row, 11, dsq_button)

        cancel_finish_button = QtWidgets.QPushButton("Отмена", self)
        cancel_finish_button.clicked.connect(rider.cancel_finish)
        cancel_finish_button.clicked.connect(self.get_update_result_slot(rider))
        self.table.setCellWidget(row, 12, cancel_finish_button)

        # for col in range(15):
        #     item = self.table.item(row, col)
        #     if item is None:
        #         item = QtWidgets.QTableWidgetItem("")
        #         self.table.setItem(row, col, item)

        #     if isinstance(rider.age_group, AgeGroup) and rider.age_group.age_max == 29:
        #         item.setBackground(QtGui.QColor("#BAFFBC"))
        #     if isinstance(rider.age_group, AgeGroup) and rider.age_group.age_max == 34:
        #         item.setBackground(QtGui.QColor("#FFF9BA"))
        #     if isinstance(rider.age_group, AgeGroup) and rider.age_group.age_max == 39:
        #         item.setBackground(QtGui.QColor("#D6DBFF"))
        #     if isinstance(rider.age_group, AgeGroup) and rider.age_group.age_max == 44:
        #         item.setBackground(QtGui.QColor("#A3FFFF"))
        #     if isinstance(rider.age_group, AgeGroup) and rider.age_group.age_max == 49:
        #         item.setBackground(QtGui.QColor("#FFD7A3"))
        #     if isinstance(rider.age_group, AgeGroup) and rider.age_group.age_max == 100:
        #         item.setBackground(QtGui.QColor("#BFBFBF"))
        #     if isinstance(rider.age_group, AgeGroup) and rider.age_group.gender == Gender.F:
        #         item.setBackground(QtGui.QColor("#FFBFF3"))

        #     if rider.age_group == "Элита":
        #         item.setBackground(QtGui.QColor("#FFB5B5"))



    def table_double_clicked(self, index):
        row = index.row()
        cell = self.table.item(row, 0)
        number = int(cell.text().lstrip('0'))

        for rider in event.riders:
            if rider.number == number:
                rider_window = RiderDetailWidget()
                rider_window.set_data(rider)
                rider_window.show()
                self.rider_windows.append(rider_window)
                return


    def get_update_result_slot(self, rider:Rider):
        def wrapper():
            def update_result():
                router.rider_finished.emit(rider)
            QtCore.QTimer.singleShot(50, self, update_result)

        return wrapper
    
    @QtCore.Slot(Rider)
    def update_rider(self, rider:Rider):
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() ==  "{:03d}".format(rider.number):
                result_item = self.table.item(row, 8)
                result_item.setText(str(rider.render_result()))
                
    @QtCore.Slot(Rider)
    def update_rider_place(self, rider:Rider):
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() ==  "{:03d}".format(rider.number):
                place_item = self.table.item(row, 7)
                place_item.setText("{:02d}".format(rider.place))


    def clear_inputs(self):
        self.number_edit.clear()
        self.last_name_edit.clear()
        self.first_name_edit.clear()
        self.birthday_edit.setDate(QtCore.QDate(2000, 1, 1))

        self.female_checkbox.setChecked(False)
        self.marathon_radio.setChecked(True)





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    from api.data import event

    w = RiderListWidget()
    w.show()

    sys.exit(app.exec())