from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, \
    QTextEdit

from vehicle_info_provider import VehicleInfoProvider


class DynamicImagePlayer(QWidget):
    def __init__(self, generate_image_function,
                 vehicle_info_provider: VehicleInfoProvider):
        super().__init__()

        self.generate_image_function = generate_image_function
        self._vehicle_info_provider = vehicle_info_provider
        self._vehicle_info = None

        main_layout = QVBoxLayout()
        # grid_layout = QGridLayout()  # Using a grid for better organization

        # Label and Line Edit (Text Box)
        self.label = QLabel(self)
        self.text_edit = QTextEdit()
        self.text_edit.setText("vehicle Number: {}"
                               "\nDriver Name: {}"
                               "\nMake & Type: {}"
                               "\nUnit: {}"
                               "\nColor: {}")
        self.text_edit.setMaximumHeight(100)
        self.text_edit.setReadOnly(True)

        # Timer for automatic updates (if needed)
        self.timer = QTimer(self)
        self.timer.timeout.connect(
            lambda: self.update_frame())  # Connect timer to update function
        self.timer_interval = 50  # Update every 1000ms (1 second)
        self.timer.start(self.timer_interval)  # Start the timer

        # Add widgets to layout
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.text_edit)

        self.setLayout(main_layout)

        self.setGeometry(100, 100, 1200, 800)

    def update_frame(self):
        frame, ocr = self.generate_image_function()  # Call the image generation function

        if ocr is not None:
            vehicle_info = self._vehicle_info_provider.get_details(ocr)
            if vehicle_info is not None:
                self._vehicle_info = vehicle_info

        self.update_text()

        if frame is not None:  # Check if image generation was successful
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line,
                                          QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_qt_format)
            scaled_pixmap = pixmap.scaled(self.label.size(),
                                          Qt.AspectRatioMode.KeepAspectRatio)
            self.label.setPixmap(scaled_pixmap)

    def update_text(self):
        if self._vehicle_info is not None:
            repr = ("vehicle Number: {}"
                    "\nDriver Name: {}"
                    "\nMake & Type: {}"
                    "\nUnit: {}"
                    "\nColor: {}".format(self._vehicle_info["vehicle_number"],
                                         self._vehicle_info["driver_name"],
                                         self._vehicle_info["make_and_type"],
                                         self._vehicle_info["unit"],
                                         self._vehicle_info["color"]))
            self.text_edit.setText(repr)
