import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from camera_feed import VideoFeedProvider
from player import DynamicImagePlayer


def main():
    app = QApplication([])
    video_feed_provider = VideoFeedProvider(Path("./assets"))

    player = DynamicImagePlayer(video_feed_provider.get_frame)
    player.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
