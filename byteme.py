from PySide6.QtCore import QTimer, Qt, QIODevice, QCoreApplication, QLoggingCategory
from PySide6.QtGui import QPainter, QColor, QCursor, QIcon, QPixmap
from PySide6.QtWidgets import QSplashScreen, QApplication, QWidget, QVBoxLayout, QComboBox,QTextEdit, QPushButton, QLabel, QHBoxLayout, QDialog, QDialogButtonBox
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
import sys

# Suppress all warnings related to unknown properties
QLoggingCategory.setFilterRules("*.warning=false")

class LedLight(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self.state = False

    def set_led_state(self, state: bool):
        self.state = state
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(0, 255, 0) if self.state else QColor(255, 0, 0)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())
        painter.end()

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        layout = QVBoxLayout()

        # Add the icon
        icon_label = QLabel()
        icon_pixmap = QPixmap("icon.floxia")  # Replace with the path to your icon
        icon_label.setPixmap(icon_pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)

        about_text = QLabel("ByteMe Serial Monitor\nVersion 0.4\n© 2025 Matteo Floria")
        about_text.setAlignment(Qt.AlignCenter)

        # License link
        license_label = QLabel(
            '<a href="https://www.gnu.org/licenses/gpl-3.0.en.html">Licensed under GPL-3.0</a>\n'
        )
        license_label.setAlignment(Qt.AlignCenter)
        license_label.setOpenExternalLinks(True)
        license_label.setCursor(QCursor(Qt.PointingHandCursor))

        # Powered by section
        # Powered by section with hyperlinks (using HTML)
        powered_by_label = QLabel()
        powered_by_label.setText(
            'Powered by: '
            '<a href="https://www.python.org/">Python</a>, '
            '<a href="https://pypi.org/project/PySide6/">PySide6</a>'
        )
        powered_by_label.setAlignment(Qt.AlignCenter)
        powered_by_label.setOpenExternalLinks(True)
        powered_by_label.setCursor(QCursor(Qt.PointingHandCursor))

        # Center the button
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.setCenterButtons(True)
        button_box.accepted.connect(self.accept)

        layout.addWidget(icon_label)
        layout.addWidget(about_text)
        layout.addWidget(license_label)
        layout.addWidget(powered_by_label)
        layout.addWidget(button_box)
        self.setLayout(layout)

class SerialMonitor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ByteMe Serial Monitor")
        self.resize(400, 300)
        self.set_app_icon(False)

        layout = QVBoxLayout()

        self.port_selector = QComboBox()
        self.update_ports()

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.update_ports)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.text_edit.clear)

        self.baud_rate_selector = QComboBox()
        self.baud_rate_selector.addItems(["9600", "14400", "19200", "28800", "38400", "57600", "115200"])

        self.device_name_label = QLabel("Device Name:")

        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        port_layout.addWidget(self.port_selector)
        port_layout.addWidget(self.refresh_button)
        port_layout.addWidget(self.clear_button)
        port_layout.addWidget(QLabel("Baud Rate:"))
        port_layout.addWidget(self.baud_rate_selector)

        self.led_light = LedLight()
        port_layout.addWidget(self.led_light)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_serial)

        self.engraved_label = QLabel("Matteo Floria")
        self.engraved_label.setAlignment(Qt.AlignCenter)
        self.engraved_label.setStyleSheet("color: gray; cursor: pointer;")
        self.engraved_label.mousePressEvent = self.show_about_dialog
        self.engraved_label.setCursor(QCursor(Qt.PointingHandCursor))

        layout.addLayout(port_layout)
        layout.addWidget(self.device_name_label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.engraved_label)

        self.setLayout(layout)

        self.serial_port = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial)

        self.port_check_timer = QTimer()
        self.port_check_timer.timeout.connect(self.check_port_availability)
        self.port_check_timer.start(1000)

        self.port_selector.currentTextChanged.connect(self.update_device_name)
        self.update_device_name()

    def update_ports(self):
        self.port_selector.clear()
        ports = QSerialPortInfo.availablePorts()
        for port in ports:
            self.port_selector.addItem(port.portName())

    def connect_serial(self):
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.close()
            self.connect_button.setText("Connect")
            self.timer.stop()
            self.led_light.set_led_state(False)
            self.set_app_icon(False)
        else:
            port = self.port_selector.currentText()
            baud_rate = int(self.baud_rate_selector.currentText())
            self.serial_port = QSerialPort(port)
            self.serial_port.setBaudRate(baud_rate)
            self.serial_port.setDataBits(QSerialPort.Data8)
            self.serial_port.setParity(QSerialPort.NoParity)
            self.serial_port.setStopBits(QSerialPort.OneStop)
            self.serial_port.setFlowControl(QSerialPort.NoFlowControl)

            if not self.serial_port.open(QIODevice.ReadWrite):
                self.text_edit.append(f"Failed to open port {port}")
                return

            self.connect_button.setText("Disconnect")
            self.timer.start(100)
            self.set_app_icon(True)

    def read_serial(self):
        if self.serial_port and self.serial_port.bytesAvailable() > 0:
            data = self.serial_port.readLine().data().decode('utf-8').strip()
            self.text_edit.append(data)
            self.led_light.set_led_state(True)
            self.set_app_icon(True)
        else:
            self.led_light.set_led_state(False)
            self.set_app_icon(False)

    def check_port_availability(self):
        if self.serial_port and not self.serial_port.isOpen():
            return

        available_ports = [port.portName() for port in QSerialPortInfo.availablePorts()]
        current_port = self.port_selector.currentText()

        if current_port not in available_ports:
            if self.serial_port and self.serial_port.isOpen():
                self.serial_port.close()
                self.connect_button.setText("Connect")
                self.timer.stop()
                self.device_name_label.setText("Device Name:")
                self.text_edit.append(f"Disconnected: {current_port} no longer available")
                self.led_light.set_led_state(False)
                self.set_app_icon(False)

    def update_device_name(self):
        port = self.port_selector.currentText()

        if port:
            for ports in QSerialPortInfo.availablePorts():
                if ports.portName() == port:
                    self.device_name_label.setText(f"Device Name: {ports.description()}")
                    break
        else:
            self.device_name_label.setText("Device Name:")

    def set_app_icon(self, on: bool):
        #icon_path = "led_on.floxia" if on else "led_off.floxia"
        icon_path = "icon.floxia"
        self.setWindowIcon(QIcon(icon_path))

    def show_about_dialog(self, event):
        about_dialog = AboutDialog(self)
        about_dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Create and show splash screen
    splash_pix = QPixmap('icon.floxia')
    splash = QSplashScreen(splash_pix)
    splash.show()
    window = SerialMonitor()
    window.show()
    splash.close()
    sys.exit(app.exec())