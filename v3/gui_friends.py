# Copyright (c) 2024, Department of Clinical Psychology, University of Buffalo.
# All rights reserved.
# This code is part of a research project and may not be used, modified, or distributed without permission.


# MADE FOR NORMALLY CLOSED VALVE

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

try:
    import RPi.GPIO as GPIO
    gpio_available = True
except (ImportError, RuntimeError):
    gpio_available = False

class ValveControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.experimentTimer = QTimer(self)
        self.experimentTimer.timeout.connect(self.updateTime)
        self.countdownTimer = QTimer(self)
        self.countdownTimer.timeout.connect(self.updateCountdown)
        self.countdownTimer_final = QTimer(self)
        self.countdownTimer_final.timeout.connect(self.updateCountdown_final)
        self.current_second = 0
        self.total_seconds = 0
        self.countdown_seconds = 10
        self.countdown_seconds_final = 10
        self.v_status = "OFF"
        self.puff_number = 0

    def initUI(self):
        self.setGeometry(100, 100, 800, 480)  # Adjust for tablet display
        self.setWindowTitle('Valve Control Experiment')
        
        layout = QVBoxLayout()
        layout.setSpacing(15)  # Increase spacing between widgets for better readability

        # Set a uniform font for all inputs and labels
        font = QFont("Arial", 12)

        # Input fields with labels and beautified design
        self.puffDurationInput = QLineEdit(self)
        self.puffDurationInput.setPlaceholderText("Enter puff duration (seconds)")
        self.puffDurationInput.setFont(font)
        self.puffDurationInput.setStyleSheet("padding: 8px;")
        layout.addWidget(self.puffDurationInput)

        self.numberOfPuffsInput = QLineEdit(self)
        self.numberOfPuffsInput.setPlaceholderText("Enter number of puffs")
        self.numberOfPuffsInput.setFont(font)
        self.numberOfPuffsInput.setStyleSheet("padding: 8px;")
        layout.addWidget(self.numberOfPuffsInput)

        self.interpuffIntervalInput = QLineEdit(self)
        self.interpuffIntervalInput.setPlaceholderText("Enter interpuff interval (seconds)")
        self.interpuffIntervalInput.setFont(font)
        self.interpuffIntervalInput.setStyleSheet("padding: 8px;")
        layout.addWidget(self.interpuffIntervalInput)

        # Start Experiment button with a more engaging design
        self.startButton = QPushButton('Start Experiment', self)
        self.startButton.clicked.connect(self.startExperiment)
        self.startButton.setFont(QFont("Arial", 16))  # Ensure the font is explicitly set
        self.startButton.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                padding: 10px;
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: beige;
                font: bold 14px;
                min-width: 10em;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #55aa55;
            }
        """)

        layout.addWidget(self.startButton)

        # Terminate Program button with a distinctive style
        self.terminateButton = QPushButton('Terminate Program', self)
        self.terminateButton.clicked.connect(self.terminateProgram)
        self.terminateButton.setFont(QFont("Arial", 16))  # Ensure the font is explicitly set
        self.terminateButton.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                padding: 10px;
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: beige;
                font: bold 14px;
                min-width: 10em;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #dd5555;
            }
        """)

        layout.addWidget(self.terminateButton)

        # Puff Number label with enhanced visibility
        self.puffNumberLabel = QLabel('Puff Number: 0', self)
        self.puffNumberLabel.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.puffNumberLabel)

        # Status label for Valve and Interpuff Interval in larger font and enhanced visibility
        self.statusLabel = QLabel('Experiment Status: Waiting to start...', self)
        self.statusLabel.setWordWrap(True)
        self.statusLabel.setFont(QFont("Arial", 16, QFont.Bold))
        self.statusLabel.setStyleSheet("QLabel { color: blue; padding: 8px; }")
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)


    # Other methods remain unchanged
    def startExperiment(self):
        if gpio_available:
            self.puff_duration = int(self.puffDurationInput.text())
            self.number_of_puffs = int(self.numberOfPuffsInput.text())
            self.interpuff_interval = int(self.interpuffIntervalInput.text())

            self.setupGPIO()
            self.prepareExperiment()
        else:
            QMessageBox.warning(self, "Error", "GPIO is not available. Ensure this is running on a Raspberry Pi with RPi.GPIO installed.")

    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)
        self.valve_pin = 24  # GPIO pin connected to the valve control (changed)
        GPIO.setwarnings(False)
        GPIO.setup(self.valve_pin, GPIO.OUT)



    def updateStatusLabel(self, text):
        self.statusLabel.setText(text)
        self.statusLabel.setStyleSheet("QLabel { color : blue; }")
        QApplication.processEvents()

    # Update the rest of the methods as necessary to ensure functionality

    def updateTime(self):
        self.current_second += 1
        if self.v_status == "ON":
            self.updateStatusLabel(f"Valve ON: {self.current_second} seconds")
        else:
            self.updateStatusLabel(f"Interpuff Interval: {self.current_second} seconds")

        if self.current_second >= self.total_seconds:
            self.experimentTimer.stop()
            if self.v_status == "ON":
                GPIO.output(self.valve_pin, GPIO.LOW)  # Turn the valve off
                self.v_status = "OFF"

                if self.puff_number <= self.number_of_puffs:
                    self.startTimer(self.interpuff_interval, "OFF")
            elif self.v_status == "OFF":
                if self.puff_number < self.number_of_puffs:
                    self.puff_number += 1
                    self.puffNumberLabel.setText(f'Puff Number: {self.puff_number}')
                    self.v_status = "ON"
                    GPIO.output(self.valve_pin, GPIO.HIGH)  # Turn the valve on for the next puff
                    self.startTimer(self.puff_duration, "ON")
                else:
                    self.countdownTimer_final.start(1000)
                    

    def updateCountdown(self):
        self.countdown_seconds -= 1
        self.updateStatusLabel(f"Experiment begins in: {self.countdown_seconds} seconds")
        if self.countdown_seconds == 0:
            self.countdownTimer.stop()
            self.puff_number = 1
            self.puffNumberLabel.setText(f'Puff Number: {self.puff_number}')
            self.v_status = "ON"
            GPIO.output(self.valve_pin, GPIO.HIGH)  # Turn the valve on for the first puff
            self.startTimer(self.puff_duration, "ON")

    def updateCountdown_final(self):
        self.countdown_seconds_final -= 1
        self.updateStatusLabel(f"Experiment terminates in: {self.countdown_seconds_final} seconds")
        #GPIO.output(self.valve_pin, GPIO.HIGH)
 
        if self.countdown_seconds_final == 0:
            self.countdownTimer_final.stop()
            self.updateStatusLabel("Experiment completed")
            #GPIO.output(self.valve_pin, GPIO.LOW)
            GPIO.cleanup()


    def startTimer(self, seconds, status):
        self.total_seconds = seconds
        self.current_second = 0
        self.experimentTimer.start(1000)  # Timer timeout in 1000 ms (1 second)

    def prepareExperiment(self):
        self.countdown_seconds = 10  # Reset countdown for experiment preparation
        self.updateStatusLabel(f"Experiment begins in: {self.countdown_seconds} seconds")
        self.countdownTimer.start(1000)  # Start countdown timer

    def terminateProgram(self):
        reply = QMessageBox.question(self, 'Terminate Experiment', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.experimentTimer.stop()
            self.countdownTimer.stop()
            if gpio_available:
                GPIO.cleanup()  # Ensure GPIO pins are cleaned up properly
            QApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ValveControlApp()
    ex.show()
    sys.exit(app.exec_())
