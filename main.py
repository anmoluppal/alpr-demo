import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from camera_feed import VideoFeedProvider
from player import DynamicImagePlayer
from vehicle_info_provider import VehicleInfoProvider


def main():
    app = QApplication([])
    video_feed_provider = VideoFeedProvider(Path("./assets"))
    vehicle_info_provider = VehicleInfoProvider(Path("./assets/vehicle_info.csv"))

    player = DynamicImagePlayer(video_feed_provider.get_frame, vehicle_info_provider)
    player.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
