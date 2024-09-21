from PySide6 import QtCore, QtWidgets, QtGui

class RiderListUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.header_label = QtWidgets.QLabel("Участники", self)

        self.header_label.setStyleSheet("""
            font-weight: bold;
            font-size: 18px; 
            qproperty-alignment: AlignCenter;                  
        """
        )

        self.table = QtWidgets.QTableWidget(self)

        self.number_edit = QtWidgets.QLineEdit(self)
        self.last_name_edit = QtWidgets.QLineEdit(self)
        self.first_name_edit = QtWidgets.QLineEdit(self)
        self.birthday_edit = QtWidgets.QDateEdit(self)
        self.female_checkbox = QtWidgets.QCheckBox("Ж", self)

        self.marathon_radio = QtWidgets.QRadioButton("60 км", self)
        self.halfmarathon_radio = QtWidgets.QRadioButton("35 км", self)
        self.add_button = QtWidgets.QPushButton("Добавить", self)

        self.number_edit.setValidator(QtGui.QIntValidator())
        self.first_name_edit.setPlaceholderText("Имя")
        self.last_name_edit.setPlaceholderText("Фамилия")
        self.marathon_radio.setChecked(True)
        self.number_edit.setPlaceholderText("№")

        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.setColumnCount(13) #Прибыл № ФИО Категория Место Результат Финиш DNF DSQ Отмена
        self.table.setHorizontalHeaderLabels(["№", "Участник", "Явка", "Опл", "Шлем", "Дист.", "Категория", "Место", "Результат", "", "", "", ""])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setMinimumSectionSize(15)


        controls_container = QtWidgets.QWidget(self)
        controls_layout = QtWidgets.QHBoxLayout(controls_container)
        controls_layout.addWidget(self.number_edit)
        controls_layout.addWidget(self.last_name_edit)
        controls_layout.addWidget(self.first_name_edit)
        controls_layout.addWidget(self.birthday_edit)
        controls_layout.addWidget(self.female_checkbox)
        controls_layout.addWidget(self.marathon_radio)
        controls_layout.addWidget(self.halfmarathon_radio)
        controls_layout.addWidget(self.add_button)
        

        content_layout = QtWidgets.QVBoxLayout(self)
        content_layout.addWidget(self.header_label)
        content_layout.addWidget(self.table)
        content_layout.addWidget(controls_container)

        controls_container.hide()










if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = RidersUI()
    w.show()

    sys.exit(app.exec())