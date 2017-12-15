from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys 
import dnachaos


app = QApplication(sys.argv)

m  = dnachaos.MainWindow()
m.show()

app.exec_()