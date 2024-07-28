from PySide6 import QtCore, QtWidgets, QtGui

class MultiAddUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.header_label = QtWidgets.QLabel("Добавить несколько результатов", self)
        self.header_label.setStyleSheet("""
            font-weight: bold;
            font-size: 18px; 
            qproperty-alignment: AlignCenter;                  
        """
        )

        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setPlaceholderText("Несколько номеров, разделённых пробелами")
        self.text_edit.setStyleSheet("""
            font-size: 16px;             
        """
        )
        
        self.finish_button = QtWidgets.QPushButton("Финишировали", self)
        self.dnf_button = QtWidgets.QPushButton("DNF", self)
        self.dsq_button = QtWidgets.QPushButton("DSQ", self)

        self.status_label = QtWidgets.QLabel(self)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.finish_button)
        btn_layout.addWidget(self.dnf_button)
        btn_layout.addWidget(self.dsq_button)
        btn_layout.setStretch(0, 1)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.header_label)
        layout.addWidget(self.text_edit)
        layout.addLayout(btn_layout)
        layout.addWidget(self.status_label)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = MultiAddUI()
    w.show()

    sys.exit(app.exec())