from PySide6 import QtCore, QtWidgets, QtGui
import config

class AgeGroupUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.header_label = QtWidgets.QLabel(self)
        self.finished_caption_label = QtWidgets.QLabel("Финиш", self)
        self.en_route_caption_label = QtWidgets.QLabel("В пути", self)
        self.total_caption_label = QtWidgets.QLabel("Всего", self)
        self.finished_label = QtWidgets.QLabel(self)
        self.en_route_label = QtWidgets.QLabel(self)
        self.total_label = QtWidgets.QLabel(self)


        self.header_label.setStyleSheet("""
            font-weight: bold;
            font-size: 18px; 
            qproperty-alignment: AlignCenter;                  
        """
        )

        self.table = QtWidgets.QTableWidget(self)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSortingEnabled(False)
        self.table.setColumnCount(3 + config.LAPS_MARATHON - 1) 
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().hide()

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.header_label, 0, 0, 1, 2)
        layout.addWidget(self.table, 1, 0, 1, 2)
        layout.addWidget(self.finished_caption_label, 5, 0)
        layout.addWidget(self.en_route_caption_label, 6, 0)
        layout.addWidget(self.total_caption_label, 7, 0)
        layout.addWidget(self.finished_label, 5, 1)
        layout.addWidget(self.en_route_label, 6, 1)
        layout.addWidget(self.total_label, 7, 1)







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = AgeGroupUI()
    w.show()
    w.header_label.setText("М 16-29")

    sys.exit(app.exec())