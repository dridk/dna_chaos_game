from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import dnachaos as dc

class MainWindow(QMainWindow):
	def __init__(self, parent = 0):
		super().__init__()
		self.area  = QScrollArea()
		self.label = QLabel()
		self.setCentralWidget(self.area)

		self.showSettings()



	def showSettings(self):
		dialog = dc.SetupDialog()
		dialog.exec()
		pix = dialog.pixmap()
		self.label.setMinimumSize(pix.size())
		self.label.setPixmap(pix)
		self.area.setWidget(self.label)



