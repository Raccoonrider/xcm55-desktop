from datetime import time, timedelta
from PySide6 import QtCore, QtWidgets, QtGui

from ui.rider_detail_ui import RiderDetailUI
from models import Rider, AgeGroup
from api.signal_router import router


class RiderDetailWidget(RiderDetailUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        router.rider_finished.connect(self.set_data)
        self.result_confirm_button.clicked.connect(self.confirm_finish)

    @QtCore.Slot(Rider)
    def update_rider(self, rider:Rider):
        if rider.number == self.rider.number:
            self.set_data(rider)

    def set_data(self, rider:Rider):
        self.rider = rider

        self.setWindowTitle(rider.format_surname_number())
        self.name_label.setText(rider.format_name())
        self.birthday_label.setText(rider.birthday.strftime("%d.%m.%Y"))
        self.number_label.setText(str(rider.number))
        self.category_label.setText(str(rider.age_group))
        self.phone_number_label.setText(rider.phone_number)


        if rider.result:
            s = rider.result.total_seconds()
            s, ms = divmod(s, 1)
            ms = int(1000 * ms)
            m, s = divmod(s, 60)
            h, m = divmod(m, 60)

            t = QtCore.QTime(h, m, s, ms)

            self.result_edit.setTime(t)

    def confirm_finish(self):
        t = self.result_edit.time()
        dt = timedelta(
            hours = t.hour(), 
            minutes=t.minute(), 
            seconds=t.second(), 
            milliseconds=t.msec()
        )

        self.rider.finish_time = self.rider.start_time + dt
        router.rider_finished.emit(self.rider)
