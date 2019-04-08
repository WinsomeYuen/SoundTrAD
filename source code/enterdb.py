import sys
from os.path import expanduser
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
import MySQLdb as mdb

class EnterDb(QDialog):
    def __init__(self):
        super(EnterDb, self).__init__()
        self.createFormGroupBox()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowIcon(QIcon('images/SoundTrad.png'))
        self.setWindowTitle("MySQL Login Credentials")
        self.resize(630, 50)

    def accept(self):
        try:
            db = mdb.connect(self.host.text(),self.user.text(),self.pw.text())
            self.close()
        except mdb.Error as e:
            QMessageBox.question(self,'Error',"Failed to connect",QMessageBox.Ok)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Login")
        layout = QFormLayout()
        self.host = QLineEdit()
        layout.addRow(QLabel("Host:"), self.host)
        self.user = QLineEdit()
        layout.addRow(QLabel("User:"), self.user)
        self.pw = QLineEdit()
        self.pw.setEchoMode(QLineEdit.Password)
        layout.addRow(QLabel("Password:"), self.pw)
        self.formGroupBox.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    def returnHost(self):
        return self.host.text()

    def returnUser(self):
        return self.user.text()

    def returnPass(self):
        return self.pw.text()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = EnterDb()
    sys.exit(dialog.exec_())

