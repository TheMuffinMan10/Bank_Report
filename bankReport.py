import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QWidget,
    QGridLayout, QDesktopWidget, QFileDialog, QMainWindow
)
import PyPDF2, spacy
from spacy.matcher import Matcher

class Transaction:
    def __init__(self, date, description, amount, balance=None):
        self.date = date
        self.description = description
        self.amount = amount
        self.balance = balance

    def __repr__(self):
        return f"Transaction(date={self.date}, desc={self.description}, amount={self.amount}, balance={self.balance})"


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
        self.btnReport.setEnabled(False)
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
            self.btnReport.setEnabled(True)
            return filePath
        else:
            return ""

    #method to get file path
    def getFilePath(self):
        self.path = self.openFileDialog()

    #method to generate the report
    def getReport(self):
        with open(self.path, "rb") as file: #allows us to loop through the provided pdf
            reader = PyPDF2.PdfReader(file)
            contents = ""
            
            #print("get all text from pdf")
            #get all text from pdf
            for page in reader.pages:
                contents += page.extract_text()
            #print(contents + "' '")

            #pattern for matcher
            open_bal_pattern = [
                {"LOWER": "opening", "OP": "?"},
                {"LOWER": "balance"},
                {"TEXT": "R", "OP": "?"},
                {"LIKE_NUM": True}
            ]

            #read text for analysis
            nlp = spacy.load("en_core_web_lg")
            matcher = Matcher(nlp.vocab)
            matcher.add("opening balance", [open_bal_pattern])
            doc = nlp(contents)

            matches = matcher(doc)
            for match_id, start, end in matches:
                span = doc[start:end]
                self.lblIncome.setText(f"{span.text} ({nlp.vocab.strings[match_id]})")
                print("machtes:", span.text, nlp.vocab.strings[match_id])

app = QApplication(sys.argv)
window = UI()
window.show()
sys.exit(app.exec_())