import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QWidget,
    QGridLayout, QDesktopWidget, QFileDialog, QMainWindow
)
import PyPDF2, spacy

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        self.setWindowTitle("Bank Report")
        self.resize(350, 500)

        path = ""

        # --- Widgets ---
        font = QFont()
        font.setBold(True)
        font.setPointSize(9)

        self.lblInstruction = QLabel("Upload your statement to get a small report")
        self.lblInstruction.setFixedHeight(25)
        self.lblInstruction.setFont(font)

        self.lblIncome = QLabel("Total Income:")
        self.lblIncome.setFixedHeight(20)

        self.lblExpense = QLabel("Total Expense:")
        self.lblExpense.setFixedHeight(20)

        self.lblNet = QLabel("Surplus/Deficet:")
        self.lblNet.setFixedHeight(20)

        self.btnUpload = QPushButton("Upload Statement")
        self.btnUpload.clicked.connect(self.getFilePath)

        self.btnReport = QPushButton("Get Report")
        self.btnReport.clicked.connect(self.getReport)

        # --- Layout ---
        central_widget = QWidget()  # central widget is required for QMainWindow
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        layout.addWidget(self.lblInstruction, 0, 0, 1, 2)  # spans 2 columns
        layout.addWidget(self.lblIncome, 1, 0)
        layout.addWidget(self.lblExpense, 1, 1)
        layout.addWidget(self.lblNet, 1, 2)
        layout.addWidget(self.btnUpload, 2, 0, 1, 3)  # span full row
        layout.addWidget(self.btnReport, 3, 0, 1, 3)

        central_widget.setLayout(layout)

        # --- Center the window on screen ---
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #method to enable user to upload their statement
    def openFileDialog(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Select Bank Statement",
            "",
            "PDF Files (*.pdf)"
        )
        if filePath:
            return filePath
        else:
            return ""

    def getFilePath(self):
        self.path = self.openFileDialog()

    def getReport(self):
        with open(self.path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            contents = ""
            for page in reader.pages:
                contents += page.extract_text()
            nlp = spacy.load("en_core_web_md")
            doc = nlp(contents)
            for ent in doc.ents:
                print(ent.text, "->", ent.label_)

# --- Run the app ---
app = QApplication(sys.argv)
window = UI()
window.show()
sys.exit(app.exec_())