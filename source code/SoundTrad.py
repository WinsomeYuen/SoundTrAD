import os, sys, csv, time, wave, contextlib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QUrl, QThread
from PyQt5.QtMultimedia import QSound, QAudioDeviceInfo, QAudio, QMediaContent, QMediaPlayer

from enterdb import EnterDb

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import datetime as dt
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection
from datetime import timedelta

from soundsuggestion import SoundSuggestion
from audioplayer import AudioPlayer
from pydub import AudioSegment
from pydub.playback import play

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = 'SoundTrad'
        self.left = 0
        self.top = 0
        self.width = 1250
        self.height = 680
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        global db
        db = EnterDb()
        # creating the Cue Sheet and Timeline widget and setting it as central
        self.cue_timeline_widget = CueTimeline(parent=self)
        self.setCentralWidget(self.cue_timeline_widget)
        # filling up a menu bar
        bar = self.menuBar()
        # File menu
        file_menu = bar.addMenu('File')
        # adding actions to file menu
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.cue_timeline_widget.handleOpen)
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.cue_timeline_widget.handleSave)
        close_action = QAction('Close', self)
        close_action.triggered.connect(self.closeEvent)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(close_action)
        #View
        create_menu = bar.addMenu('View')
        audio_action = QAction('External Audio Player', self)
        audio_action.triggered.connect(self.cue_timeline_widget.audioPlayer)
        mysql_action = QAction('Set MySQL Credentials', self)
        mysql_action.triggered.connect(self.enterDb)
        create_menu.addAction(audio_action)
        create_menu.addAction(mysql_action)
        # Help menu
        help_menu = bar.addMenu('Help')

    def enterDb(self):
        db = EnterDb()

    def saveFile(self):
        save_file = QFileDialog.getSaveFileName(self, "Save file", "./", "All files(*)")
        print(save_file)
        if save_file:
            with open(save_file, "w") as save_data:
                save_data.write(repr(DATA))

    def exitAction(self):
        exitAc = QAction('&Exit',self)
        exitAc.setShortcut('Ctrl+Q')
        exitAc.setStatusTip('Exit App')
        exitAc.triggered.connect(self.closeEvent)
        return exitAc

    def closeEvent(self,event):
            reply = QMessageBox.question(self,'Close SoundTrad','Press Yes to Close.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            if reply == QMessageBox.Yes :
                    qApp.quit()
            else :
                    try:
                            event.ignore()
                    except AttributeError:
                            pass

class CueTimeline(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # create and set layout to place widgets
        grid_layout = QGridLayout(self)

        self.createTable()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)

        self.button = QPushButton('Generate Timeline')
        self.button.clicked.connect(self.plot)

        controls = QHBoxLayout()
        self.addbtn = QPushButton("Add an Event")
        self.addbtn.clicked.connect(self.add)
        self.delbtn = QPushButton("Delete an Event")
        self.delbtn.clicked.connect(self.delete)
        self.clearbtn = QPushButton('Clear Cue Sheet')
        self.clearbtn.clicked.connect(self.clear)
        self.savebtn = QPushButton('Save Cue Sheet')
        self.savebtn.clicked.connect(self.handleSave)
        controls.addWidget(self.addbtn)
        controls.addWidget(self.delbtn)
        controls.addWidget(self.clearbtn)
        controls.addWidget(self.savebtn)

        self.centralWidget = QWidget()
        self.audioPlayer()
        self.mainaudioplayer = AudioPlayer()

        self.mixed = True
        # add widgets to layout. Params are:
        # (widget, fromRow, fromColumn, rowSpan=1, columnSpan=1)
        grid_layout.addWidget(self.toolbar, 0, 0)
        grid_layout.addWidget(self.tableWidget, 1, 0, 3, 4)
        grid_layout.addLayout(controls, 4, 0, 1, 4)
        grid_layout.addWidget(self.canvas, 5, 0, 1, 4)
        grid_layout.addWidget(self.button, 6, 0, 1, 4)
        grid_layout.addWidget(self.mainaudioplayer, 7, 0, 1, 4)

    def audioPlayer(self):
        self.audioplayer = AudioPlayer()

    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget(1,7)
        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet('font-size: 13pt; font-family: Tw Cen MT Std;')
        self.tableWidget.setHorizontalHeaderLabels(['Time', 'Identify Action/Event',
            'Cause', 'Associated Events', 'Description / Value',
            'Sound File (click sound file and press play in seperate audio player)',''])
        uploadButton = self.createUploadButton()
        causeList = self.createCauseList()
        eventList = self.createEventList()

        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.setItem(0,0, QTableWidgetItem("1:00pm"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("warning"))
        self.tableWidget.setCellWidget(0,2, causeList)
        self.tableWidget.setCellWidget(0,3, eventList)
        self.tableWidget.setItem(0,4, QTableWidgetItem("Travelling at 70mph"))
        self.tableWidget.setCellWidget(0,6, uploadButton)
        self.tableWidget.move(0,0)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_double_click)
        self.tableWidget.itemClicked.connect(self.on_one_click)

    def createCauseList(self):
        combo_box_options = ["Start","Stop","State Change", "Threshold"]
        combo = QComboBox()
        for t in combo_box_options:
            combo.addItem(t)
        return combo

    def createEventList(self):
        combo_box_options = ["User Actions","System Actions/Events",
        "Environmental Events", "Continuous Event"]
        combo = QComboBox()
        for t in combo_box_options:
            combo.addItem(t)
        return combo

    def createUploadButton(self):
        pWidget = QWidget()
        pLayout = QHBoxLayout(pWidget)
        uploadButton = QPushButton('Upload Sound')
        uploadButton.setObjectName(str(self.tableWidget.rowCount()-1))
        pLayout.addWidget(uploadButton)
        pLayout.setContentsMargins(0, 0, 0, 0)
        pWidget.setLayout(pLayout)
        uploadButton.clicked.connect(self.openUpload)
        return pWidget

    def openUpload (self):
        buttonClicked = self.sender()
        index = self.tableWidget.indexAt(buttonClicked.parent().pos())
        row = index.row()
        cause = self.tableWidget.cellWidget(row, 2)
        indexCause = cause.currentText()
        event = self.tableWidget.cellWidget(row, 3)
        indexEvent = event.currentText()
        self.dialog = SoundSuggestion()
        self.dialog.homeScreen(indexCause, indexEvent, db.returnHost(), db.returnUser(), db.returnPass())
        self.dialog.exec_()
        rowNumber = int(self.sender().objectName())
        self.tableWidget.setItem(rowNumber,5, QTableWidgetItem(str(self.dialog.filePath())))

    @pyqtSlot()
    def on_double_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    @pyqtSlot()
    def on_one_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.audioplayer.setFile(currentQTableWidgetItem.text())

    def add(self):
        rowNumber = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowNumber)
        newCauseButton = self.createCauseList()
        self.tableWidget.setCellWidget(rowNumber,2, newCauseButton)
        newEventButton = self.createEventList()
        self.tableWidget.setCellWidget(rowNumber,3, newEventButton)
        newUploadButton = self.createUploadButton()
        self.tableWidget.setCellWidget(rowNumber,6, newUploadButton)

    def delete(self):
        self.tableWidget.removeRow(self.tableWidget.currentRow())

    def clear(self):
        self.tableWidget.setRowCount(0)

    def plot(self):
        number_of_rows = self.tableWidget.rowCount()

        begins = [] #the time the sound begins according to cuesheet (HMS)
        addOn = [] #start time in seconds to add to when the file ends
        beginCount = 0
        width = 5
        for row in range(number_of_rows):
            item = self.tableWidget.item(row, 0)
            startTime = str(item.text())[:-2]
            sound = self.tableWidget.item(row, 5)
            if (startTime == "") or (sound is None) or (sound == "NA"):
                QMessageBox.question(self,'Error',"Please fill in row fully or delete it",QMessageBox.Ok)
                return
            formatted = (width - len(str(startTime))) * "0" + str(startTime)
            period = str(item.text())[-2:]
            #Converts 12h to 24h
            if(period == "pm" or period == "am"):
                startTime = dt.datetime.strptime(formatted + ":00 " + period, '%I:%M:%S %p')
                startTime = startTime.strftime("%H:%M:%S%p")[:-2]
            startTime = startTime + ":00"
            #Converts hms into seconds for below loop and adds split time to array
            hours, mins, secs, e = [int(i) for i in startTime.split(':')]
            addOnTime = 3600*hours + 60*mins + secs
            addOn.append(addOnTime)
            entry = [hours, mins, secs]
            entry = [int(x) for x in entry]
            begins.append(entry)
            beginCount+=1

        ends = [] #when the sound file ends (HMS)
        soundlength = [] #duration of each sound in secs
        endCount = 0
        for row in range(number_of_rows):
            item = self.tableWidget.item(row, 5)
            duration = 0
            #Converts sound file to seconds
            with contextlib.closing(wave.open(str(item.text()),'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                soundlength.append(duration)
            #Work out length of sound to plot on timeline
            duration = duration + addOn[endCount]
            mins, secs = divmod(duration, 60)
            hours, mins = divmod(mins, 60)
            duration = [hours, mins, secs]
            duration = [int(x) for x in duration]
            ends.append(duration)
            endCount+=1

        data = []
        cats = {}
        labels = []
        count = []
        for x in range(endCount):
            key = 'Event ' + str(x)
            data.append((dt.datetime(2018, 7, 1, begins[x][0], begins[x][1], begins[x][2]),dt.datetime(2018, 7, 1, ends[x][0], ends[x][1], ends[x][2]), key))
            cats[key] = x
            labels.append(key)
            count.append(x)

        verts = []
        for d in data:
            v =  [(mdates.date2num(d[0]), cats[d[2]]-.4),
                  (mdates.date2num(d[0]), cats[d[2]]+.4),
                  (mdates.date2num(d[1]), cats[d[2]]+.4),
                  (mdates.date2num(d[1]), cats[d[2]]-.4),
                  (mdates.date2num(d[0]), cats[d[2]]-.4)]
            verts.append(v)

        bars = PolyCollection(verts)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.add_collection(bars)
        ax.autoscale()
        loc = mdates.MinuteLocator()
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))

        ax.set_yticks(count)
        ax.set_yticklabels(labels)

        self.canvas.draw()

        mixedsound = []         #create combined sound file

        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 5).text()
            sound = AudioSegment.from_wav(str(item))
            mixedsound.append(sound)

        tmpsound = mixedsound[0]
        lengthlist = len(mixedsound)
        secondpart = 0
        if(lengthlist > 1):
            for sound in range(lengthlist-1):
                time = abs(addOn[sound]-addOn[sound+1])
                if sound == 0:
                    music = soundlength[sound]+soundlength[sound+1]
                else:
                    music = secondpart/ -1000
                if music > time: #it does overlap
                    secondmusic = mixedsound[sound+1]
                    tmpsound = tmpsound.overlay(secondmusic, position=(time* 1000))
                    lastpart = soundlength[sound] - time
                    secondpart = (soundlength[sound+1] - lastpart)* -1000
                    lastseconds = secondmusic[secondpart:]
                    tmpsound = tmpsound.append(lastseconds)
                else:
                    tmpsound = tmpsound.append(mixedsound[sound+1])

        path = os.getcwd().replace('\\', '/')

        if self.mixed == True:
            tmpsound.export("mixed_sounds.wav", format="wav")
            file = ''.join([path,"/mixed_sounds.wav"])
            self.mainaudioplayer.setFile(file)
            self.mixed = False
        else:
            tmpsound.export("mixed_sound.wav", format="wav")
            file = ''.join([path,"/mixed_sound.wav"])
            self.mainaudioplayer.setFile(file)
            self.mixed = True


    def handleSave(self):
        path = QFileDialog.getSaveFileName(self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in range(self.tableWidget.rowCount()):
                    row_data = []
                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        elif column == 2:
                            cause = self.tableWidget.cellWidget(row, column).currentIndex()
                            row_data.append(cause)
                        elif column == 3:
                            event = self.tableWidget.cellWidget(row, column).currentIndex()
                            row_data.append(event)
                        else:
                            row_data.append('')
                    writer.writerow(row_data)

    def handleOpen(self):
        self.check_change = False
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], newline='') as csv_file:
                self.tableWidget.setRowCount(0)
                self.tableWidget.setColumnCount(7)
                my_file = csv.reader(csv_file, dialect='excel')
                for row_data in my_file:
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    if len(row_data) > 7:
                        QMessageBox.question(self,'Error',"Opening an invalid file",QMessageBox.Ok)
                    for column, stuff in enumerate(row_data):
                        if column == 2:
                            newCauseButton = self.createCauseList()
                            newCauseButton.setCurrentIndex(int(stuff))
                            self.tableWidget.setCellWidget(row, column, newCauseButton)
                        elif column == 3:
                            newEventButton = self.createEventList()
                            newEventButton.setCurrentIndex(int(stuff))
                            self.tableWidget.setCellWidget(row, column, newEventButton)
                        elif column == 6:
                            newUploadButton = self.createUploadButton()
                            self.tableWidget.setCellWidget(row, column, newUploadButton)
                        else:
                            item = QTableWidgetItem(stuff)
                            self.tableWidget.setItem(row, column, item)
        self.check_change = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # creating main window
    mw = MainWindow()
    mw.setWindowIcon(QIcon('images/SoundTrad.png'))
    mw.show()
    sys.exit(app.exec_())
