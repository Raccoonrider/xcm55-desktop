from PySide6 import QtCore, QtWidgets, QtGui

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

from views.timer import RideTimerWidget
from views.rider_list import RiderListWidget
from views.agegroup import AgeGroupWidget
from views.multiadd import MultiAddWidget

class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1280, 700)

        self.riders = RiderListWidget(self)
        self.timer_full = RideTimerWidget(self)
        self.timer_half = RideTimerWidget(self)
        self.multiadd = MultiAddWidget(self)
        self.log_textedit = QtWidgets.QTextEdit(self)
        self.log_textedit.setReadOnly(True)
        self.age_groups = [AgeGroupWidget(self) for _ in range(12)]

        self.timer_full.header_label.setText("Марафон")
        self.timer_half.header_label.setText("Полумарафон")

        self.tabwidget = QtWidgets.QTabWidget(self)
        self.setCentralWidget(self.tabwidget)

        self.main_tab = QtWidgets.QWidget(self)
        self.categories_tab = QtWidgets.QWidget(self)

        self.tabwidget.addTab(self.main_tab, "Главная")
        self.tabwidget.addTab(self.categories_tab, "Категории")

        main_tab_layout = QtWidgets.QGridLayout(self.main_tab)
        main_tab_layout.addWidget(self.riders, 0, 0, 3, 1)
        main_tab_layout.addWidget(self.multiadd, 0, 1, 1, 2)
        main_tab_layout.addWidget(self.timer_full, 1, 1, 1, 1)
        main_tab_layout.addWidget(self.timer_half, 1, 2, 1, 1)
        main_tab_layout.addWidget(self.log_textedit, 2, 1, 1, 2)

        categories_tab_layout = QtWidgets.QGridLayout(self.categories_tab)

        for i, ag in enumerate(self.age_groups):
            categories_tab_layout.addWidget(ag, 1 + i//4, 1 + i%4)
        
        

        # layout = QtWidgets.QGridLayout(self)
        # layout.setColumnStretch(0, 10)
        # layout.setColumnStretch(1, 3)
        # layout.setColumnStretch(2, 3)
        # layout.setColumnStretch(3, 3)
        # layout.setColumnStretch(4, 3)
        # layout.setRowStretch(0, 0)
        # layout.setRowStretch(1, 1)
        # layout.setRowStretch(2, 1)
        # layout.setRowStretch(3, 1)
        # layout.setRowStretch(4, 1)

        # layout.addWidget(self.riders, 0, 0, 4, 1)
        # layout.addWidget(self.multiadd, 0, 1, 1, 2)
        # layout.addWidget(self.timer_full, 0, 3)
        # layout.addWidget(self.timer_half, 0, 4)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = MainUI()
    w.show()

    sys.exit(app.exec())