#!/usr/bin/python3

import json, re, sys, zmq
from PyQt4 import QtGui, QtCore

# Global variable 'callsign' to allow passing data into Thread

if len(sys.argv) == 2:
    callsign = str(sys.argv[1]).upper() # Get callsign from command line argument
else:
    callsign = ""

class dxLite():
    def __init__(self):
        context = zmq.Context()
        self.dxsocket = context.socket(zmq.SUBSCRIBE)
        self.dxsocket.connect("tcp://clublog.org:7373")

    def read(self):
        try:
            message = self.dxsocket.recv() # Wait for and accept ZMQ data
            message = message.decode() # Decode to a string
            data = json.loads(message) # Decode JSON data into list
        except UnicodeDecodeError:
            data = False # allows use of "if dxLite.read():" to test valid
        except:
            raise
        return data
        
class queueThread(QtCore.QThread):
    """ Thread to watch the cluster and emit any matches back to the main thread. """
    
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.cluster = dxLite()

    def run(self):
        while True:
            data = self.cluster.read()
            if data:
                if re.search(r"^("+re.escape(callsign)+")(\/(P|A(M?)|M(M)?))?$", data["Call"]) is not None: # Should match exact call, plus typical suffixes (/P, /A, /AM, /M, /MM)
                    header = "Spotted on " + str(data["Band"]) + "m"
                    body = data["Call"] + " spotted by " + data["Spotter"] + " on " + str(data["Freq"]/1000) + "MHz ("+str(data["Date"])[11:13] + ":" + str(data["Date"])[14:16] + "Z)"
                    
                    self.emit(QtCore.SIGNAL('message(QString, QString)'), header, body )

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip("DX Cluster Watch")
        
        while callsign == "": # If not set by argv
            self.changeCallsign()
        
        self.queue_thread = queueThread()
        self.connect(self.queue_thread, QtCore.SIGNAL('message(QString, QString)'), self.message)
        self.queue_thread.start()
        
        self.menu = QtGui.QMenu(parent)
        self.refresh_button = self.menu.addAction("Change Callsign...", self.changeCallsign)
        self.menu.addSeparator()
        exitAction = self.menu.addAction("Exit", self.askClose)
        
        self.setContextMenu(self.menu)
    
    def message(self, header, body):
        """ Function to allow Thread to interact with Tray Icon """
        self.showMessage(header, body, QtGui.QSystemTrayIcon.NoIcon, 3000)
        
    def notImplemented(self):
        """ Placeholder function for testing """
        msg = QtGui.QMessageBox()
        msg.setText("This feature does not exist.")
        msg.setWindowTitle("Not Implemented")
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        msg.exec_()
        
    def changeCallsign(self):
        """ Allow changing of callsign being monitored"""
        global callsign
        text, ok = QtGui.QInputDialog.getText(None, 'Callsign', 'Enter the callsign to watch for:', text=callsign)

        if ok and (text != ""):
            callsign = str(text).upper()
        
    def askClose(self):
        """ Avoid accidental exits """
        msg = QtGui.QMessageBox()
        msg.setText("Really Exit?")
        msg.setWindowTitle("Exit")
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        retval = msg.exec_()
        
        if retval == QtGui.QMessageBox.Yes:
            quit()

def main():
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("dx.png"), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
