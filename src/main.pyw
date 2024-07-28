import sys
from PySide6 import QtWidgets


from views.main import MainWindow

app = QtWidgets.QApplication(sys.argv)

w = MainWindow()
w.show()

sys.exit(app.exec())