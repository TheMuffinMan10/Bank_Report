import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QGridLayout, QDesktopWidget

'''
    method to check bank statement
'''

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Bank Report")
window.resize(350, 500)

#Centre the window
qr = window.frameGeometry()
cp = QDesktopWidget().availableGeometry().center()
qr.moveCenter(cp)
window.move(qr.topLeft())

#Making text bold
font = QFont()
font.setBold(True)

#Required Widgets
lblInstruction = QLabel("Upload your statement to get a small report", parent=window)
lblInstruction.setFixedHeight(25)
font.setPointSize(9)
lblInstruction.setFont(font)

    #Income
lblIncome = QLabel("Total Income")
lblIncome.setFixedHeight(10)

    #Expense
lblExpense = QLabel("Total Expense")
lblExpense.setFixedHeight(20)

    #Net
lblNet = QLabel("Surplus/Deficet")
lblNet.setFixedHeight(20)

    #Button
button = QPushButton("Upload Statement")
layout = QGridLayout()

layout.addWidget(lblInstruction, 1, 5)
layout.addWidget(lblIncome, 2, 0)
layout.addWidget(lblExpense, 2, 5)
layout.addWidget(lblNet, 2, 10)
layout.addWidget(button)
window.setLayout(layout)

window.show()
sys.exit(app.exec_())