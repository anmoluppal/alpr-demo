from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

from vehicle_info_provider import VehicleInfoProvider


class DynamicImagePlayer(QWidget):
    def __init__(self, generate_image_function, vehicle_info_provider: VehicleInfoProvider):
        super().__init__()

        self.generate_image_function = generate_image_function  # Function to generate images
        self.label = QLabel(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_frame())  # Correct connection

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setGeometry(100, 100, 1200, 800)

        self.timer.start(50)  # Adjust frame rate (milliseconds)
        self._vehicle_info_provider = vehicle_info_provider
    
    def update_frame(self):
        frame, ocr = self.generate_image_function()  # Call the image generation function
        
        if ocr is not None:
            vehicle_info = self._vehicle_info_provider.get_details(ocr)
            if vehicle_info is not None:
                print(vehicle_info)

        if frame is not None:  # Check if image generation was successful
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_qt_format)
            scaled_pixmap = pixmap.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.label.setPixmap(scaled_pixmap)