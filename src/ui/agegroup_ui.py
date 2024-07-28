from PySide6 import QtCore, QtWidgets, QtGui

class AgeGroupUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.header_label = QtWidgets.QLabel(self)

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
        self.table.setColumnCount(3) 
        self.table.setRowCount(6)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.setFixedHeight(self.table.rowCount() * self.table.rowHeight(0) + 2)

        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem("I"))
        self.table.setItem(1, 0, QtWidgets.QTableWidgetItem("II"))
        self.table.setItem(2, 0, QtWidgets.QTableWidgetItem("III"))
        self.table.setItem(3, 0, QtWidgets.QTableWidgetItem("Финиш"))
        self.table.setItem(4, 0, QtWidgets.QTableWidgetItem("В пути"))
        self.table.setItem(5, 0, QtWidgets.QTableWidgetItem("Всего"))

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.header_label)
        layout.addWidget(self.table)







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = AgeGroupUI()
    w.show()
    w.header_label.setText("М 16-29")

    sys.exit(app.exec())