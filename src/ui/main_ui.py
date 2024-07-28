from PySide6 import QtCore, QtWidgets, QtGui

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

from views.timer import RideTimerWidget
from views.riders import RidersWidget
from views.agegroup import AgeGroupWidget
from views.multiadd import MultiAddWidget

class MainUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1280, 700)

        self.riders = RidersWidget(self)
        self.timer_full = RideTimerWidget(self)
        self.timer_half = RideTimerWidget(self)
        self.multiadd = MultiAddWidget(self)

        self.timer_full.header_label.setText("Марафон")
        self.timer_half.header_label.setText("Полумарафон")
        
        self.age_groups = [AgeGroupWidget(self) for _ in range(12)]

        layout = QtWidgets.QGridLayout(self)
        layout.setColumnStretch(0, 10)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 3)
        layout.setColumnStretch(3, 3)
        layout.setColumnStretch(4, 3)
        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)

        layout.addWidget(self.riders, 0, 0, 4, 1)
        layout.addWidget(self.multiadd, 0, 1, 1, 2)
        layout.addWidget(self.timer_full, 0, 3)
        layout.addWidget(self.timer_half, 0, 4)

        for i, ag in enumerate(self.age_groups):
            layout.addWidget(ag, 1 + i//4, 1 + i%4)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = MainUI()
    w.show()

    sys.exit(app.exec())