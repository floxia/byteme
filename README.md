<p align="center">
  <img src="./icon.floxia" alt="ByteMe Logo" />
</p>

# ByteMe Serial Monitor 🚀

**ByteMe Serial Monitor** is a serial monitor tool built with PySide6, designed for interacting with serial devices. It allows you to connect, read data from serial devices easily. It also provides real-time updates and visual indicators such as an LED for incoming data status. 🔌

<p align="center">
  <img src="./snapshot.floxia" alt="ByteMe Snapshot" />
</p>

## Features: 🌟
- **Port Selection**: View and select available serial ports. ⚙️
- **Baud Rate Settings**: Adjust the baud rate for communication. Supported rates: 9600, 14400, 19200, 28800, 38400, 57600, 115200. 🏎️
- **Real-time Data**: Display received data in a scrollable text area. 📊
- **LED Indicator**: Shows green when incoming data red when no data is available. 💡
- **Device Name**: Displays the connected device’s description. 🖥️
- **Refresh Ports**: Dynamically refresh available ports. 🌊
- **About Dialog**: Provides app version, licensing information, and an app icon. ℹ️
- **GPL-3.0 Licensed**: Open-source under the GPL-3.0 License. 📜

## Installation:

1. Clone the repository:
    ```bash
    git clone https://github.com/floxia/byteme.git
    ```

2. Navigate to the project folder:
    ```bash
    cd byteme
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the app:

    Via Terminal:
    ```bash
    python byteme.py
    ```

    Or via the Windows .bat file:
    - Double-click `start.bat` to launch the app. 🖱️

## License: 📜
This project is licensed under the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Powered By: 🔋
This application is powered by:
- [Python](https://www.python.org/) 🐍
- [PySide6](https://pypi.org/project/PySide6/) ⚙️

## Acknowledgments: 🙏
- PySide6 for the GUI framework.
