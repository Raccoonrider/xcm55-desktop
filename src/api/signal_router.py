from PySide6 import QtCore

from models import Rider, AgeGroup, Event

class Router(QtCore.QObject):
    rider_added = QtCore.Signal(Rider)
    rider_finished = QtCore.Signal(Rider)
    rider_place = QtCore.Signal(Rider)


router = Router()