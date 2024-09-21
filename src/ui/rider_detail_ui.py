from PySide6 import QtCore, QtWidgets, QtGui

class RiderDetailUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(400, 100)

        self.name_label = QtWidgets.QLabel(self)
        self.birthday_label = QtWidgets.QLabel(self)
        self.phone_number_label = QtWidgets.QLabel(self)
        self.number_label = QtWidgets.QLabel(self)
        self.category_label = QtWidgets.QLabel(self)

        self.name_caption_label = QtWidgets.QLabel("Имя", self)
        self.birthday_caption_label = QtWidgets.QLabel("Дата рождения", self)
        self.phone_number_caption_label = QtWidgets.QLabel("Телефон", self)
        self.number_caption_label = QtWidgets.QLabel("Номер", self)
        self.category_caption_label = QtWidgets.QLabel("Группа", self)
        self.result_caption_label = QtWidgets.QLabel("Результат", self)

        self.result_edit = QtWidgets.QTimeEdit(self)
        self.result_edit.setDisplayFormat("HH:mm:ss.zzz")
        self.result_confirm_button = QtWidgets.QPushButton("Подтвердить", self)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.name_caption_label, 0, 0)
        layout.addWidget(self.birthday_caption_label, 1, 0)
        layout.addWidget(self.phone_number_caption_label, 2, 0)
        layout.addWidget(self.number_caption_label, 3, 0)
        layout.addWidget(self.category_caption_label, 4, 0)
        layout.addWidget(self.result_caption_label, 5, 0)

        layout.addWidget(self.name_label, 0, 1, 1, 2)
        layout.addWidget(self.birthday_label, 1, 1, 1, 2)
        layout.addWidget(self.phone_number_label, 2, 1, 1, 2)
        layout.addWidget(self.number_label, 3, 1, 1, 2)
        layout.addWidget(self.category_label, 4, 1, 1, 2)
        layout.addWidget(self.result_edit, 5, 1)
        layout.addWidget(self.result_confirm_button, 5, 2)
