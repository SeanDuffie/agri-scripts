""" @file rpi_client.py
    @author Sean Duffie
    @brief Communicate with ESP32 over bluetooth, run this on RPi 4.
    
    Resources:
    - https://www.theengineeringprojects.com/2023/04/how-to-connect-pi-4-and-esp32-via-bluetooth.html
    - https://www.reddit.com/r/arduino/comments/mx7x31/file_transfer_using_bluetooth_classic_esp32_sd/
    - https://randomnerdtutorials.com/display-images-esp32-esp8266-web-server/
"""
import sys
import time

import requests
from bluepy import btle
from PyQt5.QtCore import (QObject, QRunnable, QThreadPool, QTimer, pyqtSignal,
                          pyqtSlot)
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPlainTextEdit,
                             QPushButton, QVBoxLayout, QWidget)


class WorkerSignals(QObject):
    signalMsg = pyqtSignal(str)
    signalRes = pyqtSignal(str)

class MyDelegate(btle.DefaultDelegate):
    def __init__(self, sgn):
        btle.DefaultDelegate.__init__(self)
        self.sgn = sgn

    def handleNotification(self, cHandle, data):
        try:
            dataDecoded = data.decode()
            self.sgn.signalRes.emit(dataDecoded)
        except UnicodeError:
            print("UnicodeError: ", data)

class WorkerBLE(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.rqsToSend = False

    @pyqtSlot()
    def run(self):
        self.signals.signalMsg.emit("WorkerBLE start")
        #---------------------------------------------
        p = btle.Peripheral("3c:71:bf:0d:dd:6a")
        p.setDelegate( MyDelegate(self.signals) )
        svc = p.getServiceByUUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        self.ch_Tx = svc.getCharacteristics("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")[0]
        ch_Rx = svc.getCharacteristics("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")[0]
        setup_data = b"\x01\00"
        p.writeCharacteristic(ch_Rx.valHandle+1, setup_data)

        # BLE loop --------
        while True:
            """
            if p.waitForNotifications(1.0):
                # handleNotification() was called
                continue
            print("Waiting...")
            """
            p.waitForNotifications(1.0)
            if self.rqsToSend:
                self.rqsToSend = False
                try:
                    self.ch_Tx.write(self.bytestosend, True)
                except btle.BTLEException:
                    print("btle.BTLEException");
        #---------------------------------------------hellohello
        self.signals.signalMsg.emit("WorkerBLE end")

    def toSendBLE(self, tosend):
        self.bytestosend = bytes(tosend, 'utf-8')
        self.rqsToSend = True
        """
        try:
            self.ch_Tx.write(bytestosend, True)
        except BTLEException:
            print("BTLEException");
        """

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        buttonStartBLE = QPushButton("Start BLE")
        buttonStartBLE.pressed.connect(self.startBLE)
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.outconsole = QPlainTextEdit()
        buttonSendBLE = QPushButton("Send message")
        buttonSendBLE.pressed.connect(self.sendBLE)
        layout.addWidget(buttonStartBLE)
        layout.addWidget(self.console)
        layout.addWidget(self.outconsole)
        layout.addWidget(buttonSendBLE)
        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.show()
        self.threadpool = QThreadPool()
        print(
            "Multithreading with Maximum %d threads" % self.threadpool.maxThreadCount())

    def startBLE(self):
        self.workerBLE = WorkerBLE()
        self.workerBLE.signals.signalMsg.connect(self.slotMsg)
        self.workerBLE.signals.signalRes.connect(self.slotRes)
        self.threadpool.start(self.workerBLE)

    def sendBLE(self):
        strToSend = self.outconsole.toPlainText()
        self.workerBLE.toSendBLE(strToSend)

    def slotMsg(self, msg):
        print(msg)

    def slotRes(self, res):
        self.console.appendPlainText(res)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
