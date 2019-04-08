import sys
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection

class Timeline(QMainWindow):
    def __init__(self):
            super().__init__()

    def plot(self, tableWidget):
        number_of_rows = self.tableWidget.rowCount()
        number_of_columns = self.tableWidget.columnCount()

        begins = []
        addOn = []
        beginCount = 0
        width = 5
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            startTime = str(item.text())[:-2]
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

        ends = []
        endCount = 0
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 4)
            duration = 0
            #Converts sound file to seconds
            with contextlib.closing(wave.open(str(item.text()),'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
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
            data.append((dt.datetime(2018, 7, begins[x][0], begins[x][1], begins[x][2]),dt.datetime(2018, 7, ends[x][0], ends[x][1], ends[x][2]), key))
            cats[key] = x
            labels.append(key)
            count.append(x)

        verts = []
        for d in data:
            print(d)
            v =  [(mdates.date2num(d[0]), cats[d[2]]-.4),
                  (mdates.date2num(d[0]), cats[d[2]]+.4),
                  (mdates.date2num(d[1]), cats[d[2]]+.4),
                  (mdates.date2num(d[1]), cats[d[2]]-.4),
                  (mdates.date2num(d[0]), cats[d[2]]-.4)]
            verts.append(v)

        bars = PolyCollection(verts)

        fig, ax = plt.subplots()
        ax.add_collection(bars)
        ax.autoscale()
        loc = mdates.MinuteLocator(byminute=[0,15,30,45])
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))

        ax.set_yticks(count)
        ax.set_yticklabels(labels)
        plt.figure()
        self.canvas.draw

        #create combined sound file
        sound1 = AudioSegment.from_wav("service-bell.wav")
        sound2 = AudioSegment.from_wav("heavy-rain.wav")
        sound3 = AudioSegment.from_wav("service-bell.wav")

        # mix sound2 with sound1, starting at 70% into sound1)
        tmpsound = sound1.overlay(sound2, position=0.7 * len(sound1))
        # mix sound3 with sound1+sound2, starting at 30% into sound1+sound2)
        output = tmpsound .overlay(sound3, position=0.3 * len(tmpsound))

        play(output)
        output.export("mixed_sounds.wav", format="wav")

if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = Timeline()
        sys.exit(app.exec_())
