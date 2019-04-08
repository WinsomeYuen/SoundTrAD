import sys, datetime, wave, contextlib
import MySQLdb as mdb
from os.path import expanduser
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SoundSuggestion(QDialog):
    soundFileSelection = None

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        global soundFileSelection
        soundFileSelection = "NA"
        self.setWindowIcon(QIcon('images/SoundTrad.png'))


    def homeScreen(self, c, e, h, u, p):
        global cause
        cause = c
        global event
        event = e
        global host
        host = h
        global user
        user = u
        global password
        password = p

        if not host or not user or not password:
            QMessageBox.question(self,'Error',"Not connected to database",QMessageBox.Ok)
            return

        #Set title of window
        self.setWindowTitle('Sound Suggestions')
        self.createTable()

        controlArea = QVBoxLayout(self)
        controlArea.addWidget(self.tableWidget)
        selectButton = QPushButton('Select Sound')
        selectButton.clicked.connect(self.selectSound)
        controlArea.addWidget(selectButton)
        addButton = QPushButton('Add Sound')
        addButton.clicked.connect(self.addSound)
        controlArea.addWidget(addButton)

        #Set Dimensions of the MainWindow
        self.resize(600,300)
        #show everything.
        self.show()

    def createTable(self):
         # Create table
         self.tableWidget = QTableWidget()
         self.tableWidget.setRowCount(0)
         self.tableWidget.setColumnCount(5)
         header = self.tableWidget.horizontalHeader()
         header.setStyleSheet('font-size: 13pt; font-family: Tw Cen MT Std;')
         self.tableWidget.setHorizontalHeaderLabels(['Name','Cause','Associated Event','Length','Sound File'])

         header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
         header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
         header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
         header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
         header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

         self.tableWidget.move(0,0)
         self.loadSounds()

    def loadSounds(self):
        try:
            db = mdb.connect(host,user,password)
            print("Connected")
            cur = db.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS soundtrad")
            cur.execute("use soundtrad")
            # Create table as per requirement
            cur.execute("""CREATE TABLE IF NOT EXISTS sound (
                        ID INTEGER AUTO_INCREMENT PRIMARY KEY,
                        Name VARCHAR(500) DEFAULT NULL,
                        Cause VARCHAR(500) DEFAULT NULL,
                        Event VARCHAR(500) DEFAULT NULL,
                        Length VARCHAR(500) DEFAULT NULL,
                        SoundFile TEXT NOT NULL)""")
            cur.execute("SELECT * FROM sound")
            self.tableWidget.setRowCount(0)
            for i in range(cur.rowcount):
                result = cur.fetchall()
                for col in result:
                    if col[2] == cause and col[3] == event:
                        rowNumber = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(rowNumber)
                        self.tableWidget.setItem(rowNumber,0, self.fillItem(col[1]))
                        self.tableWidget.setItem(rowNumber,1, self.fillItem(col[2]))
                        self.tableWidget.setItem(rowNumber,2, self.fillItem(col[3]))
                        self.tableWidget.setItem(rowNumber,3, self.fillItem(col[4]))
                        self.tableWidget.setItem(rowNumber,4, self.fillItem(col[5]))
            db.close() #Disconnect from the server
        except mdb.Error as e:
            print("Failed to Connect ", e)

    def fillItem(self, row):
        item = QTableWidgetItem()
        item.setText(row)
        return item

    def selectSound(self):
        for item in self.tableWidget.selectedItems():
            global soundFileSelection
            soundFileSelection = item.text()
        self.done(0)

    def filePath(self):
        return soundFileSelection

    def addSound(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')
        filepath = filename[0]
        isWav = filepath[-3:]
        if isWav == "":
            return
        elif isWav != "wav":
            QMessageBox.question(self,'Error',"File selected is not .WAV",QMessageBox.Ok)
            return
        name = filepath.rsplit('/', 1)[-1]
        duration = ""
        with contextlib.closing(wave.open(str(filepath),'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        length = str(datetime.timedelta(seconds=duration))
        try:
            db = mdb.connect(host,user,password,"soundtrad")
            cur = db.cursor()
            cur.execute('INSERT INTO sound (Name, Length, Cause, Event, SoundFile) VALUES (%s,%s,%s,%s,%s)',(name,length,cause,event,filepath))
            db.commit()
            db.close() #Disconnect from the server
            self.loadSounds()
        except mdb.Error as e:
            print("Failed to Connect")

if __name__ == '__main__':
        app = QApplication(sys.argv)
        # creating main window
        mw = MainWindow()
        mw.show()
        sys.exit(app.exec_())
