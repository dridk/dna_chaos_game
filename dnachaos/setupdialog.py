from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Bio import SeqIO


class ComputePixmap(QThread):

    progressChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.pix = QPixmap()

    def setParams(self,size, file):
        self.size = size
        self.fasta = file 


    # @override 
    def run(self):
        self.pix  = QPixmap(self.size, self.size)
        self.pix.fill(Qt.white)

        vertexes = {"A": QPointF(0.0,0.0), 
                    "C": QPointF(0.0,self.size), 
                    "T": QPointF(self.size,0.0),
                    "G": QPointF(self.size,self.size),
                    "N": QPointF(self.size/2,self.size/2)}

        record = next(SeqIO.parse(self.fasta, "fasta"))
        p = QPointF(self.size/2, self.size/2)
        painter = QPainter()
        painter.begin(self.pix)
        pen = QPen()
        pen.setWidth(1)
        pen.setColor(Qt.black)
        painter.setPen(pen)
        index = 0
        for base in record.seq:
            v = vertexes[base.upper()]
            p = (v-p)/2
            p.setX(abs(p.x()))
            p.setY(abs(p.y()))

            painter.drawPoint(p)
            self.progressChanged.emit(index/len(record.seq)*100)
            index+=1
        painter.end()


class SetupDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.size_box = QSpinBox()
        self.algo_box = QComboBox()
        self.size_box.setRange(100,5000)
        self.progress = QProgressBar()
        self.pixmap_thread = ComputePixmap()
        self.fasta_input          = QLineEdit()
        self.fasta_input.setText("test.fasta")
        fasta_browse_button  =  QPushButton("Browse")
        button_box = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.fasta_input)
        input_layout.addWidget(fasta_browse_button)
        input_layout.setContentsMargins(0,0,0,0)

        form_layout          = QFormLayout()
        form_layout.addRow("size", self.size_box)
        form_layout.addRow("algo", self.algo_box)
        form_layout.addRow("input", input_layout)
        form_layout.addWidget(self.progress)


        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

        fasta_browse_button.clicked.connect(self.browse_fasta)
        button_box.accepted.connect(self.run_thread)
        self.pixmap_thread.progressChanged.connect(self.progress.setValue)

        self.pixmap_thread.finished.connect(self.finished)




    def browse_fasta(self):
        filename = QFileDialog.getOpenFileName(self,"Open fasta file","","Fasta (*.fasta *.fa)")
        print(filename)
        self.fasta_input.setText(filename[0])

    def run_thread(self):
        print("run")
        self.pixmap_thread.setParams(size = self.size_box.value(), file = self.fasta_input.text())
        self.pixmap_thread.start()

    def pixmap(self):
        return self.pixmap_thread.pix


    def finished(self):
        print("done")
        self.close()
       





