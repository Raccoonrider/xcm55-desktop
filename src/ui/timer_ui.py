from PySide6 import QtCore, QtWidgets, QtGui

class RideTimerUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.header_label = QtWidgets.QLabel("Марафон", self)
        self.time_label = QtWidgets.QLabel(self)
        self.start_button = QtWidgets.QPushButton("Старт", self)
        self.reset_button = QtWidgets.QPushButton("Сброс", self)

        self.header_label.setStyleSheet("""
            font-weight: bold;
            font-size: 18px; 
            qproperty-alignment: AlignCenter;                  
        """
        )
        self.time_label.setStyleSheet(
        """
            font-weight: bold;
            font-size: 48px; 
            background-color: #000;
            color: #00FF00;    
            qproperty-alignment: AlignCenter;      
            padding: 0.3em;                 

        """
        )
        self.start_button.setStyleSheet(
        """
            font-weight: bold;
            font-size: 18px;           
        """
        )
        self.reset_button.setStyleSheet(
        """
            font-weight: bold;
            font-size: 18px;           
        """
        )

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.reset_button)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.header_label)
        layout.addWidget(self.time_label)
        layout.addLayout(buttons_layout)
        layout.setStretch(1, 1)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = RideTimerUI()
    w.show()
    w.time_label.setText("01:55:48")

    sys.exit(app.exec())